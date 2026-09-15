# Unichat MCP Server in Python
Also available in [TypeScript](https://github.com/amidabuddha/unichat-ts-mcp-server)
--
 <h4 align="center">
  <a href="https://mseep.ai/app/amidabuddha-unichat-mcp-server">
  <img src="https://mseep.net/pr/amidabuddha-unichat-mcp-server-badge.png" alt="MseeP.ai Security Assessment Badge" />
  </a>
 </h4>
  <h4 align="center">
  <a href="https://github.com/amidabuddha/unichat-mcp-server/blob/main/LICENSE.md">
  <img src="https://img.shields.io/github/license/amidabuddha/unichat-mcp-server" alt="Released under the MIT license." />
  </a>
  <a href="https://archestra.ai/mcp-catalog/amidabuddha__unichat-mcp-server">
    <img src="https://archestra.ai/mcp-catalog/api/badge/quality/amidabuddha/unichat-mcp-server" alt="Trust Score" />
  </a>
  <a href="https://smithery.ai/server/unichat-mcp-server">
    <img src="https://smithery.ai/badge/unichat-mcp-server" alt="Smithery Server Installations" />
  </a>
</h4>
 <h4 align="center">
  <a href="https://mcphub.com/mcp-servers/amidabuddha/unichat-mcp-server">
  <img src="https://img.mcphub.com/_next/image?url=%2Flogo-dark.png&w=48&q=75" alt="Hosted at MCPHub" />
  </a>
 </h4>

Send requests to OpenAI, Anthropic, and OpenAI-compatible providers using MCP protocol via tool or predefined prompts. For OpenAI-compatible providers such as MistralAI, xAI, Google AI, DeepSeek, Alibaba, or Inception, set `UNICHAT_BASE_URL` to the provider's compatible API endpoint.
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

**Supported Models:**
> A list of currently supported models to be used as `"SELECTED_UNICHAT_MODEL"` may be found [here](https://github.com/amidabuddha/unichat/blob/main/unichat/models.py). Please make sure to add the relevant vendor API key as `"YOUR_UNICHAT_API_KEY"`

**Example:**
```json
"env": {
  "UNICHAT_MODEL": "gpt-5.4-mini",
  "UNICHAT_API_KEY": "YOUR_OPENAI_API_KEY"
}
```

For OpenAI-compatible providers with custom endpoints:
```json
"env": {
  "UNICHAT_MODEL": "PROVIDER_MODEL",
  "UNICHAT_API_KEY": "YOUR_PROVIDER_API_KEY",
  "UNICHAT_BASE_URL": "https://provider.example.com/v1"
}
```

When `UNICHAT_BASE_URL` is set, the server accepts the configured `UNICHAT_MODEL` without checking it against Unichat's built-in model list.

Development/Unpublished Servers Configuration
```json
"mcpServers": {
  "unichat-mcp-server": {
    "command": "uv",
    "args": [
      "--directory",
      "{{your source code local directory}}/unichat-mcp-server",
      "run",
      "--locked",
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

### Clean installation from source

Prerequisites: Git, Python 3.11 or newer (as declared in `pyproject.toml`), and `uv` available on your PATH. Node.js/npm is only needed for the optional MCP Inspector below. The shell examples use Bash/Zsh syntax.

Clone the repository and restore its locked dependencies:

```bash
git clone https://github.com/amidabuddha/unichat-mcp-server.git
cd unichat-mcp-server
uv sync --locked
```

`uv sync --locked` creates the project-local `.venv/`, installs the project in editable mode and restores dependencies from `uv.lock`. It fails if the lockfile needs updating instead of silently changing it. No virtual-environment activation or global Python dependency installation is required when using `uv run`.

Set the same environment variables used in the Claude Desktop examples, replacing the placeholders with your provider's values:

```bash
export UNICHAT_MODEL="SELECTED_UNICHAT_MODEL"
export UNICHAT_API_KEY="YOUR_UNICHAT_API_KEY"
# Optional, for an OpenAI-compatible provider with a custom endpoint:
# export UNICHAT_BASE_URL="https://provider.example.com/v1"
```

The server reads environment variables; it does not load `.env` files itself. For Claude Desktop, keep these values in the server's `env` configuration shown above.

Run the local server:

```bash
uv run --locked unichat-mcp-server
```

This is a stdio MCP server: connect through Claude Desktop or the Inspector below to interact with it. It does not start a web page or an interactive chat prompt. The editable installation is sufficient to run it; to also create source and wheel distributions using the configured Hatchling backend:

```bash
uv build
```

Packages are written to `dist/`. `uv build` supplies the build backend in an isolated environment; a globally installed `build` frontend is unnecessary. Runtime dependencies are locked by `uv.lock`, but the `hatchling` build requirement is not version-pinned in `pyproject.toml`.

### Normal development

After editing files under `src/`, restart the server or reconnect it in your MCP client:

```bash
uv run --locked unichat-mcp-server
```

The editable installation uses the current source. Ordinary source changes do not require deleting `.venv/`, reinstalling dependencies or rebuilding distribution packages. Run `uv build` again only when you need updated package artifacts. After pulling changes to the dependency manifest and lockfile, run `uv sync --locked` to update the environment to match them.

This repository has no configured automated test suite or watch command. Use the Inspector below to manually exercise tools and prompts, restarting the server after changes.

### Clean rebuild of an existing checkout

Stop the running server and run these commands from the repository root (the directory containing `pyproject.toml` and `uv.lock`). These paths assume uv's default project-local environment: `.venv/` contains installed dependencies and the editable project, and `dist/` contains generated source/wheel archives.

```bash
rm -rf .venv dist
uv sync --locked
uv build
```

This recreates the environment and distribution packages. Keep `uv.lock`, source, configuration, `.env` files and user data. Other ignored names such as `build/` and `wheels/` are not established outputs of this project's build workflow and are not cleanup targets. Global uv caches and Python installations can be reused. To run again, retain or reapply the environment variables above and use `uv run --locked unichat-mcp-server`.

### Intentional dependency updates

Dependency updates are separate from restoration. When deliberately changing requirements in `pyproject.toml`, run `uv lock` and review the resulting `uv.lock` changes, then run `uv sync --locked`. To deliberately upgrade an existing dependency within its declared constraints, for example:

```bash
uv lock --upgrade-package unichat
uv sync --locked
```

Review the lockfile changes and check server behavior before accepting the update. Routine installation and rebuilding should use the existing lockfile.

### Publishing

Publishing is a separate maintainer action and is not part of local installation or rebuilding. Prepare fresh distributions with the clean-rebuild workflow above and verify that `dist/` contains only the intended release before uploading to PyPI:

```bash
uv publish --token "YOUR_PYPI_API_TOKEN"
```

The repository also has a publishing workflow in `.github/workflows/publish.yml`, triggered by changes to `pyproject.toml` on `main` or manual dispatch.

### Debugging

Since MCP servers run over stdio, debugging can be challenging. For the best debugging
experience, we strongly recommend using the [MCP Inspector](https://github.com/modelcontextprotocol/inspector).


You can launch the MCP Inspector via [`npm`](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) with this command:

```bash
npx @modelcontextprotocol/inspector uv --directory "/path/to/unichat-mcp-server" run --locked unichat-mcp-server
```


Upon launching, the Inspector will display a URL that you can access in your browser to begin debugging.

## Hosted deployment

A hosted deployment is available on [Fronteir AI](https://fronteir.ai/mcp/amidabuddha-unichat-mcp-server).
