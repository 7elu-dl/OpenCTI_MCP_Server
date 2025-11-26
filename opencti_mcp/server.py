"""FastMCP server for querying OpenCTI."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, cast

from dotenv import load_dotenv
from fastmcp import Context, FastMCP
from fastmcp.exceptions import ToolError

# Handle running as standalone script
if __package__ in {None, ""}:
    sys.path.append(str(Path(__file__).resolve().parents[1]))
    from opencti_mcp.client import OpenCTIClient
    from opencti_mcp.config import get_settings
    from opencti_mcp.exceptions import ConfigurationError, OpenCTIAPIError, wrap_api_error
    from opencti_mcp.observables import (
        OBSERVABLE_TYPES,
        ObservableKind,
        infer_observable_type,
    )
    from opencti_mcp.queries import (
        COLLECTION_QUERIES,
        CORE_OBJECT_QUERY,
        CORE_RELATIONSHIP_QUERY,
        CYBER_OBSERVABLE_QUERY,
        ENTITY_ATTACK_PATTERNS_QUERY,
        ENTITY_INDICATORS_QUERY,
        ENTITY_NOTES_QUERY,
        ENTITY_OBSERVABLES_QUERY,
        ENTITY_RELATIONSHIPS_QUERY,
        LIST_CONNECTORS_QUERY,
        MALWARE_ANALYSIS_QUERY,
        SEARCH_BY_STIX_ID_QUERY,
        CollectionQuery,
    )
else:
    from .client import OpenCTIClient
    from .config import get_settings
    from .exceptions import ConfigurationError, OpenCTIAPIError, wrap_api_error
    from .observables import OBSERVABLE_TYPES, ObservableKind, infer_observable_type
    from .queries import (
        COLLECTION_QUERIES,
        CORE_OBJECT_QUERY,
        CORE_RELATIONSHIP_QUERY,
        CYBER_OBSERVABLE_QUERY,
        ENTITY_ATTACK_PATTERNS_QUERY,
        ENTITY_INDICATORS_QUERY,
        ENTITY_NOTES_QUERY,
        ENTITY_OBSERVABLES_QUERY,
        ENTITY_RELATIONSHIPS_QUERY,
        LIST_CONNECTORS_QUERY,
        MALWARE_ANALYSIS_QUERY,
        SEARCH_BY_STIX_ID_QUERY,
        CollectionQuery,
    )

# Load environment variables from .env file
load_dotenv()

# Initialize FastMCP application
app = FastMCP(
    name="opencti",
    instructions="Fetches intelligence data from an OpenCTI instance.",
)


def _build_client() -> OpenCTIClient:
    """
    Build a configured OpenCTI client instance.

    Returns:
        Configured OpenCTI client

    Raises:
        ToolError: If configuration is invalid
    """
    try:
        settings = get_settings()
    except ConfigurationError as exc:
        raise ToolError(str(exc)) from exc

    return OpenCTIClient(settings=settings)


async def _execute_collection_query(
    context: Context,
    *,
    config: CollectionQuery,
    search: str | None,
    limit: int,
) -> dict[str, Any]:
    """
    Execute a predefined collection query.

    Args:
        context: FastMCP context for logging
        config: Query configuration
        search: Optional search string
        limit: Maximum number of results

    Returns:
        Query results (edges, pageInfo)

    Raises:
        ToolError: If query fails or limit is invalid
    """
    if limit <= 0:
        raise ToolError("Parameter 'limit' must be greater than zero.")

    client = _build_client()
    variables: dict[str, Any] = {"first": limit}
    if search:
        variables["search"] = search

    context.log(f"Querying {config.label}: search='{search}', limit={limit}")

    try:
        data = await client.graphql_query(query=config.query, variables=variables)
    except OpenCTIAPIError as exc:
        context.log(f"OpenCTI error for {config.label}: {exc}")
        raise wrap_api_error(exc, "OpenCTI API error during query.") from exc

    if config.result_key not in data:
        raise ToolError(
            f"Unexpected OpenCTI response: missing '{config.result_key}'."
        )

    return data[config.result_key]


# Collection search tools

@app.tool(
    name="search_indicators",
    description="Search indicators via the OpenCTI GraphQL API.",
)
async def search_indicators(
    context: Context,
    search: str | None = None,
    *,
    limit: int = 25,
) -> dict[str, Any]:
    """Search indicators and return the raw OpenCTI response."""
    config = COLLECTION_QUERIES["indicators"]
    return await _execute_collection_query(
        context, config=config, search=search, limit=limit
    )


@app.tool(
    name="search_threat_actors",
    description="Search threat actors via the OpenCTI GraphQL API.",
)
async def search_threat_actors(
    context: Context,
    search: str | None = None,
    *,
    limit: int = 25,
) -> dict[str, Any]:
    """Search threat actors in OpenCTI."""
    config = COLLECTION_QUERIES["threat_actors"]
    return await _execute_collection_query(
        context, config=config, search=search, limit=limit
    )


@app.tool(
    name="search_intrusion_sets",
    description="Search intrusion sets via the OpenCTI GraphQL API.",
)
async def search_intrusion_sets(
    context: Context,
    search: str | None = None,
    *,
    limit: int = 25,
) -> dict[str, Any]:
    """Search intrusion sets in OpenCTI."""
    config = COLLECTION_QUERIES["intrusion_sets"]
    return await _execute_collection_query(
        context, config=config, search=search, limit=limit
    )


@app.tool(
    name="search_campaigns",
    description="Search campaigns via the OpenCTI GraphQL API.",
)
async def search_campaigns(
    context: Context,
    search: str | None = None,
    *,
    limit: int = 25,
) -> dict[str, Any]:
    """Search campaigns in OpenCTI."""
    config = COLLECTION_QUERIES["campaigns"]
    return await _execute_collection_query(
        context, config=config, search=search, limit=limit
    )


@app.tool(
    name="search_malware",
    description="Search malware families via the OpenCTI GraphQL API.",
)
async def search_malware(
    context: Context,
    search: str | None = None,
    *,
    limit: int = 25,
) -> dict[str, Any]:
    """Search malware entries in OpenCTI."""
    config = COLLECTION_QUERIES["malware"]
    return await _execute_collection_query(
        context, config=config, search=search, limit=limit
    )


@app.tool(
    name="search_attack_patterns",
    description="Search attack patterns via the OpenCTI GraphQL API.",
)
async def search_attack_patterns(
    context: Context,
    search: str | None = None,
    *,
    limit: int = 25,
) -> dict[str, Any]:
    """Search attack patterns in OpenCTI."""
    config = COLLECTION_QUERIES["attack_patterns"]
    return await _execute_collection_query(
        context, config=config, search=search, limit=limit
    )


@app.tool(
    name="search_infrastructures",
    description="Search adversary infrastructures via the OpenCTI GraphQL API.",
)
async def search_infrastructures(
    context: Context,
    search: str | None = None,
    *,
    limit: int = 25,
) -> dict[str, Any]:
    """Search infrastructures in OpenCTI."""
    config = COLLECTION_QUERIES["infrastructures"]
    return await _execute_collection_query(
        context, config=config, search=search, limit=limit
    )


@app.tool(
    name="search_vulnerabilities",
    description="Search vulnerabilities via the OpenCTI GraphQL API.",
)
async def search_vulnerabilities(
    context: Context,
    search: str | None = None,
    *,
    limit: int = 25,
) -> dict[str, Any]:
    """Search vulnerabilities in OpenCTI."""
    config = COLLECTION_QUERIES["vulnerabilities"]
    return await _execute_collection_query(
        context, config=config, search=search, limit=limit
    )


@app.tool(
    name="search_reports",
    description="Search intelligence reports via the OpenCTI GraphQL API.",
)
async def search_reports(
    context: Context,
    search: str | None = None,
    *,
    limit: int = 25,
) -> dict[str, Any]:
    """Search reports in OpenCTI."""
    config = COLLECTION_QUERIES["reports"]
    return await _execute_collection_query(
        context, config=config, search=search, limit=limit
    )


@app.tool(
    name="search_tools",
    description="Search attack tools via the OpenCTI GraphQL API.",
)
async def search_tools(
    context: Context,
    search: str | None = None,
    *,
    limit: int = 25,
) -> dict[str, Any]:
    """Search tools in OpenCTI."""
    config = COLLECTION_QUERIES["tools"]
    return await _execute_collection_query(
        context, config=config, search=search, limit=limit
    )


@app.tool(
    name="search_incidents",
    description="Search security incidents via the OpenCTI GraphQL API.",
)
async def search_incidents(
    context: Context,
    search: str | None = None,
    *,
    limit: int = 25,
) -> dict[str, Any]:
    """Search incidents in OpenCTI."""
    config = COLLECTION_QUERIES["incidents"]
    return await _execute_collection_query(
        context, config=config, search=search, limit=limit
    )


# Observable management tools

@app.tool(
    name="create_observable",
    description="Create a new observable (IP address, domain, or file hash) in OpenCTI.",
)
async def create_observable(
    context: Context,
    value: str,
    value_type: ObservableKind | None = None,
) -> dict[str, Any]:
    """
    Create a STIX Cyber Observable for the provided value.

    Args:
        context: FastMCP context
        value: Observable value (IP, domain, or hash)
        value_type: Optional explicit type specification

    Returns:
        Creation result with status and observable details
    """
    if not value or not value.strip():
        raise ToolError("Parameter 'value' must be a non-empty string.")

    # Determine observable type
    normalized_type = _normalize_observable_type(value, value_type)
    client = _build_client()
    allowed_types = OBSERVABLE_TYPES[normalized_type]

    context.log(
        f"Checking for existing observable: value='{value}', type='{normalized_type}'."
    )

    # Check if observable already exists
    try:
        existing = await client.find_observable_by_value(
            value.strip(), types=allowed_types
        )
    except OpenCTIAPIError as exc:
        raise wrap_api_error(
            exc, "Failed to search for observable in OpenCTI."
        ) from exc

    if existing:
        return _format_observable_result(existing, value, status="exists")

    # Create new observable
    context.log(f"Creating new {normalized_type} observable for value '{value}'.")

    try:
        created = await client.create_observable(
            value=value.strip(),
            observable_type=normalized_type,
        )
    except OpenCTIAPIError as exc:
        raise wrap_api_error(
            exc, "Failed to create observable in OpenCTI."
        ) from exc

    return _format_observable_result(created, value, status="created")


@app.tool(
    name="ask_virustotal_enrichment",
    description="Trigger VirusTotal enrichment for an observable (IP, domain, or hash).",
)
async def ask_virustotal_enrichment(
    context: Context,
    value: str,
    value_type: ObservableKind | None = None,
) -> dict[str, Any]:
    """
    Request enrichment via the VirusTotal connector.

    Args:
        context: FastMCP context
        value: Observable value
        value_type: Optional explicit type specification

    Returns:
        Enrichment job details
    """
    if not value or not value.strip():
        raise ToolError("Parameter 'value' must be a non-empty string.")

    # Get connector ID from settings
    settings = get_settings()
    if not settings.virustotal_connector_id:
        raise ToolError(
            "VirusTotal connector not configured. "
            "Set VIRUSTOTAL_CONNECTOR_ID environment variable."
        )

    # Determine observable type
    normalized_type = _normalize_observable_type(value, value_type)
    client = _build_client()
    allowed_types = OBSERVABLE_TYPES[normalized_type]

    context.log(
        f"Searching observable for enrichment: value='{value}', type='{normalized_type}'."
    )

    # Find the observable
    try:
        observable = await client.find_observable_by_value(
            value.strip(), types=allowed_types
        )
    except OpenCTIAPIError as exc:
        raise wrap_api_error(
            exc, "Failed to search for observable in OpenCTI."
        ) from exc

    if not observable:
        raise ToolError(
            f"No observable found matching value '{value}' for type '{normalized_type}'."
        )

    # Request enrichment
    observable_id = observable["id"]
    context.log(
        f"Requesting VirusTotal enrichment for observable '{observable_id}'."
    )

    try:
        work_id = await client.ask_enrichment(
            observable_id, settings.virustotal_connector_id
        )
    except OpenCTIAPIError as exc:
        raise wrap_api_error(
            exc, "Failed to request enrichment from OpenCTI."
        ) from exc

    observable_value = (
        observable.get("observable_value")
        or observable.get("value")
        or observable.get("name")
        or value
    )

    return {
        "work_id": work_id,
        "connector_id": settings.virustotal_connector_id,
        "observable": {
            "id": observable_id,
            "entity_type": observable.get("entity_type"),
            "value": observable_value,
        },
    }


# Entity retrieval tools

@app.tool(
    name="get_entity",
    description="Fetch a single entity by ID using the OpenCTI GraphQL API.",
)
async def get_entity(
    context: Context,
    entity_type: str,
    entity_id: str,
) -> dict[str, Any]:
    """
    Retrieve a specific OpenCTI entity.

    Args:
        context: FastMCP context
        entity_type: Expected entity type
        entity_id: OpenCTI internal ID

    Returns:
        Entity data
    """
    client = _build_client()
    context.log(f"Fetching OpenCTI entity {entity_type}/{entity_id}")

    # Try each query type
    queries = (
        ("stixCoreObject", CORE_OBJECT_QUERY),
        ("stixCoreRelationship", CORE_RELATIONSHIP_QUERY),
        ("stixCyberObservable", CYBER_OBSERVABLE_QUERY),
    )

    for key, query in queries:
        try:
            data = await client.graphql_query(query, {"id": entity_id})
        except OpenCTIAPIError as exc:
            raise wrap_api_error(
                exc, "Failed to fetch entity from OpenCTI."
            ) from exc

        result = data.get(key)
        if result:
            # Validate entity type if specified
            fetched_type = result.get("entity_type")
            if entity_type and fetched_type and fetched_type != entity_type:
                context.log(
                    f"Entity type mismatch for id '{entity_id}': "
                    f"expected '{entity_type}', got '{fetched_type}'."
                )
                continue
            return result

    raise ToolError(f"No entity found with id '{entity_id}'.")


@app.tool(
    name="execute_graphql",
    description="Execute a raw GraphQL query against the OpenCTI API.",
)
async def execute_graphql(
    context: Context,
    query: str,
    variables: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Run a GraphQL query and return the data payload.

    Args:
        context: FastMCP context
        query: GraphQL query string
        variables: Optional query variables

    Returns:
        Query response data
    """
    client = _build_client()
    context.log("Executing GraphQL query against OpenCTI")

    try:
        return await client.graphql_query(query=query, variables=variables)
    except OpenCTIAPIError as exc:
        raise wrap_api_error(exc, "Failed to execute GraphQL query.") from exc


