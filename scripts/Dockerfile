FROM python:3.11

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN pip install poetry

COPY . /app/

RUN poetry install

# Set script variables
ENV JSON_FILE_PATH "data/data.json"
ENV CSV_FILE_PATH "data/data.csv"
ENV ZIP_FILE_PATH "data/data.zip"  

# Database variables , in production we would use a secret file of course.
ENV DB_HOST "db"
ENV DB_DATABASE "production"
ENV DB_USER "user"
ENV DB_PASSWORD "pwd"


ENTRYPOINT ["poetry", "run", "pipeline"]
