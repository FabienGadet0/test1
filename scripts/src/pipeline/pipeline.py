from db_handler.create_connection import create_connection
from converter.convert_to_json import main as convert_to_json
from db_handler.call_procedure import main as call_procedure
from db_handler.load_to_db import main as load_to_db
from converter.unzip import main as unzip
import click


@click.command()
@click.argument('csv_file_path',  type=click.Path(exists=True), envvar="CSV_FILE_PATH")
@click.argument('json_file_path', type=click.Path(exists=True), envvar="JSON_FILE_PATH")
@click.argument('zip_file_path', envvar="ZIP_FILE_PATH",  type=click.Path(exists=True))
@click.option('--batch_size', default='1000', help='Batch size for processing CSV file')
@click.option('--target_dir', default="./data")
def main(csv_file_path, json_file_path, zip_file_path, batch_size, target_dir):

    connected, connection = create_connection()
    if connected:
        print("[INFO] unzipping csv file")
        unzip(zip_file_path, target_dir)
        print("[INFO] running conversion to json ...")
        convert_to_json(csv_file_path, json_file_path, batch_size)
        print("[INFO] running load to database ...")
        load_to_db(json_file_path)
        print("[INFO] Call procedure to extract json ")
        print("[INFO] it can take a little bit of time ...")
        call_procedure()
    else:
        print(f"[ERROR] Can't connect to the database. Error: {connection}")


if __name__ == "__main__":
    main()
