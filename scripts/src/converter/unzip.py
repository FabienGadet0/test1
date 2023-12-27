import click
import shutil


def main(zip_file_path, target_dir):
    e = shutil.unpack_archive(zip_file_path, target_dir)
    print(f"file {zip_file_path} unzipped to {target_dir}")
    return e


@click.command()
@click.argument('zip_file_path', envvar="ZIP_FILE_PATH",  type=click.Path(exists=True))
@click.option('--target_dir', default="./data")
def main_command(zip_file_path, target_dir):
    main(zip_file_path, target_dir)


if __name__ == '__main__':
    main_command()