# Relationship and analysis tools

@app.tool(
    name="get_entity_relationships",
    description="Get all relationships for a specific entity in OpenCTI.",
)
async def get_entity_relationships(
    context: Context,
    entity_id: str,
    *,
    limit: int = 50,
) -> dict[str, Any]:
    """
    Retrieve all relationships connected to an entity.

    Args:
        context: FastMCP context
        entity_id: OpenCTI internal ID of the entity
        limit: Maximum number of relationships to return

    Returns:
        Entity relationships data
    """
    if limit <= 0:
        raise ToolError("Parameter 'limit' must be greater than zero.")

    client = _build_client()
    context.log(f"Fetching relationships for entity {entity_id}")

    try:
        data = await client.graphql_query(
            query=ENTITY_RELATIONSHIPS_QUERY,
            variables={"id": entity_id, "first": limit},
        )
    except OpenCTIAPIError as exc:
        raise wrap_api_error(
            exc, "Failed to fetch entity relationships from OpenCTI."
        ) from exc

    if "stixCoreObject" not in data or not data["stixCoreObject"]:
        raise ToolError(f"No entity found with id '{entity_id}'.")

    return data["stixCoreObject"]


@app.tool(
    name="get_indicators_by_entity",
    description="Get indicators related to a specific entity (threat actor, malware, etc.).",
)
async def get_indicators_by_entity(
    context: Context,
    entity_id: str,
    *,
    limit: int = 25,
) -> dict[str, Any]:
    """
    Retrieve indicators associated with an entity.

    Args:
        context: FastMCP context
        entity_id: OpenCTI internal ID of the entity
        limit: Maximum number of indicators to return

    Returns:
        Related indicators data
    """
    if limit <= 0:
        raise ToolError("Parameter 'limit' must be greater than zero.")

    client = _build_client()
    context.log(f"Fetching indicators for entity {entity_id}")

    try:
        data = await client.graphql_query(
            query=ENTITY_INDICATORS_QUERY,
            variables={"id": entity_id, "first": limit},
        )
    except OpenCTIAPIError as exc:
        raise wrap_api_error(
            exc, "Failed to fetch entity indicators from OpenCTI."
        ) from exc

    if "stixCoreObject" not in data or not data["stixCoreObject"]:
        raise ToolError(f"No entity found with id '{entity_id}'.")

    return data["stixCoreObject"]


