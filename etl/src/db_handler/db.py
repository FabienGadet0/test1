import json
import click
import os
import psycopg2
from psycopg2 import extras

# This could also be in an env file or a configuration file
TABLE_NAME = "landing.raw_products"


def load_json_to_pg(json_file, table_name, connection):
    try:
        # Connect to the PostgreSQL database
        cursor = connection.cursor()

        # Read the JSON file
        with open(json_file, 'r') as file:
            data = json.load(file)
        # Insert JSON data into the table
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

    connected, connection = create_connection()
    if connected:
        load_json_to_pg(json_file_path, TABLE_NAME, connection)
    else:
        print(f"Can't connect to database error : {connection}")


if __name__ == "__main__":
    main()
