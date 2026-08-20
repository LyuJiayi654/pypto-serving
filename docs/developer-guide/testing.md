# Testing

Run host-side unit tests and lint checks before sending documentation or code
changes.

## Unit Tests

```bash
python -m pytest tests/unit
```

## Lint Checks

```bash
python tests/lint/check_headers.py
python tests/lint/check_english_only.py
ruff check --config ruff.toml .
```

## Documentation Build

```bash
python -m pip install -r docs/requirements.txt
mkdocs build --strict
```

## NPU Validation

Use the model examples for device validation. Keep environment variables from a
known-good runtime unless the test is specifically about changing them.