@app.tool(
    name="get_attack_patterns_by_entity",
    description="Get attack patterns (TTPs) used by a specific entity.",
)
async def get_attack_patterns_by_entity(
    context: Context,
    entity_id: str,
    *,
    limit: int = 25,
) -> dict[str, Any]:
    """
    Retrieve attack patterns associated with an entity.

    Args:
        context: FastMCP context
        entity_id: OpenCTI internal ID of the entity
        limit: Maximum number of attack patterns to return

    Returns:
        Related attack patterns data
    """
    if limit <= 0:
        raise ToolError("Parameter 'limit' must be greater than zero.")

    client = _build_client()
    context.log(f"Fetching attack patterns for entity {entity_id}")

    try:
        data = await client.graphql_query(
            query=ENTITY_ATTACK_PATTERNS_QUERY,
            variables={"id": entity_id, "first": limit},
        )
    except OpenCTIAPIError as exc:
        raise wrap_api_error(
            exc, "Failed to fetch entity attack patterns from OpenCTI."
        ) from exc

    if "stixCoreObject" not in data or not data["stixCoreObject"]:
        raise ToolError(f"No entity found with id '{entity_id}'.")

    return data["stixCoreObject"]


@app.tool(
    name="get_entity_observables",
    description="Get observables (IPs, domains, hashes) related to a specific entity.",
)
async def get_entity_observables(
    context: Context,
    entity_id: str,
    *,
    limit: int = 25,
) -> dict[str, Any]:
    """
    Retrieve observables associated with an entity.

    Args:
        context: FastMCP context
        entity_id: OpenCTI internal ID of the entity
        limit: Maximum number of observables to return

    Returns:
        Related observables data
    """
    if limit <= 0:
        raise ToolError("Parameter 'limit' must be greater than zero.")

    client = _build_client()
    context.log(f"Fetching observables for entity {entity_id}")

    try:
        data = await client.graphql_query(
            query=ENTITY_OBSERVABLES_QUERY,
            variables={"id": entity_id, "first": limit},
        )
    except OpenCTIAPIError as exc:
        raise wrap_api_error(
            exc, "Failed to fetch entity observables from OpenCTI."
        ) from exc

    if "stixCoreObject" not in data or not data["stixCoreObject"]:
        raise ToolError(f"No entity found with id '{entity_id}'.")

    return data["stixCoreObject"]


