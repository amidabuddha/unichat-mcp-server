# Unichat MCP Server in Python
Also available in [TypeScript](https://github.com/amidabuddha/unichat-ts-mcp-server)
[![smithery badge](https://smithery.ai/badge/unichat-mcp-server)](https://smithery.ai/server/unichat-mcp-server)
--
Send requests to OpenAI, MistralAI, Anthropic, xAI, or Google AI using MCP protocol via tool or predefined prompts.
Vendor API key required

### Tools

The server implements one tool:
- `unichat`: Send a request to unichat
  - Takes "messages" as required string arguments
  - Returns a response

### Prompts

- `code_review`
  - Review code for best practices, potential issues, and improvements
  - Arguments:
    - `code` (string, required): The code to review"
- `document_code`
  - Generate documentation for code including docstrings and comments
  - Arguments:
    - `code` (string, required): The code to comment"
- `explain_code`
  - Explain how a piece of code works in detail
  - Arguments:
    - `code` (string, required): The code to explain"
- `code_rework`
  - Apply requested changes to the provided code
  - Arguments:
    - `changes` (string, optional): The changes to apply"
    - `code` (string, required): The code to rework"

## Quickstart

### Install

#### Claude Desktop

On MacOS: `~/Library/Application\ Support/Claude/claude_desktop_config.json`
On Windows: `%APPDATA%/Claude/claude_desktop_config.json`

Development/Unpublished Servers Configuration
```json
"mcpServers": {
  "unichat-mcp-server": {
    "command": "uv",
    "args": [
      "--directory",
      "{{your source code local directory}}/unichat-mcp-server",
      "run",
      "unichat-mcp-server"
    ],
    "env": {
      "UNICHAT_MODEL": "SELECTED_UNICHAT_MODEL",
      "UNICHAT_API_KEY": "YOUR_UNICHAT_API_KEY"
    }
  }
}
```

Published Servers Configuration
```json
"mcpServers": {
  "unichat-mcp-server": {
    "command": "uvx",
    "args": [
      "unichat-mcp-server"
    ],
    "env": {
      "UNICHAT_MODEL": "SELECTED_UNICHAT_MODEL",
      "UNICHAT_API_KEY": "YOUR_UNICHAT_API_KEY"
    }
  }
}
```

### Installing via Smithery

To install Unichat for Claude Desktop automatically via [Smithery](https://smithery.ai/server/unichat-mcp-server):

```bash
npx -y @smithery/cli install unichat-mcp-server --client claude
```

## Development

### Building and Publishing

To prepare the package for distribution:

1. Sync dependencies and update lockfile:
```bash
uv sync
```

2. Build package distributions:
```bash
uv build
```

This will create source and wheel distributions in the `dist/` directory.

3. Publish to PyPI:
```bash
uv publish --token {{YOUR_PYPI_API_TOKEN}}
```

### Debugging

Since MCP servers run over stdio, debugging can be challenging. For the best debugging
experience, we strongly recommend using the [MCP Inspector](https://github.com/modelcontextprotocol/inspector).


You can launch the MCP Inspector via [`npm`](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) with this command:

```bash
npx @modelcontextprotocol/inspector uv --directory {{your source code local directory}}/unichat-mcp-server run unichat-mcp-server
```


Upon launching, the Inspector will display a URL that you can access in your browser to begin debugging.
