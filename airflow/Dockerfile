FROM apache/airflow:latest-python3.11

WORKDIR /opt/airflow

USER root

RUN apt-get update \
  && apt-get -y install libpq-dev gcc \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

USER airflow 

COPY pyproject.toml poetry.lock /opt/airflow/

RUN pip install poetry 


RUN poetry install --no-root

COPY . /opt/airflow

RUN airflow db init

CMD ["airflow", "dags", "trigger", "import_dag"]
