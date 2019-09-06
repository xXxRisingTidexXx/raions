# colors
GREEN = $(shell tput -Txterm setaf 2)
YELLOW = $(shell tput -Txterm setaf 3)
WHITE = $(shell tput -Txterm setaf 7)
RESET = $(shell tput -Txterm sgr0)
GRAY = $(shell tput -Txterm setaf 6)
TARGET_MAX_CHAR_NUM = 25
YAMJAM_PATH = "~/.yamjam/config.yaml"
TESTING_DATABASE = traions

.PHONY: autogenerate-migrations migrate test-reapy test-agony collect-static \
	run-reapy-manage run-reapy-schedule run-agony-dev help


# Configuration

## Edit & lint YamJam configuration
yamjam:
	@( \
		cd ./agony/; \
		source ./venv/bin/activate; \
		nano ${YAMJAM_PATH}; \
		yjlint ${YAMJAM_PATH}; \
		deactivate; \
		cd ../; \
	)


# Migrations

## Automatically generate migrations
autogenerate-migrations:
	@( \
		cd ./agony/; \
		source ./venv/bin/activate; \
		./manage.py makemigrations; \
		deactivate; \
		cd ../; \
	)

## Migrate all databases
migrate:
	@( \
		cd ./agony/; \
		source ./venv/bin/activate; \
		printf "\ndefault is being migrated...\n"; \
		./manage.py migrate; \
		printf "\n${TESTING_DATABASE} is being migrated...\n"; \
		./manage.py migrate --database=${TESTING_DATABASE}; \
		deactivate; \
		cd ../; \
	)


# Tests

## Run reapy's pytest.
test-reapy:
	@( \
		cd ./reapy/; \
		source ./venv/bin/activate; \
		pytest -q -x --timeout=5 ./tests/; \
		deactivate; \
		cd ../; \
	)

## Run agony's unittest.
test-agony:
	@( \
		cd ./agony/; \
		source ./venv/bin/activate; \
		printf "\nDirect test chain\'s started\n\n"; \
		./manage.py test; \
		printf "\nReverse test chain\'s started\n\n"; \
		./manage.py test --reverse; \
		deactivate; \
		cd ../; \
	)


# Static files

## Collects static files into single directory
collect-static:
	@( \
		cd ./agony/; \
		source ./venv/bin/activate; \
		./manage.py collectstatic; \
		deactivate; \
		cd ../; \
	)


# Run

## Run single reapy's worker
run-reapy-manage:
	@( \
		cd ./reapy/; \
		source ./venv/bin/activate; \
		printf "\nEnter worker name: "; \
		read WORKER; \
		./manage.py ${WORKER}; \
		deactivate; \
		cd ../; \
	)

## Run the whole reapy's schedule
run-reapy-schedule:
	@( \
		cd ./reapy/; \
		source ./venv/bin/activate; \
		./schedule.py; \
		deactivate; \
		cd ../; \
	)

## Run agony's dev server
run-agony-dev:  # TODO here we need to explicitly set DEBUG to True
	@( \
		cd ./agony/; \
		source ./venv/bin/activate; \
		./manage.py runserver; \
		deactivate; \
		cd ../; \
	)


# Help

## Show help.
help:
	@echo ''
	@echo 'Usage:'
	@echo ''
	@echo '  ${YELLOW}make${RESET} ${GREEN}<target>${RESET}'
	@echo ''
	@echo 'Targets:'
	@awk '/^[a-zA-Z\-]+:/ { \
		helpMessage = match(lastLine, /^## (.*)/); \
		if (helpMessage) { \
		    if (index(lastLine, "|") != 0) { \
				stage = substr(lastLine, index(lastLine, "|") + 1); \
				printf "\n ${GRAY}%s: \n\n", stage;  \
			} \
			helpCommand = substr($$1, 0, index($$1, ":")-1); \
			helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
			if (index(lastLine, "|") != 0) { \
				helpMessage = substr(helpMessage, 0, index(helpMessage, "|")-1); \
			} \
			printf "  ${YELLOW}%-$(TARGET_MAX_CHAR_NUM)s${RESET} ${GREEN}%s${RESET}\n", helpCommand, helpMessage; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST)
	@echo ''
