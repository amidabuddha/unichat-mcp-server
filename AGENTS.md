# Repository instructions

## Closure and clean-up

This MCP server reaches users through PyPI; nothing is installed locally from this checkout. When a change is complete:

1. Check that it still starts or imports (`uv run python -c "import unichat_mcp_server"`), then commit locally.
2. Remove reproducible leftovers: `.venv/`, `__pycache__/`, `build/`, `dist/` and `*.egg-info/`. Keep `uv.lock`.

## Releases

- A push to `main` that changes `pyproject.toml` triggers `.github/workflows/publish.yml`, which publishes to PyPI. Change the version, or anything else in `pyproject.toml`, only when Stefan explicitly asks for a release.

## Git workflow

- Commit locally as work progresses. Push only when Stefan asks; when a milestone is done, ask once whether to push now or not yet.
- Use plain `git` on `main`. Create branches or pull requests only when asked.
