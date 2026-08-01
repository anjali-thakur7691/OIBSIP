"""CSV backup/export helpers."""
import csv
from pathlib import Path

CSV_FILE = Path(__file__).resolve().parent / "csv" / "history.csv"
HEADERS = ["ID", "Name", "Age", "Gender", "Weight", "Height", "BMI", "Category", "Date"]


class CSVHandler:
    def __init__(self, path: Path | str = CSV_FILE):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.create_csv()

    def create_csv(self):
        if not self.path.exists():
            self.sync_records([])

    def sync_records(self, records):
        with self.path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(HEADERS)
            writer.writerows(records)

    def read_csv(self):
        with self.path.open(newline="", encoding="utf-8") as file:
            return list(csv.reader(file))

    def clear_csv(self):
        self.sync_records([])