@app.tool(
    name="get_entity_notes",
    description="Get analysis notes for a specific entity in OpenCTI.",
)
async def get_entity_notes(
    context: Context,
    entity_id: str,
    *,
    limit: int = 10,
) -> dict[str, Any]:
    """
    Retrieve notes associated with an entity.

    Args:
        context: FastMCP context
        entity_id: OpenCTI internal ID of the entity
        limit: Maximum number of notes to return

    Returns:
        Entity notes data
    """
    if limit <= 0:
        raise ToolError("Parameter 'limit' must be greater than zero.")

    client = _build_client()
    context.log(f"Fetching notes for entity {entity_id}")

    try:
        data = await client.graphql_query(
            query=ENTITY_NOTES_QUERY,
            variables={"id": entity_id, "first": limit},
        )
    except OpenCTIAPIError as exc:
        raise wrap_api_error(
            exc, "Failed to fetch entity notes from OpenCTI."
        ) from exc

    if "stixCoreObject" not in data or not data["stixCoreObject"]:
        raise ToolError(f"No entity found with id '{entity_id}'.")

    return data["stixCoreObject"]


@app.tool(
    name="search_by_stix_id",
    description="Search for an entity using its STIX ID.",
)
async def search_by_stix_id(
    context: Context,
    stix_id: str,
) -> dict[str, Any]:
    """
    Retrieve an entity by its STIX identifier.

    Args:
        context: FastMCP context
        stix_id: STIX ID (e.g., threat-actor--...)

    Returns:
        Entity data
    """
    if not stix_id or not stix_id.strip():
        raise ToolError("Parameter 'stix_id' must be a non-empty string.")

    client = _build_client()
    context.log(f"Searching for entity with STIX ID: {stix_id}")

    try:
        data = await client.graphql_query(
            query=SEARCH_BY_STIX_ID_QUERY,
            variables={"stixId": stix_id},
        )
    except OpenCTIAPIError as exc:
        raise wrap_api_error(
            exc, "Failed to search by STIX ID in OpenCTI."
        ) from exc

    if "stixDomainObject" not in data or not data["stixDomainObject"]:
        raise ToolError(f"No entity found with STIX ID '{stix_id}'.")

    return data["stixDomainObject"]


