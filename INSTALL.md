# Installation and development

This is the authoritative setup guide for the preserved repository. Dependencies are declared in `pyproject.toml` and locked in `uv.lock`.

## Prerequisites

- Git.
- [uv](https://docs.astral.sh/uv/).
- Python 3.10 through 3.15, as declared in `pyproject.toml`. The latest documented local verification used Python 3.14.4; the full declared range was not tested locally.

## Clone

```bash
git clone https://github.com/iconata/Turn-based-WoW.git
cd Turn-based-WoW
git switch local-state
```

If `local-state` is no longer available, use the repository's current default branch.

## Set up the environment

From the repository root, create or update the uv-managed environment and install the locked development dependencies:

```bash
uv sync --extra dev
```

This installs the `dev` extra declared in `pyproject.toml`, including pytest, pytest-cov, and Ruff. Package or editable installation has not been verified and is not required for these commands.

## Run the game

```bash
uv run python -m turn_based_wow
```

Information-only commands:

```bash
uv run python -m turn_based_wow --show-classes
uv run python -m turn_based_wow --show-roles
```

## Run tests

```bash
uv run python -m pytest
```

Latest verified local run: 80 tests passed on Python 3.14.4. Passing tests characterize covered behavior; they do not prove that every gameplay rule is correct.

## Run coverage

```bash
uv run python -m pytest --cov=. --cov-report=term-missing
```

Coverage was not run during the final documentation update.

## Run Ruff

```bash
uv run ruff check .
```

Ruff is configured in `pyproject.toml`. The latest recorded full-repository run reported 107 findings; the preserved snapshot is not lint-clean.

## Setup scripts

The checked-in `setup.sh` and `setup.ps1` scripts are stale: both still attempt to install from the removed `requirements.txt` file and then invoke bare `pytest`. They are not recommended without modification. Neither script was executed end to end during the repository review.

Use the direct uv commands above on macOS, Linux, or Windows PowerShell:

```text
uv sync --extra dev
uv run python -m pytest
uv run python -m turn_based_wow
```

## Troubleshooting

### Local modules are not found during test collection

Run pytest through uv and Python's module invocation from the repository root:

```bash
uv run python -m pytest
```

### `uv` is not found

Install uv using its official instructions, then restart the shell if the executable is not yet on `PATH`.

### Ruff fails

The preserved snapshot has known lint findings. A Ruff failure is not necessarily an installation failure.
