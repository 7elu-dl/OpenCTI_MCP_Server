"""OpenCTI FastMCP Server package.

This package provides a Model Context Protocol (MCP) server for interacting
with OpenCTI threat intelligence platforms.
"""

from __future__ import annotations

from .client import OpenCTIClient
from .config import OpenCTISettings, get_settings
from .exceptions import ConfigurationError, OpenCTIAPIError
from .observables import ObservableKind, infer_observable_type
from .queries import COLLECTION_QUERIES, CollectionQuery

__version__ = "0.1.0"

__all__ = [
    "OpenCTIClient",
    "OpenCTISettings",
    "get_settings",
    "ConfigurationError",
    "OpenCTIAPIError",
    "ObservableKind",
    "infer_observable_type",
    "COLLECTION_QUERIES",
    "CollectionQuery",
]
