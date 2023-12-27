
import json
import click
import os
import psycopg2
from psycopg2 import extras

# This could also be in an env file or a configuration file
TABLE_NAME = "landing.raw_products"


def load_json_to_pg(json_file, table_name, connection):
    """
    Load JSON data into a PostgreSQL table.

    Args:
        json_file (str): Path to the JSON file containing the data.
        table_name (str): Name of the PostgreSQL table to insert data into.
        connection: PostgreSQL database connection.

    Returns:
        None
    """
    try:
        cursor = connection.cursor()

        with open(json_file, 'r') as file:
            data = json.load(file)

        insert_query = f"INSERT INTO {table_name} (data) VALUES %s;"
        extras.execute_values(cursor, insert_query, [
                              (json.dumps(record),) for record in data])
        connection.commit()

        print(f"Data loaded successfully into the '{table_name}' table.")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if connection:
            cursor.close()
            connection.close()


def create_connection():
    """
    Create a connection to the PostgreSQL database.

    Returns:
        tuple: A tuple containing a boolean indicating success and the database connection or an error message.
    """
    try:
        host = os.environ.get('DB_HOST', 'localhost')
        database = os.environ.get('DB_DATABASE', 'production')
        user = os.environ.get('DB_USER', 'user')
        password = os.environ.get('DB_PASSWORD', 'pwd')

        connection_params = {
            "host": host,
            "database": database,
            "user": user,
            "password": password,
        }

        connection = psycopg2.connect(**connection_params)

        return True, connection

    except Exception as e:
        error_message = f"Error: {e}"
        return False, error_message


@click.command()
@click.argument('json_file_path', type=click.Path(exists=True))
def main(json_file_path):
    """
    Main function to load JSON data into PostgreSQL table 
    (table name is defined under TABLE_NAME variable)

    Args:
        json_file_path (str): Path to the JSON file containing the data.

    Returns:
        None
    """
    connected, connection = create_connection()
    if connected:
        load_json_to_pg(json_file_path, TABLE_NAME, connection)
    else:
        print(f"Can't connect to the database. Error: {connection}")


if __name__ == "__main__":
    main()
