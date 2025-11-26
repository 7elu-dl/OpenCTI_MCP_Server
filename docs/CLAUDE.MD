# OpenCTI FastMCP Server - Project Guide

## Project Overview
This is a Model Context Protocol (MCP) server that provides Claude with direct access to an OpenCTI threat intelligence platform. Built using FastMCP framework, it exposes OpenCTI's capabilities through standardized MCP tools.

## Architecture

### Module Structure (Post-Refactoring)

```
opencti_mcp/
├── __init__.py          # Package initialization and public API
├── server.py            # FastMCP server and tool definitions
├── client.py            # OpenCTI API client (GraphQL + REST)
├── config.py            # Configuration management
├── queries.py           # GraphQL query definitions
├── observables.py       # Observable detection and validation
└── exceptions.py        # Custom exception classes
```

### Module Responsibilities

#### server.py
- FastMCP application initialization
- MCP tool function definitions
- Request routing and validation
- Tool-level error handling

#### client.py
- HTTP client for OpenCTI REST API
- GraphQL query execution
- Observable CRUD operations
- Enrichment request handling
- Response parsing and validation

#### config.py
- Environment variable loading
- Settings validation
- Configuration singleton management

#### queries.py
- GraphQL query templates
- Collection query metadata (CollectionQuery dataclass)
- Entity retrieval queries

#### observables.py
- Observable type inference (IP, domain, hash)
- Value validation (regex patterns)
- Hash algorithm detection
- Type-to-STIX mapping

#### exceptions.py
- Custom exception definitions
- Error wrapping utilities
- Consistent error messaging

## Available Tools

### Search Tools
All search tools accept optional `search` (string) and `limit` (int, default 25) parameters:

1. **search_indicators** - Find IoCs (Indicators of Compromise)
2. **search_threat_actors** - Locate threat actor profiles
3. **search_intrusion_sets** - Find organized threat groups
4. **search_campaigns** - Search attack campaigns
5. **search_malware** - Locate malware families and samples
6. **search_attack_patterns** - Find TTPs (MITRE ATT&CK patterns)
7. **search_infrastructures** - Search adversary infrastructure
8. **search_vulnerabilities** - Find CVEs and vulnerability data
9. **search_reports** - Search threat intelligence reports

### Entity Management Tools

10. **get_entity** - Fetch specific entity by type and ID
    - Parameters: `entity_type`, `entity_id`
    - Supports: core objects, relationships, and observables

11. **create_observable** - Create new observable (IP/domain/hash)
    - Parameters: `value`, optional `value_type` (auto-detected)
    - Validates and deduplicates before creation

12. **ask_virustotal_enrichment** - Request VT enrichment
    - Parameters: `value`, optional `value_type`
    - Requires configured `VIRUSTOTAL_CONNECTOR_ID`

13. **execute_graphql** - Run arbitrary GraphQL queries
    - Parameters: `query`, optional `variables`
    - For advanced use cases beyond standard tools

## Configuration

### Required Environment Variables
```bash
OPENCTI_URL=https://your-opencti.example.com
OPENCTI_TOKEN=YOUR_API_TOKEN
```

### Optional Environment Variables
```bash
OPENCTI_VERIFY_SSL=true          # SSL certificate verification
OPENCTI_TIMEOUT=30               # Request timeout in seconds
VIRUSTOTAL_CONNECTOR_ID=UUID     # For VT enrichment feature
```

Configuration is loaded via `.env` file or environment variables.

## Code Design Patterns

### Separation of Concerns
- **Business Logic**: Client module handles API interactions
- **Validation**: Observables module handles type detection
- **Presentation**: Server module handles MCP tool interface
- **Configuration**: Config module handles environment setup
- **Data**: Queries module contains all GraphQL templates

### Error Handling Strategy
1. API errors caught at client level → OpenCTIAPIError
2. Configuration errors at startup → ConfigurationError
3. Both wrapped to ToolError at server level for MCP
4. Consistent error messages via wrap_api_error() utility

### Type Safety
- Literal types for observable kinds: `Literal["ip", "domain", "hash"]`
- Frozen dataclasses for immutable configuration
- Type hints throughout for better IDE support

### Code Reusability
- `_execute_collection_query()` handles all search tools
- `_normalize_observable_type()` shared validation logic
- `_format_observable_result()` consistent response formatting
- Static methods for pure utility functions

