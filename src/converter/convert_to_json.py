
import csv
import json
import click

# i use latin-1 because utf-8 return errors for some specific characters
CSV_ENCODING = 'latin-1'


def process_batch(batch):
    return batch


@click.command()
@click.option('--csv-file', required=True, help='Path to the input CSV file')
@click.option('--json-file', required=True, help='Path to the output JSON file')
@click.option('--batch-size', default=1000, help='Batch size for processing CSV file')
def main(csv_file, json_file, batch_size):
    try:
        with open(csv_file, 'r', encoding=CSV_ENCODING) as csv_file:
            # i use dictReader because it can read lazily
            csv_reader = csv.DictReader(csv_file)

            batch_count = 0

            with open(json_file, 'w', encoding='utf-8') as json_out:
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
    main()
