.PHONY: pre-commit
pre-commit:
	@echo running black
	@black .
	@echo running isort
	@isort .
	@echo running flake8
	@flake8 --max-line-length 91

.PHONY: database
database:
	@make migrations
	@make migrate

.PHONY: run
run:
	@python3 manage.py runserver