"""Configuration management for the OpenCTI FastMCP server."""

from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache

from .exceptions import ConfigurationError


@dataclass(frozen=True, slots=True)
class OpenCTISettings:
    """Application settings loaded from environment variables."""

    base_url: str
    api_token: str
    verify_ssl: bool = True
    timeout_seconds: float = 30.0
    virustotal_connector_id: str | None = None

    @classmethod
    def from_env(cls) -> OpenCTISettings:
        """
        Build settings from environment variables.

        Required variables:
            - OPENCTI_URL: Base URL of the OpenCTI instance
            - OPENCTI_TOKEN: API authentication token

        Optional variables:
            - OPENCTI_VERIFY_SSL: Enable/disable SSL verification (default: true)
            - OPENCTI_TIMEOUT: Request timeout in seconds (default: 30)
            - VIRUSTOTAL_CONNECTOR_ID: Connector ID for VirusTotal enrichment

        Returns:
            Configured OpenCTISettings instance

        Raises:
            ConfigurationError: If required environment variables are missing
        """
        base_url = os.environ.get("OPENCTI_URL")
        api_token = os.environ.get("OPENCTI_TOKEN")

        # Validate required settings
        missing = []
        if not base_url:
            missing.append("OPENCTI_URL")
        if not api_token:
            missing.append("OPENCTI_TOKEN")

        if missing:
            raise ConfigurationError(
                f"Missing required OpenCTI configuration: {', '.join(missing)}"
            )

        # Parse optional boolean for SSL verification
        verify_raw = os.environ.get("OPENCTI_VERIFY_SSL", "true").lower()
        verify_ssl = verify_raw not in {"0", "false", "no", "off"}

        # Parse optional timeout
        timeout_raw = os.environ.get("OPENCTI_TIMEOUT", "").strip()
        try:
            timeout_seconds = float(timeout_raw) if timeout_raw else 30.0
        except ValueError:
            raise ConfigurationError(
                f"Invalid OPENCTI_TIMEOUT value: '{timeout_raw}'. Must be a number."
            )

        # Get optional VirusTotal connector ID
        vt_connector_id = os.environ.get("VIRUSTOTAL_CONNECTOR_ID") or None

        return cls(
            base_url=base_url.rstrip("/"),
            api_token=api_token,
            verify_ssl=verify_ssl,
            timeout_seconds=timeout_seconds,
            virustotal_connector_id=vt_connector_id,
        )


@lru_cache(maxsize=1)
def get_settings() -> OpenCTISettings:
    """
    Return cached settings instance.

    This function ensures settings are loaded only once and reused
    across multiple calls.

    Returns:
        Singleton OpenCTISettings instance

    Raises:
        ConfigurationError: If configuration is invalid
    """
    return OpenCTISettings.from_env()
