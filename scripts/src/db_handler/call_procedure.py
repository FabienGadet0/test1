"""
Call the procedure called raw_json_to_parsed_product 
which parse json data from landing schema to column based table in the public schema
"""

from .create_connection import create_connection


def call_procedure(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("CALL raw_json_to_parsed_product();")
        connection.commit()

        print("Procedure succeeded, json loaded to public schema")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if connection:
            cursor.close()


def main():
    connected, connection = create_connection()
    if connected:
        call_procedure(connection)
        connection.close()
    else:
        print(f"Can't connect to the database. Error: {connection}")


if __name__ == "__main__":
    main()
