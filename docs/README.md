# Documentation

This directory contains detailed documentation for the OpenCTI FastMCP Server project.

## 📚 Available Documentation

### [CLAUDE.MD](CLAUDE.MD)
**Developer Guide and Project Architecture**

Complete technical documentation covering:
- Project overview and architecture
- Module structure and responsibilities
- Available tools and their usage
- Code design patterns
- Observable type detection
- Common workflows
- Extension points
- Installation and configuration
- Security considerations
- Troubleshooting guide
- Future enhancement ideas

**Audience**: Developers, contributors, and advanced users

### [schema.txt](schema.txt)
**OpenCTI GraphQL Schema**

Complete GraphQL schema introspection results from OpenCTI API.

**Usage**:
- Reference for building custom queries
- Understanding available types and fields
- Validating query structure
- API exploration

**Format**: JSON introspection results

## 🎯 Quick Links

### For Users
- [Main README](../README.md) - Installation and usage
- [Examples](../examples/README.md) - Configuration examples

### For Developers
- [CLAUDE.MD](CLAUDE.MD) - Architecture guide
- [Contributing Guide](../CONTRIBUTING.md) - How to contribute
- [schema.txt](schema.txt) - GraphQL reference

## 📖 Documentation Structure

```
docs/
├── README.md        # This file (documentation index)
├── CLAUDE.MD        # Developer guide and architecture
└── schema.txt       # OpenCTI GraphQL schema
```

## 🔍 Finding Information

### Installation and Setup
→ See [Main README](../README.md#-quick-start)

### Tool Usage
→ See [Main README](../README.md#-available-tools)

### Architecture Details
→ See [CLAUDE.MD](CLAUDE.MD#architecture)

### Adding Features
→ See [CONTRIBUTING.md](../CONTRIBUTING.md#-architecture-guidelines)

### GraphQL Queries
→ See [schema.txt](schema.txt) and [CLAUDE.MD](CLAUDE.MD#graphql-query-structure)

### Troubleshooting
→ See [Main README](../README.md#-troubleshooting) and [CLAUDE.MD](CLAUDE.MD#troubleshooting)

## 🛠️ Building Custom Queries

Reference the GraphQL schema to build custom queries:

```python
from opencti_mcp import OpenCTIClient, get_settings

client = OpenCTIClient(settings=get_settings())

custom_query = """
query CustomQuery($search: String) {
  indicators(search: $search, first: 10) {
    edges {
      node {
        id
        name
        pattern
      }
    }
  }
}
"""

result = await client.graphql_query(custom_query, {"search": "malware"})
```

## 📝 Documentation Guidelines

When updating documentation:

1. **Keep it current**: Update docs when code changes
2. **Be clear**: Use simple, direct language
3. **Add examples**: Show, don't just tell
4. **Link appropriately**: Cross-reference related sections
5. **Consider audience**: Write for your target reader

## 🤝 Contributing to Documentation

Documentation improvements are always welcome!

- Fix typos or unclear explanations
- Add missing examples
- Improve formatting
- Update outdated information
- Add diagrams or visualizations

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

## 📮 Questions?

If documentation doesn't answer your question:

1. Check [existing issues](https://github.com/yourusername/OpenCTI_MCP_Claude/issues)
2. Open a [new issue](https://github.com/yourusername/OpenCTI_MCP_Claude/issues/new)
3. Start a [discussion](https://github.com/yourusername/OpenCTI_MCP_Claude/discussions)

## 🔗 External Resources

- [OpenCTI Documentation](https://docs.opencti.io/)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)
- [GraphQL Documentation](https://graphql.org/)
