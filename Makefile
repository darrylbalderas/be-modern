list:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

dev-init:
	@echo "--> Start database"
	@docker-compose up -d --remove-orphans --build
	@echo "--> Waiting for database to spin up"
	@sleep 1
	@echo "--> Setting up migrations"
	@python manage.py makemigrations
	@echo "--> Applying migrations"
	@python manage.py migrate
	@echo "--> Upload seed data"
	@python manage.py loaddata programs
dev-start:
	@make dev-init
	@docker logs test-be
dev-stop:
	@echo "--> Stop and delete database"
	@docker-compose down --remove-orphans -v
	# @docker container rm -f $$(docker ps -aqf "name=test-be") || echo "test-be container does not exist"
unittest:
	@export DJANGO_ENVIRONMENT=test
	@flake8 --max-line-length=88
	@python manage.py test

