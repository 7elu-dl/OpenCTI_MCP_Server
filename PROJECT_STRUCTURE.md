# Project Structure

Complete directory structure of the OpenCTI FastMCP Server project.

```
OpenCTI_MCP_Claude/
│
├── 📁 opencti_mcp/              # Main package directory
│   ├── __init__.py              # Package initialization & public API
│   ├── server.py                # FastMCP server & tool definitions
│   ├── client.py                # OpenCTI API client (GraphQL + REST)
│   ├── config.py                # Configuration management
│   ├── queries.py               # GraphQL query templates
│   ├── observables.py           # Observable type detection & validation
│   └── exceptions.py            # Custom exception classes
│
├── 📁 docs/                     # Documentation
│   ├── README.md                # Documentation index
│   ├── CLAUDE.MD                # Developer guide & architecture
│   └── schema.txt               # OpenCTI GraphQL schema reference
│
├── 📁 examples/                 # Configuration examples
│   ├── README.md                # Examples documentation
│   ├── sample.env               # Sample environment configuration
│   └── test.env                 # Test environment configuration
│
├── 📄 README.md                 # Main project documentation
├── 📄 CONTRIBUTING.md           # Contribution guidelines
├── 📄 CHANGELOG.md              # Version history
├── 📄 LICENSE                   # MIT License
├── 📄 PROJECT_STRUCTURE.md      # This file
├── 📄 pyproject.toml            # Project metadata & dependencies
├── 📄 .gitignore                # Git ignore rules
│
└── 📄 .env                      # Environment variables (not in git)

# Build artifacts (not in repository)
├── opencti_mcp.egg-info/        # Package metadata (generated)
└── opencti_mcp/__pycache__/     # Python bytecode cache (generated)
```

## Directory Descriptions

### 📁 `opencti_mcp/` - Main Package
Core application code implementing the MCP server.

**Key Files**:
- **server.py**: FastMCP application with 13 tool definitions
- **client.py**: HTTP/GraphQL client for OpenCTI API communication
- **config.py**: Environment variable loading and validation
- **queries.py**: Predefined GraphQL query templates for all entities
- **observables.py**: Auto-detection logic for IPs, domains, and hashes
- **exceptions.py**: Custom exception classes and error wrappers

### 📁 `docs/` - Documentation
Comprehensive project documentation for developers and users.

**Key Files**:
- **CLAUDE.MD**: Complete architecture guide and developer documentation
- **schema.txt**: Full OpenCTI GraphQL schema (introspection results)
- **README.md**: Documentation navigation and index

### 📁 `examples/` - Configuration Examples
Template files and examples for various use cases.

**Key Files**:
- **sample.env**: Template with all configuration options
- **test.env**: Example configuration for testing
- **README.md**: Configuration guide and troubleshooting

## Root Files

### Documentation
- **README.md**: Main user-facing documentation with quick start
- **CONTRIBUTING.md**: Guidelines for contributors
- **CHANGELOG.md**: Version history and release notes
- **LICENSE**: MIT License text

### Configuration
- **pyproject.toml**: Python package configuration (dependencies, scripts)
- **.gitignore**: Files and directories to exclude from version control
- **.env**: Environment variables (user-created, not in repository)

## Module Relationships

```
┌─────────────────────────────────────────────────────┐
│                   server.py                         │
│  ┌───────────┐  ┌──────────┐  ┌─────────────┐     │
│  │  Tool 1   │  │  Tool 2  │  │   Tool 13   │     │
│  └─────┬─────┘  └────┬─────┘  └──────┬──────┘     │
│        └─────────────┴────────────────┘             │
└────────────────────┬────────────────────────────────┘
                     │
        ┌────────────▼───────────┐
        │      client.py         │
        │  ┌─────────────────┐  │
        │  │  GraphQL Client │  │
        │  │   REST Client   │  │
        │  └─────────────────┘  │
        └────────────────────────┘
                     │
        ┌────────────▼───────────┐
        │  OpenCTI API           │
        └────────────────────────┘

Supporting Modules:
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  config.py   │  │ queries.py   │  │observables.py│
│ (Settings)   │  │  (GraphQL)   │  │ (Detection)  │
└──────────────┘  └──────────────┘  └──────────────┘
```

## File Size Overview

| Component | Files | Lines of Code (approx) |
|-----------|-------|------------------------|
| Core Package | 7 | ~2,000 |
| Documentation | 5 | ~1,500 |
| Examples | 3 | ~100 |
| Configuration | 5 | ~200 |
| **Total** | **20** | **~3,800** |

## Version Control

### Tracked Files (in Git)
- All source code (`opencti_mcp/*.py`)
- Documentation (`docs/`, `*.md`)
- Configuration templates (`examples/*.env`)
- Project files (`pyproject.toml`, `.gitignore`)
- License (`LICENSE`)

### Ignored Files (not in Git)
- Environment variables (`.env`, `*.env` in root)
- Python cache (`__pycache__/`, `*.pyc`)
- Build artifacts (`*.egg-info/`, `build/`, `dist/`)
- IDE files (`.vscode/`, `.idea/`)
- OS files (`.DS_Store`, `Thumbs.db`)

## Installation Artifacts

After running `pip install -e .`:
- `opencti_mcp.egg-info/` - Package metadata
- `opencti_mcp/__pycache__/` - Compiled Python files
- Executable script in Python's `Scripts/` directory

## Adding New Files

### New Module
```bash
# Create in opencti_mcp/
touch opencti_mcp/new_module.py
# Update __init__.py to export public API
```

### New Documentation
```bash
# Create in docs/
touch docs/NEW_GUIDE.md
# Update docs/README.md with link
```

### New Example
```bash
# Create in examples/
touch examples/new_example.env
# Update examples/README.md with description
```

## Quick Navigation

- **User Documentation**: [README.md](README.md)
- **Developer Guide**: [docs/CLAUDE.MD](docs/CLAUDE.MD)
- **API Reference**: [opencti_mcp/](opencti_mcp/)
- **Examples**: [examples/](examples/)
- **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md)

## Cleanup Commands

```bash
# Remove Python cache
find . -type d -name __pycache__ -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# Remove build artifacts
rm -rf *.egg-info build dist

# Remove environment file (be careful!)
rm -f .env
```

## Project Statistics

- **Python Version**: 3.10+
- **Dependencies**: 3 direct (fastmcp, httpx, python-dotenv)
- **Tools Exposed**: 13 MCP tools
- **Supported Entities**: 9 STIX types
- **Observable Types**: 3 (IP, domain, hash)
- **Lines of Documentation**: ~1,500
- **Test Coverage**: Manual testing (automated tests TODO)

## Architecture Principles

- ✅ **Modular**: Separated concerns across 7 modules
- ✅ **Type-Safe**: Full Python type hints
- ✅ **Async**: All I/O operations are async
- ✅ **Documented**: Comprehensive inline and external docs
- ✅ **Extensible**: Easy to add new tools and features
- ✅ **Secure**: Environment-based configuration, SSL by default

---

**Last Updated**: 2025-01-25
**Project Version**: 0.1.0
