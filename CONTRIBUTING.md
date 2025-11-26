# Contributing to OpenCTI FastMCP Server

Thank you for your interest in contributing to the OpenCTI FastMCP Server project! This document provides guidelines and instructions for contributing.

## 🤝 How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- Clear description of the bug
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details (Python version, OpenCTI version, OS)
- Relevant logs or error messages

### Suggesting Features

Feature requests are welcome! Please include:
- Clear use case
- Expected behavior
- Why this would be valuable
- Any implementation ideas

### Code Contributions

1. **Fork the Repository**
   ```bash
   git clone https://github.com/yourusername/OpenCTI_MCP_Claude.git
   cd OpenCTI_MCP_Claude
   ```

2. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

3. **Set Up Development Environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install in development mode
   pip install -e .

   # Copy example environment
   cp examples/sample.env .env
   # Edit .env with your OpenCTI credentials
   ```

4. **Make Your Changes**
   - Follow the code style guidelines below
   - Add tests if applicable
   - Update documentation as needed

5. **Test Your Changes**
   ```bash
   # Run the server
   python -m opencti_mcp.server

   # Test with Claude Desktop or MCP client
   ```

6. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "Brief description of changes"
   ```

7. **Push and Create Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then create a Pull Request on GitHub.

## 📝 Code Style Guidelines

### Python Style
- Follow [PEP 8](https://peps.python.org/pep-0008/)
- Use Python 3.10+ features
- Add type hints to all functions
- Use `from __future__ import annotations` for forward references

### Docstrings
Use Google-style docstrings:
```python
def example_function(param1: str, param2: int) -> bool:
    """
    Brief description of function.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: When invalid input is provided
    """
    pass
```

### Code Organization
- Keep functions focused (Single Responsibility Principle)
- Use dataclasses for immutable data structures
- Separate concerns into appropriate modules
- Write self-documenting code

### Example
```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class MyDataClass:
    """Immutable data class example."""

    field1: str
    field2: int


async def my_async_function(value: str) -> dict[str, Any]:
    """
    Example async function.

    Args:
        value: Input value to process

    Returns:
        Processed data dictionary
    """
    # Implementation here
    pass
```

## 🧪 Testing

### Manual Testing
1. Start OpenCTI test instance
2. Configure `.env` with test credentials
3. Run the server: `python -m opencti_mcp.server`
4. Test with Claude Desktop or MCP inspector

### Test Coverage
- Test all new features
- Ensure existing functionality isn't broken
- Test error handling and edge cases

## 📚 Documentation

### When to Update Documentation
- Adding new tools
- Changing existing APIs
- Adding configuration options
- Fixing bugs that affect usage

### Documentation Files
- **README.md**: User-facing documentation
- **docs/CLAUDE.MD**: Developer guide and architecture
- **Code comments**: Inline documentation for complex logic
- **Docstrings**: Function and class documentation

## 🔄 Pull Request Process

1. **Before Submitting**
   - Ensure code follows style guidelines
   - Update documentation
   - Test thoroughly
   - Write clear commit messages

2. **PR Description Should Include**
   - What changes were made
   - Why the changes are needed
   - How to test the changes
   - Any breaking changes
   - Related issues (if any)

3. **Review Process**
   - Maintainers will review your PR
   - Address feedback and requested changes
   - Once approved, maintainers will merge

4. **After Merge**
   - Delete your feature branch
   - Pull latest changes to your fork

## 🏗️ Architecture Guidelines

### Adding New Search Tools

1. **Add GraphQL Query** (`opencti_mcp/queries.py`)
   ```python
   "new_entity": CollectionQuery(
       result_key="newEntities",
       label="OpenCTI new entities",
       query="""
       query NewEntities($search: String, $first: Int) {
         newEntities(search: $search, first: $first) {
           edges {
             node {
               id
               name
               # ... other fields
             }
           }
           pageInfo {
             endCursor
             hasNextPage
           }
         }
       }
       """,
   )
   ```

2. **Add Tool Function** (`opencti_mcp/server.py`)
   ```python
   @app.tool(
       name="search_new_entities",
       description="Search new entities via OpenCTI GraphQL API.",
   )
   async def search_new_entities(
       context: Context,
       search: str | None = None,
       *,
       limit: int = 25,
   ) -> dict[str, Any]:
       """Search new entities in OpenCTI."""
       config = COLLECTION_QUERIES["new_entity"]
       return await _execute_collection_query(
           context, config=config, search=search, limit=limit
       )
   ```

3. **Update Documentation**
   - Add tool description to README.md
   - Update tool count in documentation

### Adding New Observable Types

1. **Update Detection** (`opencti_mcp/observables.py`)
   ```python
   def _is_new_type(value: str) -> bool:
       """Check if value is a new observable type."""
       # Add validation logic
       pass
   ```

2. **Update Type Mapping**
   ```python
   OBSERVABLE_TYPES: dict[ObservableKind, tuple[str, ...]] = {
       # ... existing types
       "new_type": ("NewSTIXType",),
   }
   ```

3. **Add Creation Logic** (`opencti_mcp/client.py`)
   ```python
   async def _create_new_type_observable(self, value: str) -> dict[str, Any]:
       """Create a new type observable."""
       # Implementation
       pass
   ```

## 🐛 Debugging Tips

### Enable Verbose Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Test GraphQL Queries
Use the `execute_graphql` tool to test queries interactively.

### Check OpenCTI Logs
Review OpenCTI server logs for API errors.

## 📮 Questions?

- Open a [GitHub Discussion](https://github.com/yourusername/OpenCTI_MCP_Claude/discussions)
- Check existing [Issues](https://github.com/yourusername/OpenCTI_MCP_Claude/issues)
- Review [docs/CLAUDE.MD](docs/CLAUDE.MD) for architecture details

## 🙏 Recognition

Contributors will be acknowledged in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for contributing to make OpenCTI FastMCP Server better!