@app.tool(
    name="list_connectors",
    description="List all available connectors in OpenCTI.",
)
async def list_connectors(
    context: Context,
) -> dict[str, Any]:
    """
    Retrieve the list of all connectors.

    Args:
        context: FastMCP context

    Returns:
        List of connectors with their details
    """
    client = _build_client()
    context.log("Fetching list of connectors")

    try:
        data = await client.graphql_query(query=LIST_CONNECTORS_QUERY)
    except OpenCTIAPIError as exc:
        raise wrap_api_error(
            exc, "Failed to fetch connectors from OpenCTI."
        ) from exc

    return data


@app.tool(
    name="get_malware_analysis",
    description="Get detailed analysis information for a specific malware family.",
)
async def get_malware_analysis(
    context: Context,
    malware_id: str,
) -> dict[str, Any]:
    """
    Retrieve comprehensive malware analysis data.

    Args:
        context: FastMCP context
        malware_id: OpenCTI internal ID of the malware

    Returns:
        Detailed malware analysis data including relationships and kill chain phases
    """
    if not malware_id or not malware_id.strip():
        raise ToolError("Parameter 'malware_id' must be a non-empty string.")

    client = _build_client()
    context.log(f"Fetching malware analysis for {malware_id}")

    try:
        data = await client.graphql_query(
            query=MALWARE_ANALYSIS_QUERY,
            variables={"id": malware_id},
        )
    except OpenCTIAPIError as exc:
        raise wrap_api_error(
            exc, "Failed to fetch malware analysis from OpenCTI."
        ) from exc

    if "malware" not in data or not data["malware"]:
        raise ToolError(f"No malware found with id '{malware_id}'.")

    return data["malware"]


