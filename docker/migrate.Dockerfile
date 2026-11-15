# Migration service: standard library only, so no pip install needed.
FROM python:3.12-slim
WORKDIR /code
COPY app/ app/
COPY migrate/ migrate/
COPY seed/ seed/
ENV DB_PATH=/data/students.db
CMD ["python", "-m", "migrate.migrate"]
