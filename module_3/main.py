import argparse
from pathlib import Path
from shutil import copyfile
from threading import Thread
from logger import logger


parser = argparse.ArgumentParser(description='Sorting folder')
parser.add_argument("source", help="Source folder")
parser.add_argument("--output", "-o", help="Output folder", default="Sorted_files")


try:
    args = vars(parser.parse_args())
    source = args.get("source")
    output = args.get("output")

except Exception as e:
    print(e)
    parser.print_help()


folders = []


def grabs_folder(path: Path):
    for el in path.iterdir():
        if el.is_dir():
            folders.append(el)
            grabs_folder(el)


def sort(path: Path):
    for el in path.iterdir():
        if el.is_file():
            ext = el.suffix
            new_path = output_folder / ext
            try:
                new_path.mkdir(exist_ok=True, parents=True)
                copyfile(el, new_path / el.name)
            except OSError as e:
                logger.error(e)


if __name__ == '__main__':
    base_folder = Path(source)
    output_folder = Path(output)
    folders.append(base_folder)
    grabs_folder(base_folder)
    threads = []
    for folder in folders:
        th = Thread(target=sort, args=(folder,))
        th.start()
        threads.append(th)

    [th.join() for th in threads]
    print('You can delete the sorted folder')