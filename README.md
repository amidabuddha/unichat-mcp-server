# unichat-mcp-server MCP server

Unichat MCP Server

### Tools

The server implements one tool:
- unichat: Send a request to unichat
  - Takes "messages" as required string arguments
  - Returns a response


## Quickstart

### Install

#### Claude Desktop

On MacOS: `~/Library/Application\ Support/Claude/claude_desktop_config.json`
On Windows: `%APPDATA%/Claude/claude_desktop_config.json`

<details>
  <summary>Development/Unpublished Servers Configuration</summary>
  ```
  "mcpServers": {
    "unichat-mcp-server": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/stefan/Documents/Playground/OpenAI/unichat-mcp-server",
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
</details>

<details>
  <summary>Published Servers Configuration</summary>
  ```
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
</details>

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
npx @modelcontextprotocol/inspector uv --directory /Users/stefan/Documents/Playground/OpenAI/unichat-mcp-server run unichat-mcp-server
```


Upon launching, the Inspector will display a URL that you can access in your browser to begin debugging.