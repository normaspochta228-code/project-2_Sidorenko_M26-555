install:
	poetry install

project:
	poetry run project

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	powershell -Command "pip install (Get-Item dist/*.whl).FullName"

lint:
	poetry run ruff check .

lint-fix:
	poetry run ruff check . --fix
