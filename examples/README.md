# Examples

This directory contains example configuration files and usage scenarios for the OpenCTI FastMCP Server.

## Configuration Examples

### `sample.env`
Template environment file with all available configuration options.

**Usage**:
```bash
# Copy to project root
cp sample.env ../.env

# Edit with your OpenCTI credentials
nano ../.env
```

### `test.env`
Example configuration for testing environments.

**Usage**:
```bash
# Use for testing
cp test.env ../.env
# Update with test instance credentials
```

## Environment Variables

### Required
- `OPENCTI_URL`: Your OpenCTI instance URL
- `OPENCTI_TOKEN`: API authentication token

### Optional
- `OPENCTI_VERIFY_SSL`: Enable/disable SSL verification (default: `true`)
- `OPENCTI_TIMEOUT`: Request timeout in seconds (default: `30`)
- `VIRUSTOTAL_CONNECTOR_ID`: Connector ID for VirusTotal enrichment

## Quick Setup

```bash
# 1. Copy sample configuration
cp examples/sample.env .env

# 2. Edit configuration
# Replace placeholders with your actual values:
#   - OPENCTI_URL=https://your-opencti-instance.com
#   - OPENCTI_TOKEN=your_api_token_here

# 3. Test connection
python -m opencti_mcp.server
```

## Security Notes

- **Never commit `.env` files** to version control
- **Rotate API tokens** regularly
- **Use read-only tokens** when possible
- **Enable SSL verification** in production

## Getting API Token

1. Log in to your OpenCTI instance
2. Go to **Profile** → **Settings**
3. Navigate to **API Access**
4. Generate a new token with appropriate permissions
5. Copy the token to your `.env` file

## Testing Configuration

```bash
# Test OpenCTI connectivity
curl -H "Authorization: Bearer YOUR_TOKEN" \
     https://your-opencti.example.com/graphql \
     -d '{"query": "{ about { version } }"}'

# Should return OpenCTI version information
```

## Common Issues

### SSL Certificate Errors
```bash
# For testing only (not recommended for production)
OPENCTI_VERIFY_SSL=false
```

### Connection Timeouts
```bash
# Increase timeout for slow networks
OPENCTI_TIMEOUT=60
```

### Invalid Token
- Verify token is correct
- Check token hasn't expired
- Ensure token has sufficient permissions

## Additional Resources

- [OpenCTI Documentation](https://docs.opencti.io/)
- [Project README](../README.md)
- [Developer Guide](../docs/CLAUDE.MD)
