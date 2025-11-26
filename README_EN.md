# OpenCTI FastMCP Server

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastMCP](https://img.shields.io/badge/FastMCP-2.13+-green.svg)](https://github.com/jlowin/fastmcp)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Model Context Protocol (MCP) server that connects Claude AI to [OpenCTI](https://www.opencti.io/) threat intelligence platform. Built with [FastMCP](https://github.com/jlowin/fastmcp), this server exposes OpenCTI's capabilities as easy-to-use tools for AI-powered threat intelligence analysis.

## 🌟 Features

### Search & Discovery
- **11 Search Tools**: Search indicators, threat actors, intrusion sets, campaigns, malware, attack patterns, infrastructures, vulnerabilities, reports, tools, and incidents
- **Smart Filtering**: Search with keywords and limit results
- **Rich Metadata**: Retrieve comprehensive STIX-compliant threat intelligence data

### Observable Management
- **Auto-Detection**: Automatically identify IP addresses, domains, and file hashes
- **Deduplication**: Check for existing observables before creation
- **VirusTotal Integration**: Request enrichment for observables via VirusTotal connector

### Relationship & Analysis Tools
- **Relationship Analysis**: Explore connections between entities
- **Entity Indicators**: Get indicators related to specific entities
- **Attack Pattern Mapping**: Retrieve TTPs used by threat actors or malware
- **Observable Tracking**: Find observables associated with entities
- **Note Management**: Access analyst notes and comments

### Advanced Capabilities
- **GraphQL Queries**: Execute arbitrary GraphQL queries for custom data retrieval
- **Entity Retrieval**: Fetch detailed information about any STIX object
- **STIX ID Search**: Look up entities by their STIX identifiers
- **Connector Management**: List and manage enrichment connectors
- **Malware Analysis**: Get comprehensive malware family information
- **Type Safety**: Full Python type hints for better IDE support

## 📋 Requirements

- **Python**: 3.10 or higher
- **OpenCTI**: Access to an OpenCTI instance (v5.x or v6.x)
- **API Token**: Valid OpenCTI API token with appropriate permissions

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/OpenCTI_MCP_Claude.git
cd OpenCTI_MCP_Claude

# Install the package
pip install -e .
```

### 2. Configuration

Create a `.env` file in the project root:

```bash
# Required
OPENCTI_URL=https://your-opencti.example.com
OPENCTI_TOKEN=your_api_token_here

# Optional
OPENCTI_VERIFY_SSL=true                    # Enable/disable SSL verification (default: true)
OPENCTI_TIMEOUT=30                         # Request timeout in seconds (default: 30)
VIRUSTOTAL_CONNECTOR_ID=your_vt_connector  # For VirusTotal enrichment
```

### 3. Running the Server

```bash
# Start the MCP server (STDIO transport)
opencti-mcp

# Or run directly with Python
python -m opencti_mcp.server
```

The server will start and listen for MCP protocol messages over STDIO, ready to connect with Claude Desktop or other MCP clients.

## 🔧 Claude Desktop Integration

Add this configuration to your Claude Desktop config file:

**macOS/Linux**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "opencti": {
      "command": "python",
      "args": [
        "D:/code/OpenCTI_MCP_Claude/opencti_mcp/server.py"
      ],
      "env": {
        "OPENCTI_URL": "https://your-opencti.example.com",
        "OPENCTI_TOKEN": "your_api_token_here"
      }
    }
  }
}
```

Restart Claude Desktop to load the server.

## 🛠️ Available Tools (23 Total)

### Search Tools (11 tools)

All search tools accept optional parameters:
- `search` (string, optional): Search term to filter results
- `limit` (int, default: 25): Maximum number of results to return

#### 1. `search_indicators`
Search for Indicators of Compromise (IoCs) in OpenCTI.

**Returns**: Indicators with pattern types, valid dates, scores, and STIX metadata

**Example**:
```
Claude: Search for indicators related to "ransomware"
```

#### 2. `search_threat_actors`
Locate threat actor profiles and APT groups.

**Returns**: Threat actors with aliases, motivations, sophistication levels, and goals

**Example**:
```
Claude: Find threat actors associated with espionage campaigns
```

#### 3. `search_intrusion_sets`
Find organized threat groups and intrusion sets.

**Returns**: Intrusion sets with aliases, goals, resource levels, and motivations

#### 4. `search_campaigns`
Search for attack campaigns.

**Returns**: Campaigns with objectives, temporal information, and aliases

#### 5. `search_malware`
Locate malware families and samples.

**Returns**: Malware with types, capabilities, implementation languages, and execution environments

#### 6. `search_attack_patterns`
Find TTPs (Tactics, Techniques, and Procedures) including MITRE ATT&CK patterns.

**Returns**: Attack patterns with MITRE IDs, platforms, permissions required, and detection methods

#### 7. `search_infrastructures`
Search for adversary infrastructure.

**Returns**: Infrastructure with types, temporal bounds, and aliases

#### 8. `search_vulnerabilities`
Locate CVEs and vulnerability information.

**Returns**: Vulnerabilities with CVSS scores, severity, attack vectors, and impact assessments

#### 9. `search_reports`
Search threat intelligence reports.

**Returns**: Reports with types, publication dates, and confidence levels

#### 10. `search_tools`
Search for attack tools used by threat actors.

**Returns**: Tools with types, versions, aliases, and STIX metadata

**Example**:
```
Claude: Find tools related to "powershell"
```

#### 11. `search_incidents`
Search for security incidents in OpenCTI.

**Returns**: Incidents with severity, types, objectives, and temporal information

**Example**:
```
Claude: Search for ransomware incidents
```

### Observable Management Tools (2 tools)

#### 12. `create_observable`
Create a new observable (IP address, domain name, or file hash) in OpenCTI.

**Parameters**:
- `value` (string, required): The observable value
- `value_type` (string, optional): Explicitly specify `ip`, `domain`, or `hash` (auto-detected if omitted)

**Auto-Detection**:
- **IP addresses**: IPv4 and IPv6 format validation
- **Domains**: FQDN pattern matching
- **Hashes**: MD5 (32), SHA-1 (40), SHA-256 (64), SHA-512 (128)

**Returns**: Status (`created` or `exists`) and observable details

**Example**:
```
Claude: Create an observable for IP 192.168.1.100
```

#### 13. `ask_virustotal_enrichment`
Request VirusTotal enrichment for an observable.

**Parameters**:
- `value` (string, required): Observable value
- `value_type` (string, optional): Type specification

**Requirements**: `VIRUSTOTAL_CONNECTOR_ID` must be configured

**Returns**: Work ID, connector ID, and observable information

**Example**:
```
Claude: Enrich this hash with VirusTotal: d41d8cd98f00b204e9800998ecf8427e
```

### Entity & Query Tools (2 tools)

#### 14. `get_entity`
Retrieve detailed information about a specific entity by ID.

**Parameters**:
- `entity_type` (string, required): Entity type (e.g., `Indicator`, `ThreatActor`)
- `entity_id` (string, required): OpenCTI internal ID

**Returns**: Complete entity data including relationships and metadata

**Example**:
```
Claude: Get entity details for indicator ID abc123...
```

#### 15. `execute_graphql`
Execute arbitrary GraphQL queries against the OpenCTI API.

**Parameters**:
- `query` (string, required): GraphQL query string
- `variables` (dict, optional): Query variables

**Returns**: Raw GraphQL response data

**Example**:
```
Claude: Execute a GraphQL query to find all indicators created in the last 7 days
```

### Relationship & Analysis Tools (8 tools)

#### 16. `get_entity_relationships`
Get all relationships for a specific entity.

**Parameters**:
- `entity_id` (string, required): OpenCTI internal ID
- `limit` (int, default: 50): Maximum number of relationships

**Returns**: All relationships (from/to) connected to the entity

**Example**:
```
Claude: Show me all relationships for this threat actor
```

#### 17. `get_indicators_by_entity`
Get indicators related to a specific entity (threat actor, malware, campaign, etc.).

**Parameters**:
- `entity_id` (string, required): OpenCTI internal ID
- `limit` (int, default: 25): Maximum number of indicators

**Returns**: Indicators associated with the entity

**Example**:
```
Claude: Find all indicators for this malware family
```

#### 18. `get_attack_patterns_by_entity`
Get attack patterns (TTPs) used by a specific entity.

**Parameters**:
- `entity_id` (string, required): OpenCTI internal ID
- `limit` (int, default: 25): Maximum number of attack patterns

**Returns**: MITRE ATT&CK patterns and other TTPs used by the entity

**Example**:
```
Claude: What attack patterns does APT28 use?
```

#### 19. `get_entity_observables`
Get observables (IPs, domains, hashes) related to a specific entity.

**Parameters**:
- `entity_id` (string, required): OpenCTI internal ID
- `limit` (int, default: 25): Maximum number of observables

**Returns**: Cyber observables associated with the entity

**Example**:
```
Claude: Show me all observables for this campaign
```

#### 20. `get_entity_notes`
Get analysis notes and comments for a specific entity.

**Parameters**:
- `entity_id` (string, required): OpenCTI internal ID
- `limit` (int, default: 10): Maximum number of notes

**Returns**: Analyst notes with content, authors, and timestamps

**Example**:
```
Claude: Get all analyst notes for this incident
```

#### 21. `search_by_stix_id`
Search for an entity using its STIX identifier.

**Parameters**:
- `stix_id` (string, required): STIX ID (e.g., `threat-actor--12345...`)

**Returns**: Entity data for the STIX object

**Example**:
```
Claude: Find entity with STIX ID threat-actor--12345...
```

#### 22. `list_connectors`
List all available enrichment and integration connectors.

**Returns**: Connector details including type, scope, status, and configuration

**Example**:
```
Claude: What connectors are available in OpenCTI?
```

#### 23. `get_malware_analysis`
Get comprehensive analysis information for a malware family.

**Parameters**:
- `malware_id` (string, required): OpenCTI internal ID of the malware

**Returns**: Detailed malware data including capabilities, kill chain phases, and relationships

**Example**:
```
Claude: Analyze this malware family in detail
```

## 📊 Usage Examples

### Example 1: Threat Actor Investigation
```
User: Tell me about APT28

Claude uses:
1. search_threat_actors(search="APT28")
2. get_entity(entity_type="ThreatActor", entity_id="...")
3. search_campaigns() to find related campaigns

Response: Detailed APT28 profile with campaigns, TTPs, and targets
```

### Example 2: Malware Analysis
```
User: Analyze this file hash: 5d41402abc4b2a76b9719d911017c592

Claude uses:
1. create_observable(value="5d41402abc4b2a76b9719d911017c592")
2. ask_virustotal_enrichment(value="5d41402abc4b2a76b9719d911017c592")

Response: Creates observable and initiates VT analysis
```

### Example 3: Campaign Research
```
User: What are the latest ransomware campaigns?

Claude uses:
1. search_campaigns(search="ransomware")
2. search_malware(search="ransomware")
3. search_indicators() to find associated IoCs

Response: Comprehensive ransomware campaign overview
```

## 🏗️ Architecture

```
┌─────────────┐
│   Claude    │  ← MCP Protocol
└──────┬──────┘
       │
┌──────▼──────────────┐
│  FastMCP Server     │  ← This Project
│  (opencti_mcp)      │
└──────┬──────────────┘
       │
┌──────▼──────────────┐
│  OpenCTI GraphQL    │  ← Threat Intelligence
│  & REST API         │     Platform
└─────────────────────┘
```

### Module Structure

```
opencti_mcp/
├── __init__.py          # Package initialization
├── server.py            # FastMCP server & tool definitions
├── client.py            # OpenCTI API client (GraphQL + REST)
├── config.py            # Configuration management
├── queries.py           # GraphQL query templates
├── observables.py       # Observable type detection
└── exceptions.py        # Custom exceptions
```

## 🔒 Security

- **API Tokens**: Never commit tokens to version control
- **SSL Verification**: Enabled by default (`OPENCTI_VERIFY_SSL=true`)
- **Input Validation**: Multi-layer validation (server → client → API)
- **Network Segmentation**: Consider restricting OpenCTI access
- **Connector Permissions**: Review enrichment connector permissions

## 🐛 Troubleshooting

### Import Errors
```bash
# Ensure package is installed
pip install -e .

# Check Python version
python --version  # Should be 3.10+
```

### Connection Issues
```bash
# Test OpenCTI connectivity
curl -H "Authorization: Bearer YOUR_TOKEN" https://your-opencti.example.com/graphql

# Disable SSL verification for testing (not recommended for production)
export OPENCTI_VERIFY_SSL=false
```

### GraphQL Errors
- Verify entity IDs are internal OpenCTI IDs (not `standard_id`)
- Check OpenCTI logs for detailed error messages
- Use `execute_graphql` tool to test queries interactively

### Enrichment Not Working
- Confirm `VIRUSTOTAL_CONNECTOR_ID` is correctly configured
- Verify the connector is enabled in OpenCTI settings
- Check that the observable exists before requesting enrichment

## 📚 Development

### Code Style
- Python 3.10+ with type hints
- Google-style docstrings
- Frozen dataclasses for immutability
- Modular architecture (Single Responsibility Principle)

### Testing
```bash
# Run with test environment
cp test.env .env
# Edit .env with your test instance details
opencti-mcp
```

### Adding New Search Tools
1. Add GraphQL query to `queries.py`
2. Create tool function in `server.py` with `@app.tool` decorator
3. Call `_execute_collection_query()` with query config
4. Update this README

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [OpenCTI](https://www.opencti.io/) - Cyber Threat Intelligence Platform
- [FastMCP](https://github.com/jlowin/fastmcp) - Fast Model Context Protocol Framework
- [Anthropic](https://www.anthropic.com/) - Claude AI and MCP Protocol

## 📞 Support

- **Documentation**: See [docs/CLAUDE.MD](docs/CLAUDE.MD) for detailed project guide
- **Examples**: Check [examples/](examples/) for configuration templates
- **Contributing**: Read [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines
- **Changelog**: See [CHANGELOG.md](CHANGELOG.md) for version history
- **Issues**: Report bugs via [GitHub Issues](https://github.com/yourusername/OpenCTI_MCP_Claude/issues)
- **OpenCTI Docs**: https://docs.opencti.io/
- **MCP Docs**: https://modelcontextprotocol.io/

## 🗺️ Roadmap

- [x] Relationship traversal tools ✅
- [x] Entity-specific queries (indicators, attack patterns, observables) ✅
- [x] Incident and tool search capabilities ✅
- [x] Malware analysis tools ✅
- [ ] Batch operations for multiple IoCs
- [ ] STIX bundle import/export
- [ ] Advanced filtering (confidence scores, TLP markings)
- [ ] Entity creation and update operations
- [ ] Caching layer for performance
- [ ] Rate limiting and backoff strategies
- [ ] WebSocket transport support