## Observable Type Detection

The server includes smart observable type inference:
- **IP addresses**: Validates IPv4/IPv6 format via `ipaddress` module
- **Domains**: Regex validation for valid FQDNs
- **Hashes**: Detects MD5 (32), SHA-1 (40), SHA-256 (64), SHA-512 (128)

Mapped to STIX types:
- `ip` → IPv4-Addr, IPv6-Addr
- `domain` → Domain-Name
- `hash` → Artifact, StixFile

Detection logic in `observables.py`:
```python
infer_observable_type(value: str) -> ObservableKind | None
```

## Common Workflows

### Indicator Investigation
1. Use `search_indicators` to find IoC by pattern
2. Get full details with `get_entity` using returned ID
3. Optionally enrich with `ask_virustotal_enrichment`

### Threat Actor Research
1. Search with `search_threat_actors` for actor name/alias
2. Use `execute_graphql` to fetch related campaigns/malware
3. Cross-reference with `search_reports` for analyst context

### Observable Management
1. `create_observable` automatically checks for duplicates
2. Returns existing entity if already present
3. Enables enrichment workflow via `ask_virustotal_enrichment`

## Extension Points

### Adding New Search Tools
1. Add GraphQL query to `COLLECTION_QUERIES` in `queries.py`
2. Create async tool function in `server.py` with `@app.tool` decorator
3. Call `_execute_collection_query()` with appropriate config
4. Update README.md with tool documentation

### Adding New Observable Types
1. Add regex/validation to `observables.py`
2. Add STIX type mapping to `OBSERVABLE_TYPES`
3. Implement creation logic in `client.py`
4. Update `ObservableKind` Literal type

### Custom GraphQL Queries
Use `execute_graphql` tool for one-off queries or prototype new search patterns before adding dedicated tools.

## Installation & Running

```bash
# Install package
pip install -e .

# Run server (STDIO transport by default)
opencti-mcp
```

FastMCP handles MCP protocol communication; server runs until terminated.

## Development Guidelines

### Code Style
- Use `from __future__ import annotations` for forward references
- Prefer frozen dataclasses for immutable data structures
- Use type hints for all function signatures
- Document with Google-style docstrings

### Testing Considerations
- Requires live OpenCTI instance or mock server
- Environment variables must be set before testing
- test.env and Sample.env available as configuration templates
- Consider adding pytest fixtures for client mocking

### Performance
- HTTP clients created per-request (context manager pattern)
- Settings cached via `@lru_cache` decorator
- GraphQL queries optimized to fetch only needed fields
- Configurable timeouts and SSL verification

## Refactoring Improvements

### Before
- 843-line monolithic `server.py`
- Mixed concerns (queries, validation, API client)
- Duplicate error handling code
- Hard to test individual components

### After
- Modular architecture (7 focused modules)
- Single Responsibility Principle applied
- Reusable validation and error handling
- Easy to mock and test components
- Better IDE navigation and code discovery

## Security Considerations

- API tokens should never be committed to version control
- Use `.env` for local development
- SSL verification enabled by default (OPENCTI_VERIFY_SSL)
- Consider network segmentation for OpenCTI access
- Review connector permissions for enrichment features
- Input validation at multiple layers (server → client → API)

## Troubleshooting

### Import Errors
- Ensure `opencti_mcp` package is installed (`pip install -e .`)
- Check Python version (requires 3.10+)
- Verify all dependencies installed

### Connection Issues
- Verify `OPENCTI_URL` is reachable
- Check `OPENCTI_TOKEN` has valid permissions
- Test with `OPENCTI_VERIFY_SSL=false` for cert issues (dev only)

### Query Failures
- Use `execute_graphql` to test queries interactively
- Check OpenCTI logs for GraphQL errors
- Verify entity IDs are internal OpenCTI IDs, not standard_ids

### Enrichment Not Working
- Confirm `VIRUSTOTAL_CONNECTOR_ID` is set correctly
- Check connector is enabled and configured in OpenCTI
- Verify observable exists before requesting enrichment

## Future Enhancement Ideas

- Add relationship traversal tools (get related entities)
- Support for creating/updating entities beyond observables
- Batch operations for multiple IoCs
- Filtering by confidence scores or TLP markings
- Support for STIX bundle import/export
- Caching layer for frequently accessed entities
- Async batch query optimization
- Rate limiting and backoff strategies
