"""Observable value detection and validation utilities."""

from __future__ import annotations

import ipaddress
import re
from typing import Literal

# Type alias for observable kinds
ObservableKind = Literal["ip", "domain", "hash"]

# Mapping of observable kinds to STIX types
OBSERVABLE_TYPES: dict[ObservableKind, tuple[str, ...]] = {
    "ip": ("IPv4-Addr", "IPv6-Addr"),
    "domain": ("Domain-Name",),
    "hash": ("Artifact", "StixFile"),
}

# Valid hash lengths (MD5=32, SHA-1=40, SHA-256=64, SHA-512=128)
HASH_LENGTHS = frozenset({32, 40, 64, 128})

# Regex patterns for validation
HASH_REGEX = re.compile(r"^[A-Fa-f0-9]+$")
DOMAIN_REGEX = re.compile(
    r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)"
    r"(?:\.(?!-)[A-Za-z0-9-]{1,63}(?<!-))*"
    r"\.[A-Za-z]{2,63}$"
)


def infer_observable_type(value: str) -> ObservableKind | None:
    """
    Infer the observable type from a value string.

    Args:
        value: The observable value to analyze

    Returns:
        The inferred observable kind, or None if type cannot be determined

    Examples:
        >>> infer_observable_type("192.168.1.1")
        'ip'
        >>> infer_observable_type("example.com")
        'domain'
        >>> infer_observable_type("d41d8cd98f00b204e9800998ecf8427e")
        'hash'
    """
    candidate = value.strip()
    if not candidate:
        return None

    # Check if it's an IP address
    if _is_ip_address(candidate):
        return "ip"

    # Check if it's a hash (must be hex and match valid hash lengths)
    if _is_hash(candidate):
        return "hash"

    # Check if it's a domain name
    if _is_domain(candidate):
        return "domain"

    return None


def get_hash_algorithm(hash_value: str) -> str:
    """
    Determine the hash algorithm based on hash length.

    Args:
        hash_value: The hash string

    Returns:
        The algorithm name (MD5, SHA-1, SHA-256, or SHA-512)

    Raises:
        ValueError: If the hash length doesn't match any known algorithm
    """
    length = len(hash_value)
    algorithm_map = {
        32: "MD5",
        40: "SHA-1",
        64: "SHA-256",
        128: "SHA-512",
    }

    if length not in algorithm_map:
        raise ValueError(
            f"Invalid hash length {length}. Expected one of: {sorted(algorithm_map.keys())}"
        )

    return algorithm_map[length]


def _is_ip_address(value: str) -> bool:
    """Check if value is a valid IPv4 or IPv6 address."""
    try:
        ipaddress.ip_address(value)
        return True
    except ValueError:
        return False


def _is_hash(value: str) -> bool:
    """Check if value appears to be a cryptographic hash."""
    lower = value.lower()
    return len(lower) in HASH_LENGTHS and HASH_REGEX.match(lower) is not None


def _is_domain(value: str) -> bool:
    """Check if value appears to be a domain name."""
    return DOMAIN_REGEX.match(value) is not None
