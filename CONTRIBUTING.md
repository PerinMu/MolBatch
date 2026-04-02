# Contributing

Thank you for considering a contribution.

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e .[dev]
```

## Run tests

```bash
pytest
```

## Style guidelines

- Keep core logic backend-agnostic where possible.
- Put viewer-specific command rendering inside backend modules.
- Add tests for every new config option or planning rule.
- Update documentation when public behavior changes.

## Pull requests

1. Create a feature branch.
2. Add or update tests.
3. Update `CHANGELOG.md`.
4. Open a pull request.
