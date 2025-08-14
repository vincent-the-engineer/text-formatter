import argparse
import os
import sys

from pathlib import Path

import textformatter
from textformatter import configfile
from textformatter import textformatter
from textformatter.configfile import (
    read_config_file,
)
from textformatter.textformatter import (
    TextFormatterConfig,
    process_file,
)


def main() -> None:
    parser = argparse.ArgumentParser(usage="%(prog)s <config file> <input files>")
    parser.add_argument("config", nargs=1)
    parser.add_argument("files", nargs="+")
    args = parser.parse_args()
    config_file = Path(args.config[0]).resolve()
    if not os.path.exists(config_file):
        print("Configuration file does not exist.")
        sys.exit(1)
    files = []
    for f in args.files:
        files.extend(list(Path(".").glob(f)))
    files = list(map(lambda f: str(Path(f).resolve()), files))
    if len(files) == 0:
        print("No input files provided.")
        sys.exit(1)
    config = read_config_file(config_file)
    for file in files:
        process_file(file, config)


if __name__ == "__main__":
    main()

