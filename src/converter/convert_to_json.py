import csv
import json
import click

# i use latin-1 because utf-8 return errors for some specific characters
CSV_ENCODING = 'latin-1'


def process_batch(batch):
    return json.dumps(batch, indent=2)


@click.command()
@click.option('--csv-file', required=True, help='Path to the input CSV file')
@click.option('--json-file', required=True, help='Path to the output JSON file')
@click.option('--batch-size', default=1000, help='Batch size for processing CSV file')
def main(csv_file, json_file, batch_size):
    """

    """
    data_list = []

    try:
        with open(csv_file, 'r', encoding=CSV_ENCODING) as csv_file:
            # i use dictReader because it can read lazily
            csv_reader = csv.DictReader(csv_file)

            batch_count = 0
            for row in csv_reader:
                data_list.append(row)

                if len(data_list) == batch_size:
                    json_batch = process_batch(data_list)

                    # write to JSON
                    with open(json_file, 'a', encoding='utf-8') as json_out:
                        json_out.write(json_batch)

                    # clear for next batch
                    data_list = []
                    batch_count += 1

            if data_list:
                json_batch = process_batch(data_list)
                with open(json_file, 'a', encoding='utf-8') as json_out:
                    json_out.write(json_batch)

        print(f"[Success] Processed {batch_count + 1} batches.")

    except UnicodeDecodeError as e:
        print(
            f"[Error] decoding the CSV file. Please check the encoding or file contents.")
        print(f"[Error] details: {e}")


if __name__ == '__main__':
    main()
