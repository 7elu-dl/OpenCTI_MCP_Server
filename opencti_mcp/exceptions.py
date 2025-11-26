"""Exception classes and error handling utilities."""

from __future__ import annotations

from fastmcp.exceptions import ToolError


class OpenCTIAPIError(RuntimeError):
    """Raised when OpenCTI API returns an error response."""


class ConfigurationError(RuntimeError):
    """Raised when server configuration is incomplete or invalid."""


def wrap_api_error(exc: Exception, fallback_message: str) -> ToolError:
    """
    Convert an exception to a ToolError with a user-friendly message.

    Args:
        exc: The original exception
        fallback_message: Message to use if exception has no useful message

    Returns:
        A ToolError suitable for returning to MCP clients
    """
    message = str(exc).strip() or fallback_message
    return ToolError(message)
