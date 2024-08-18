
In case you want to develop new features on this package, run:

```shell
pip install -e . # (Which will incldue the dev dependendencies)
pre-commit install # More info here: https://github.com/pre-commit/pre-commit
pre-commit install --hook-type commit-msg
```

After a commit you should:

```shell
# Apply black formatting (or add an extension in VSCode/Pycharm for ease of use)
black .

# See if ruff complains about anything
ruff check . --output-format=concise

# Run all the tests
pytest -n auto --disable-pytest-warnings
```

If you want to go the extra mile:

```shell
# Pump that coverage up!
pytest --cov-report xml:cov.xml --cov=lhf -n auto --disable-pytest-warnings
coverage report -m

# Run mypy to lint typing problems
mypy lhf/llmtools
```
