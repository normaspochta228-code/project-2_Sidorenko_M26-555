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

make lint:
	poetry run ruff check .

make lint-fix:
	poetry run ruff check . --fix



