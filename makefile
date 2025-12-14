COMMAND = python3 manage.py
DOCKER = docker compose 

.PHONY: up

.PHONY: pre-commit
pre-commit:
	@echo running black
	@black .
	@echo running isort
	@isort .

.PHONY: migrations
migrations:
	${COMMAND} makemigrations

.PHONY: migrate
migrate:
	${COMMAND} migrate


.PHONY: run
run:
	${COMMAND} runserver

.PHONY: db
db:
	${DOCKER} up -d db
