FROM python:3.9-slim-buster as builder
RUN apt-get update \
    && apt-get install gcc make -y \
    && apt-get clean
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --no-warn-script-location --user -r requirements.txt
COPY modern_catalog/ modern_catalog/
COPY manage.py . 


FROM python:3.9-slim-buster as test
COPY --from=builder /root/.local /root/.local
COPY --from=builder /app/modern_catalog /app/modern_catalog
COPY --from=builder /app/manage.py /app/manage.py
WORKDIR /app
COPY requirements-test.txt .
RUN pip install -r requirements-test.txt
ENV PATH=/root/.local/bin:$PATH
ENV DJANGO_ENVIRONMENT=test
RUN python manage.py test --keepdb


FROM python:3.9-slim-buster as final
COPY --from=builder /root/.local /root/.local
COPY --from=builder /app/modern_catalog /app/modern_catalog
COPY --from=builder /app/manage.py /app/manage.py
WORKDIR /app
EXPOSE 8000
ENV PATH=/root/.local/bin:$PATH
# ENTRYPOINT gunicorn modern_catalog.asgi:application -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
ENTRYPOINT gunicorn modern_catalog.asgi:application -w 4 -k uvicorn.workers.UvicornWorker

