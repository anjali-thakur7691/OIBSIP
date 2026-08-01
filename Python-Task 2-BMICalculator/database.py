"""Safe SQLite persistence layer for BMI records."""
from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_NAME = BASE_DIR / "database" / "bmi.db"


class BMIDatabase:
    def __init__(self, database_path: Path | str = DB_NAME):
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self.create_table()

    @contextmanager
    def connect(self):
        """Yield a connection and always release its file handle."""
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            yield connection
            connection.commit()
        finally:
            connection.close()

    def create_table(self) -> None:
        with self.connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS bmi_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    gender TEXT NOT NULL,
                    weight REAL NOT NULL,
                    height REAL NOT NULL,
                    bmi REAL NOT NULL,
                    category TEXT NOT NULL,
                    date TEXT NOT NULL
                )
            """)

    def save_record(self, name, age, gender, weight, height, bmi, category) -> bool:
        try:
            with self.connect() as conn:
                conn.execute("""INSERT INTO bmi_history
                    (name, age, gender, weight, height, bmi, category, date)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    (name.strip(), age, gender, weight, height, bmi, category,
                     datetime.now().strftime("%d-%m-%Y %H:%M:%S")))
            return True
        except sqlite3.Error:
            return False

    def get_all_records(self) -> list[tuple]:
        try:
            with self.connect() as conn:
                return [tuple(row) for row in conn.execute("SELECT * FROM bmi_history ORDER BY id ASC")]
        except sqlite3.Error:
            return []

    def search_user(self, keyword: str) -> list[tuple]:
        try:
            with self.connect() as conn:
                query = "SELECT * FROM bmi_history WHERE name LIKE ? ORDER BY id ASC"
                return [tuple(row) for row in conn.execute(query, (f"%{keyword.strip()}%",))]
        except sqlite3.Error:
            return []

    def update_record(self, record_id, name, age, gender, weight, height, bmi, category) -> bool:
        try:
            with self.connect() as conn:
                cursor = conn.execute("""UPDATE bmi_history SET name=?, age=?, gender=?, weight=?, height=?, bmi=?, category=?
                    WHERE id=?""", (name.strip(), age, gender, weight, height, bmi, category, record_id))
            return cursor.rowcount == 1
        except sqlite3.Error:
            return False

    def delete_record(self, record_id: int) -> bool:
        try:
            with self.connect() as conn:
                cursor = conn.execute("DELETE FROM bmi_history WHERE id=?", (record_id,))
            return cursor.rowcount == 1
        except sqlite3.Error:
            return False

    def delete_all(self) -> bool:
        try:
            with self.connect() as conn:
                conn.execute("DELETE FROM bmi_history")
            return True
        except sqlite3.Error:
            return False