# Helper functions

def _normalize_observable_type(
    value: str, value_type: ObservableKind | None
) -> ObservableKind:
    """
    Normalize and validate observable type.

    Args:
        value: Observable value
        value_type: Optional explicit type

    Returns:
        Normalized observable type

    Raises:
        ToolError: If type is invalid or cannot be inferred
    """
    if value_type:
        normalized = cast(ObservableKind, value_type.lower())
        if normalized not in OBSERVABLE_TYPES:
            raise ToolError(
                "Parameter 'value_type' must be one of: ip, domain, hash."
            )
        return normalized

    # Attempt to infer type
    inferred = infer_observable_type(value)
    if not inferred:
        raise ToolError(
            "Unable to infer value type. "
            "Please provide 'value_type' as ip, domain, or hash."
        )

    return inferred


def _format_observable_result(
    observable: dict[str, Any], original_value: str, *, status: str
) -> dict[str, Any]:
    """Format observable creation/retrieval result."""
    return {
        "status": status,
        "observable": {
            "id": observable["id"],
            "entity_type": observable.get("entity_type"),
            "value": (
                observable.get("observable_value")
                or observable.get("value")
                or observable.get("name")
                or original_value
            ),
        },
    }


def main() -> None:
    """Entry point for running as a CLI."""
    app.run()


if __name__ == "__main__":
    main()
