# Repository instructions

## Closure and clean-up

This MCP server reaches users through PyPI; nothing is installed locally from this checkout. When a change is complete:

1. Check that it still starts or imports (`uv run python -c "import unichat_mcp_server"`), then commit locally.
2. Remove reproducible leftovers: `.venv/`, `__pycache__/`, `build/`, `dist/` and `*.egg-info/`. Keep `uv.lock`.

For documentation-only changes to repository instructions, review the diff and commit locally; no version bump, dependency installation, build or test run is needed.

## Releases

- A push to `main` that changes `pyproject.toml` triggers `.github/workflows/publish.yml`, which publishes to PyPI. Change the version, or anything else in `pyproject.toml`, only when Stefan explicitly asks for a release.
- If a published release is broken, violates its compatibility guarantees or contains a security vulnerability, yank the affected release after verifying that the fixed version is available on PyPI. Use the authenticated release-management page at `https://pypi.org/manage/project/unichat-mcp-server/releases/` and give a reason naming the defect and the fixed version to upgrade to. Follow [PyPI's yanking guidance](https://docs.pypi.org/project-management/yanking/); preserve the release files and do not yank older releases merely because they have been superseded.
- Verify the affected release through `https://pypi.org/pypi/unichat-mcp-server/<affected-version>/json`: its nonempty `urls` list must show `yanked: true` and the intended `yanked_reason` for every file. Publishing through CI does not establish an authenticated maintainer session for yanking. If authentication blocks it, report the exact versions still pending and do not claim yanking is complete.

## Git workflow

- Commit locally as work progresses. Push only when Stefan asks; when a milestone is done, ask once whether to push now or not yet.
- Use plain `git` on `main`. Create branches or pull requests only when asked.
