import csv
import json
import click

# I use latin-1 because utf-8 returns errors for some specific characters
CSV_ENCODING = 'latin-1'


def process_batch(batch):
    """
    Process a batch of rows from the CSV file.

    Args:
        batch (list): List of rows in the batch.

    Returns:
        list: Processed batch.
    """
    return batch


@click.command()
@click.argument('csv_file_path', envvar="CSV_FILE_PATH")
@click.argument('json_file_path', envvar="JSON_FILE_PATH")
@click.option('--batch_size', default=1000, help='Batch size for processing CSV file')
def main_command(csv_file_path, json_file_path, batch_size):
    return main(csv_file_path, json_file_path, batch_size)


def main(csv_file_path, json_file_path, batch_size):
    """
    Main function to convert CSV to JSON.

    Args:
        csv_file (str): Path to the input CSV file.
        json_file (str): Path to the output JSON file.
        batch_size (int): Batch size for processing CSV file.

    Returns:
        None
    """
    try:
        with open(csv_file_path, 'r', encoding=CSV_ENCODING) as csv_file:
            # I use DictReader because it can read lazily
            csv_reader = csv.DictReader(csv_file)

            batch_count = 0

            with open(json_file_path, 'w', encoding='utf-8') as json_out:
                json_out.write("[")  # Start of JSON array

                for row in csv_reader:
                    if batch_count > 0:
                        json_out.write(',')
                    json_out.write(json.dumps(process_batch([row]), indent=2)[
                                   1:-1])  # Remove leading '[' and trailing ']'
                    batch_count += 1

                json_out.write("]")  # End of JSON array

        print(f"[Success] Processed {batch_count} batches.")

    except UnicodeDecodeError as e:
        print(
            f"[Error] decoding the CSV file. Please check the encoding or file contents.")
        print(f"[Error] details: {e}")


if __name__ == '__main__':
    main_command()
