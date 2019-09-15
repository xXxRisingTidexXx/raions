# colors
GREEN = $(shell tput -Txterm setaf 2)
YELLOW = $(shell tput -Txterm setaf 3)
WHITE = $(shell tput -Txterm setaf 7)
RESET = $(shell tput -Txterm sgr0)
GRAY = $(shell tput -Txterm setaf 6)
TARGET_MAX_CHAR_NUM = 25

.PHONY: autogenerate-migrations generate-data-migrations migrate test-agony \
	test-reapy run-agony-dev run-reapy-manage run-reapy-schedule help


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

## Generate data migrations
generate-data-migrations:
	@( \
		cd ./agony/; \
		source ./venv/bin/activate; \
		./manage.py makemigrations --empty core; \
		deactivate; \
		cd ../; \
	)

## Migrate all databases
migrate:
	@( \
		cd ./agony/; \
		source ./venv/bin/activate; \
		./manage.py migrate; \
		echo ""; \
		./manage.py migrate --database=testing; \
		deactivate; \
		cd ../; \
	)


# Tests

## Run agony's unittest.
test-agony:
	@( \
		cd ./agony/; \
		source ./venv/bin/activate; \
		./manage.py test; \
		echo ""; \
		./manage.py test --reverse; \
		deactivate; \
		cd ../; \
	)

## Run reapy's pytest.
test-reapy:
	@( \
		cd ./reapy/; \
		source ./venv/bin/activate; \
		pytest -q -x --timeout=5 ./tests/; \
		deactivate; \
		cd ../; \
	)


# Run

## Run agony's dev server
run-agony-dev:
	@( \
		cd ./agony/; \
		source ./venv/bin/activate; \
		AGONY_DEBUG=True ./manage.py runserver; \
		deactivate; \
		cd ../; \
	)

## Run www.olx.ua flat reaper
run-olx-flat-reaper:
	@( \
		cd ./reapy/; \
		source ./venv/bin/activate; \
		./manage.py OlxFlatReaper; \
		deactivate; \
		cd ../; \
	)

## Run dom.ria.com flat reaper
run-dom-ria-flat-reaper:
	@( \
		cd ./reapy/; \
		source ./venv/bin/activate; \
		./manage.py DomRiaFlatReaper; \
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


# Help

## Show help.
help:
	@echo ''
	@echo 'Usage:'
	@echo ''
	@echo '  ${YELLOW}make${RESET} ${GREEN}<target>${RESET}'
	@echo ''
	@echo 'Targets:'
	@echo ''
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
