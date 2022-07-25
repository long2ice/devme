checkfiles = devme/ tests/ conftest.py
py_warn = PYTHONDEVMODE=1

up:
	@poetry update

deps: 
	@poetry install

style: deps
	@isort -src $(checkfiles)
	@black $(checkfiles)

check: deps
	@black --check $(checkfiles)
	@pflake8 $(checkfiles)
	@mypy $(checkfiles)

test: deps
	$(py_warn) pytest

ci: check
