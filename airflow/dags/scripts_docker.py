
from airflow import DAG
from datetime import timedelta
from airflow.operators.docker_operator import DockerOperator
import logging
from airflow.utils.dates import days_ago


def on_failure_callback(context):
    """
    Callback function to handle task failures.

    Parameters:
        - context (Dict[str, Any]): Context information about the failed task.
    """
    logging.error(
        f"Task {context['task_instance'].task_id} failed. Handling error...")


CONFIG = {
    "dag_docker_image_name": "import_dag",
    "airflow": {
        "owner": "airflow",
        "retries": 2,
        "retry_delay": {"minutes": 5},
        "schedule_interval": timedelta(hours=24)
    },
    "scripts": {
        "csv_file_path": "src/data/data.csv",
        "zip_file_path": "src/data/data.zip",
        "json_file_path": "src/data/data.json",
        "batch_size": 100
    }
}

# Define DAG and tasks
config_args = {
    'owner': CONFIG['airflow'].get('owner'),
    'retries': CONFIG['airflow'].get('retries'),
    'retry_delay': timedelta(minutes=CONFIG['airflow'].get('retry_delay', {}).get('minutes', 5)),
    'schedule_interval': CONFIG['airflow'].get('schedule_interval', timedelta(hours=1)),
}

dag = DAG(
    'test1',
    start_date=days_ago(1),
    default_args=config_args,
    description='import to database raw data',
    # schedule_interval=config_args['schedule_interval'],
)

# the environment variables
CSV_FILE_PATH = CONFIG['scripts'].get('csv_file_path')
ZIP_FILE_PATH = CONFIG['scripts'].get('zip_file_path')
JSON_FILE_PATH = CONFIG['scripts'].get('json_file_path')
BATCH_SIZE = CONFIG['airflow'].get('batch_size')

# Docker image for your scripts
SCRIPTS_IMAGE = CONFIG['dag_docker_image_name']

# DockerOperator for unzip task
unzip_task = DockerOperator(
    task_id='unzip',
    image=SCRIPTS_IMAGE,
    network_mode='airflow_default',
    command='poetry run pipeline unzip',
    dag=dag,
)

# DockerOperator for convert_to_json task
convert_to_json_task = DockerOperator(
    task_id='convert_to_json',
    network_mode='airflow_default',
    image=SCRIPTS_IMAGE,
    command='poetry run pipeline csv_to_json',
    dag=dag,
)

# DockerOperator for load_to_db task
load_to_db_task = DockerOperator(
    task_id='load_to_db',
    network_mode='airflow_default',
    image=SCRIPTS_IMAGE,
    command='poetry run pipeline json_to_db',
    dag=dag,
)

# DockerOperator for call_procedure task
call_procedure_task = DockerOperator(
    task_id='call_procedure',
    network_mode='airflow_default',
    image=SCRIPTS_IMAGE,
    command='poetry run pipeline call_procedure',
    dag=dag,
)

# Set up task dependencies
unzip_task >> convert_to_json_task >> load_to_db_task >> call_procedure_task
