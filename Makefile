list:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

dev-start:
	@docker-compose up -d --remove-orphans --build
	@python manage.py loaddata programs
	@gunicorn modern_catalog.asgi:application -w 4 -k uvicorn.workers.UvicornWorker
dev-stop:
	@docker-compose  --remove-orphans -v