# Installation and development

This is the authoritative setup guide for the current repository. Commands below match the checked-in entry point, dependency files, project configuration, and setup scripts.

## Prerequisites

- Git.
- Python 3.10 or later. This minimum is declared by `pyproject.toml`; the documentation review successfully ran tests on Python 3.14.4, but did not test every declared Python version.
- `pip`, or optionally [uv](https://docs.astral.sh/uv/).

## Clone

```bash
git clone https://github.com/iconata/Turn-based-WoW.git
cd Turn-based-WoW
```

The `local-state` command selects the source branch documented by this snapshot. If it has already been merged or removed, use the repository's current default branch instead.

## Virtual environment

With the standard library:

```bash
python -m venv .venv
source .venv/bin/activate
```

With uv:

```bash
uv venv
source .venv/bin/activate
```

On Windows PowerShell, activate either environment with:

```powershell
.\.venv\Scripts\Activate.ps1
```

## Install runtime dependencies

The game currently uses only the Python standard library, so no third-party runtime package is required. Note that the current `requirements.txt` also lists development tools despite its “Core dependencies” comment:

```bash
python -m pip install -r requirements.txt
```

Or with uv:

```bash
uv pip install -r requirements.txt
```

## Install development dependencies

```bash
python -m pip install -r requirements-dev.txt
```

Or:

```bash
uv pip install -r requirements-dev.txt
```

The current project metadata also declares a `dev` extra, but editable/package installation should be treated cautiously until packaging is verified from a clean checkout.

## Run game

```bash
python main.py
```

Information-only commands:

```bash
python main.py --show-classes
python main.py --show-roles
```

## Run tests

Use module invocation from the repository root:

```bash
python -m pytest
```

Latest recorded local run: 79 tests passed. During this review, bare `pytest` failed import collection in the active environment while `python -m pytest` passed, so the module form is the documented command. Passing tests do not prove that game rules are correct.

## Run coverage

```bash
python -m pytest --cov=. --cov-report=term-missing
```

Coverage was not run during this documentation task.

## Run Ruff

```bash
ruff check .
```

Ruff is configured in `pyproject.toml`. It was run during this review and currently reports 107 errors; a clean lint run remains planned work. Use `--fix` only when intentionally performing a separate code-change task.

## Windows PowerShell setup

The checked-in script performs these operations: checks for uv, offers to install it, creates `.venv`, activates it, installs `requirements.txt`, and runs `pytest -q`.

```powershell
.\setup.ps1
```

The script was inspected but not executed during this review. Because it invokes bare `pytest`, its verification step may encounter the import-path issue observed in the current macOS environment.

For a manual PowerShell setup:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
python -m pytest
python main.py
```

## macOS/Linux setup

The checked-in script performs these operations: checks for uv, offers to install it with `curl`, creates `.venv`, activates it, installs `requirements.txt`, and runs `pytest -q`.

```bash
./setup.sh
```

The script was inspected but not executed during this review. It downloads uv when missing, and its bare `pytest` verification may encounter the import-path issue observed during this task.

For a manual setup:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pytest
python main.py
```

## Troubleshooting

### Local modules are not found during test collection

Run tests from the repository root with:

```bash
python -m pytest
```

This avoids the import-path failure observed with the bare `pytest` executable in the review environment.

### `uv` is not found

Either install uv using its official instructions or use the standard-library `venv` and `pip` commands above. Restart the shell after installing uv if its executable is not yet on `PATH`.

### PowerShell blocks activation

Use an execution policy appropriate for your environment, or invoke the virtual environment's Python directly:

```powershell
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe main.py
```

### Ruff fails

The current snapshot has known lint findings. A Ruff failure is not necessarily an installation failure; fixing it is separate planned work.
