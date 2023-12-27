import os
import psycopg2


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
