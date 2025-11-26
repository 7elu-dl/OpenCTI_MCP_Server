"""OpenCTI API client for REST and GraphQL operations."""

from __future__ import annotations

import ipaddress
from dataclasses import dataclass
from typing import Any

import httpx

from .config import OpenCTISettings
from .exceptions import OpenCTIAPIError
from .observables import ObservableKind, get_hash_algorithm

# API path prefix for REST endpoints
_API_PREFIX = "/api/v1"


@dataclass(frozen=True, slots=True)
class OpenCTIClient:
    """Async client for the OpenCTI REST and GraphQL APIs."""

    settings: OpenCTISettings

    @property
    def _headers(self) -> dict[str, str]:
        """Generate HTTP headers with authentication."""
        return {
            "Authorization": f"Bearer {self.settings.api_token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def _create_http_client(self) -> httpx.AsyncClient:
        """Create a configured httpx client."""
        return httpx.AsyncClient(
            base_url=self.settings.base_url,
            verify=self.settings.verify_ssl,
            timeout=self.settings.timeout_seconds,
        )

    async def rest_get(
        self,
        resource: str,
        *,
        resource_id: str | None = None,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Perform a REST GET request against the OpenCTI API.

        Args:
            resource: The resource type (e.g., 'indicator', 'threat-actor')
            resource_id: Optional specific resource ID
            params: Optional query parameters

        Returns:
            JSON response data as dictionary

        Raises:
            OpenCTIAPIError: If the API returns an error
        """
        path = f"{_API_PREFIX}/{resource}"
        if resource_id:
            path = f"{path}/{resource_id}"

        async with self._create_http_client() as client:
            response = await client.get(path, params=params, headers=self._headers)
            response.raise_for_status()

            # Handle empty responses
            if response.status_code == 204 or not response.content:
                return {}

            # Parse JSON response
            try:
                payload = response.json()
            except ValueError as exc:
                snippet = self._truncate_text(response.text)
                raise OpenCTIAPIError(
                    f"Invalid JSON response from OpenCTI: {snippet}"
                ) from exc

        # Check for error status in response
        self._validate_response_status(payload)
        return payload

    async def graphql_query(
        self,
        query: str,
        variables: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Execute a GraphQL query against the OpenCTI API.

        Args:
            query: GraphQL query string
            variables: Optional query variables

        Returns:
            The 'data' portion of the GraphQL response

        Raises:
            OpenCTIAPIError: If the query fails or returns errors
        """
        body = {"query": query, "variables": variables or {}}

        async with self._create_http_client() as client:
            response = await client.post("/graphql", json=body, headers=self._headers)
            response.raise_for_status()

            try:
                payload = response.json()
            except ValueError as exc:
                snippet = self._truncate_text(response.text)
                raise OpenCTIAPIError(
                    f"Invalid JSON response from OpenCTI GraphQL API: {snippet}"
                ) from exc

        # Check for GraphQL errors
        if errors := payload.get("errors"):
            raise OpenCTIAPIError(f"GraphQL error: {errors}")

        return payload.get("data", {})

    async def find_observable_by_value(
        self,
        value: str,
        *,
        types: tuple[str, ...],
        limit: int = 10,
    ) -> dict[str, Any] | None:
        """
        Locate a STIX Cyber Observable matching the provided value.

        Args:
            value: The observable value to search for
            types: STIX types to filter by (e.g., 'IPv4-Addr', 'Domain-Name')
            limit: Maximum number of results to retrieve

        Returns:
            The matching observable node, or None if not found

        Raises:
            OpenCTIAPIError: If the query fails
        """
        query = """
        query FindObservables($search: String, $types: [String!], $first: Int) {
          stixCyberObservables(search: $search, types: $types, first: $first) {
            edges {
              node {
                id
                standard_id
                entity_type
                observable_value
                ... on DomainName { value }
                ... on IPv4Addr { value }
                ... on IPv6Addr { value }
                ... on StixFile {
                  name
                  hashes {
                    algorithm
                    hash
                  }
                }
                ... on Artifact {
                  url
                  hashes {
                    algorithm
                    hash
                  }
                }
              }
            }
          }
        }
        """
        data = await self.graphql_query(
            query,
            variables={
                "search": value,
                "types": list(types),
                "first": limit,
            },
        )

        container = data.get("stixCyberObservables", {})
        edges = container.get("edges", [])
        target = value.lower()

        # Search through results for exact match
        for edge in edges:
            if node := self._match_observable_node(edge, target):
                return node

        return None

    async def ask_enrichment(self, entity_id: str, connector_id: str) -> str:
        """
        Request enrichment for an entity using a connector.

        Args:
            entity_id: OpenCTI internal ID of the entity
            connector_id: ID of the enrichment connector

        Returns:
            Work ID for the enrichment job

        Raises:
            OpenCTIAPIError: If enrichment request fails
        """
        mutation = """
        mutation AskEnrichment($id: ID!, $connectorId: ID!) {
          stixCoreObjectEdit(id: $id) {
            askEnrichment(connectorId: $connectorId) {
              id
            }
          }
        }
        """
        data = await self.graphql_query(
            mutation, variables={"id": entity_id, "connectorId": connector_id}
        )

        edit_block = data.get("stixCoreObjectEdit", {})
        enrichment = edit_block.get("askEnrichment")

        if not enrichment or "id" not in enrichment:
            raise OpenCTIAPIError("Failed to request enrichment for the observable.")

        return enrichment["id"]

    async def create_observable(
        self,
        *,
        value: str,
        observable_type: ObservableKind,
    ) -> dict[str, Any]:
        """
        Create a STIX Cyber Observable of the specified type.

        Args:
            value: The observable value
            observable_type: Type of observable ('ip', 'domain', or 'hash')

        Returns:
            The created observable data

        Raises:
            OpenCTIAPIError: If creation fails
        """
        if observable_type == "domain":
            return await self._create_domain_observable(value)
        elif observable_type == "ip":
            return await self._create_ip_observable(value)
        else:  # hash
            return await self._create_hash_observable(value)

    # Private helper methods

    async def _create_domain_observable(self, value: str) -> dict[str, Any]:
        """Create a Domain-Name observable."""
        mutation = """
        mutation CreateDomain($type: String!, $input: DomainNameAddInput!) {
          stixCyberObservableAdd(type: $type, DomainName: $input) {
            id
            entity_type
            observable_value
          }
        }
        """
        variables = {
            "type": "Domain-Name",
            "input": {"value": value},
        }
        return await self._execute_create_mutation(mutation, variables)

    async def _create_ip_observable(self, value: str) -> dict[str, Any]:
        """Create an IPv4-Addr or IPv6-Addr observable."""
        try:
            ip_obj = ipaddress.ip_address(value)
        except ValueError as exc:
            raise OpenCTIAPIError(f"Invalid IP address value: {value}") from exc

        if ip_obj.version == 4:
            mutation = """
            mutation CreateIPv4($type: String!, $input: IPv4AddrAddInput!) {
              stixCyberObservableAdd(type: $type, IPv4Addr: $input) {
                id
                entity_type
                observable_value
              }
            }
            """
            stix_type = "IPv4-Addr"
        else:
            mutation = """
            mutation CreateIPv6($type: String!, $input: IPv6AddrAddInput!) {
              stixCyberObservableAdd(type: $type, IPv6Addr: $input) {
                id
                entity_type
                observable_value
              }
            }
            """
            stix_type = "IPv6-Addr"

        variables = {"type": stix_type, "input": {"value": value}}
        return await self._execute_create_mutation(mutation, variables)

    async def _create_hash_observable(self, value: str) -> dict[str, Any]:
        """Create an Artifact observable for a hash."""
        try:
            algo = get_hash_algorithm(value)
        except ValueError as exc:
            raise OpenCTIAPIError(str(exc)) from exc

        mutation = """
        mutation CreateArtifact($type: String!, $input: ArtifactAddInput!) {
          stixCyberObservableAdd(type: $type, Artifact: $input) {
            id
            entity_type
            observable_value
          }
        }
        """
        variables = {
            "type": "Artifact",
            "input": {
                "hashes": [{"algorithm": algo, "hash": value}],
            },
        }
        return await self._execute_create_mutation(mutation, variables)

    async def _execute_create_mutation(
        self, mutation: str, variables: dict[str, Any]
    ) -> dict[str, Any]:
        """Execute a create mutation and validate the result."""
        data = await self.graphql_query(mutation, variables=variables)
        created = data.get("stixCyberObservableAdd")
        if not created or "id" not in created:
            raise OpenCTIAPIError("Failed to create observable.")
        return created

    @staticmethod
    def _match_observable_node(edge: dict[str, Any], target: str) -> dict[str, Any] | None:
        """Check if an observable node matches the target value."""
        node = (edge or {}).get("node") or {}
        if not node:
            return None

        # Check direct value fields
        observed_values = [
            str(node.get("observable_value", "")).lower(),
            str(node.get("value", "")).lower(),
            str(node.get("name", "")).lower(),
        ]

        if target in observed_values:
            return node

        # Check hashes
        hashes = node.get("hashes") or []
        for entry in hashes:
            if str(entry.get("hash", "")).lower() == target:
                return node

        return None

    @staticmethod
    def _validate_response_status(payload: dict[str, Any]) -> None:
        """Validate that a REST response doesn't contain an error status."""
        if isinstance(payload, dict):
            status = payload.get("status")
            if status is not None and status != "success":
                message = payload.get("message") or str(payload)
                raise OpenCTIAPIError(f"OpenCTI reported an error: {message}")

    @staticmethod
    def _truncate_text(text: str, max_length: int = 200) -> str:
        """Truncate text for error messages."""
        snippet = text.strip()
        if len(snippet) > max_length:
            return snippet[:max_length] + "…"
        return snippet
