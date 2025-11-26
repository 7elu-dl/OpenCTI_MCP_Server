# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2025-01-25

### Added
- Initial release of OpenCTI FastMCP Server
- 9 search tools for STIX entities (indicators, threat actors, intrusion sets, campaigns, malware, attack patterns, infrastructures, vulnerabilities, reports)
- Observable management tools (create_observable, ask_virustotal_enrichment)
- Entity retrieval tool (get_entity)
- GraphQL query execution tool (execute_graphql)
- Automatic observable type detection (IP, domain, hash)
- Support for IPv4, IPv6, domain names, and file hashes (MD5, SHA-1, SHA-256, SHA-512)
- VirusTotal enrichment integration
- Comprehensive GraphQL query templates
- Modular architecture with separated concerns
- Type-safe implementation with Python type hints
- Configuration management via environment variables
- SSL verification and timeout configuration
- Error handling with custom exceptions
- FastMCP integration for MCP protocol support

### Architecture
- Separated modules: server, client, config, queries, observables, exceptions
- Immutable dataclasses for configuration and query metadata
- Async/await pattern for all API operations
- Context manager pattern for HTTP clients
- Cached configuration singleton

### Documentation
- Comprehensive README with usage examples
- Developer guide (CLAUDE.MD) with architecture details
- Contributing guidelines
- Example configuration files
- GraphQL schema reference

### Security
- Environment-based configuration (no hardcoded credentials)
- SSL verification enabled by default
- Multi-layer input validation
- API token authentication

## [0.0.1] - 2025-01-20

### Added
- Initial project structure
- Basic FastMCP server setup
- Simple indicator search functionality

---

## Release Categories

### Added
New features, tools, or capabilities

### Changed
Changes to existing functionality

### Deprecated
Features that will be removed in future versions

### Removed
Features that have been removed

### Fixed
Bug fixes

### Security
Security-related changes or fixes

[Unreleased]: https://github.com/yourusername/OpenCTI_MCP_Claude/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/yourusername/OpenCTI_MCP_Claude/releases/tag/v0.1.0
[0.0.1]: https://github.com/yourusername/OpenCTI_MCP_Claude/releases/tag/v0.0.1
