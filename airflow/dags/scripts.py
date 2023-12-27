from pendulum import duration
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import logging
import json
from airflow.utils.dates import days_ago

CONFIG_FILE_PATH = './dags/dag_config.json'


def on_failure_callback(context):
    """
    Callback function to handle task failures.

    Parameters:
        - context (Dict[str, Any]): Context information about the failed task.
    """
    logging.error(
        f"Task {context['task_instance'].task_id} failed. Handling error...")


def get_config():
    """
    Retrieve configurations from the configuration file.

    Returns:
        Tuple[Dict[str, Any], Dict[str, Any]]: Tuple containing the airflow and scripts configurations.
    """
    try:
        # Read configuration from the file
        with open(CONFIG_FILE_PATH, 'r') as config_file:
            config = json.load(config_file)

        # Retrieve configurations from the loaded dictionary
        config_airflow = config.get('airflow', {})
        config_scripts = config.get('scripts', {})
    except FileNotFoundError as e:
        logging.error(f"Configuration file not found: {CONFIG_FILE_PATH}")
        raise e
    except Exception as e:
        logging.error(f"Error loading configuration: {e}")
        raise e

    return config_airflow, config_scripts


# Retrieve configurations
config_airflow, config_scripts = get_config()

# Define DAG and tasks
config_args = {
    'owner': config_airflow.get('owner'),
    'retries': config_airflow.get('retries'),
    'retry_delay': duration(**config_airflow.get('retry_delay', {})),
    'on_failure_callback': on_failure_callback,
    'schedule_interval': duration(**config_airflow.get('schedule_interval', {})),
}

dag = DAG(
    'import_dag',
    start_date=days_ago(1),
    default_args=config_args,
    description='import to database raw data',
    schedule_interval=config_args['schedule_interval'],
)


def run_csv_to_json():
    """
    Run the CSV to JSON conversion task.
    """
    try:
        from src.converter.convert_to_json import main
        main(csv_file=config_scripts.get('csv_file_path'),
             json_file=config_scripts.get('json_file_path'),
             batch_size=config_airflow.get('batch_size'))
    except Exception as e:
        logging.error(f"Error in run_csv_to_json: {e}")
        raise  # Re-raise the exception to trigger retries


def run_json_to_db():
    """
    Run the JSON to DB insertion task.
    """
    try:
        from src.db_handler.db import main
        main(json_file_path=config_scripts.get('json_file_path'))
    except Exception as e:
        logging.error(f"Error in run_json_to_db: {e}")
        raise  # Re-raise the exception to trigger retries


# ===================== Define tasks ================================
csv_to_json_task = PythonOperator(
    task_id='csv_to_json',
    python_callable=run_csv_to_json,
    dag=dag,
)

json_to_db_task = PythonOperator(
    task_id='json_to_db',
    python_callable=run_json_to_db,
    dag=dag,
)

# json_to_db depends on csv_to_json
csv_to_json_task >> json_to_db_task
