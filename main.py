import argparse
import csv
import logging
import sys

from tabulate import tabulate

from reports import REPORTS

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

REQUIRED_COLUMNS = {"title", "ctr", "retention_rate"}


def read_csv_files(file_paths: list[str]) -> list[dict]:
    rows = []
    for path in file_paths:
        try:
            with open(path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                if missing := REQUIRED_COLUMNS - set(reader.fieldnames or []):
                    logger.error("Missing columns in %s: %s", path, ", ".join(missing))
                    sys.exit(1)
                rows.extend(reader)
        except FileNotFoundError:
            logger.error("File not found: %s", path)
            sys.exit(1)
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="YouTube metrics reporter")
    parser.add_argument("--files", nargs="+", required=True, help="Paths to CSV files")
    parser.add_argument(
        "--report",
        required=True,
        choices=list(REPORTS.keys()),
        help="Report name",
    )
    args = parser.parse_args()

    rows = read_csv_files(args.files)
    result = REPORTS[args.report](rows)

    if not result:
        print("No data matches the report criteria.")
        return

    print(tabulate(result, headers="keys", tablefmt="simple", floatfmt=".1f"))


if __name__ == "__main__":
    main()