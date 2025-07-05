import sqlite3
import csv
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "database.db"
SCHEMA_PATH = Path(__file__).resolve().parent / "schema.sql"
DATA_DIR = Path(__file__).resolve().parent.parent / "data"

TABLES = {
    "customers": ["id", "name", "email", "country"],
    "orders": ["id", "customer_id", "order_date", "total_amount"],
    "order_items": ["id", "order_id", "product_name", "quantity", "price"],
}


def create_database(connection: sqlite3.Connection) -> None:
    """
    Создаёт таблицы в SQLite, применяя schema.sql.
    """
    with SCHEMA_PATH.open("r", encoding="utf-8") as schema_file:
        sql_script = schema_file.read()
        connection.executescript(sql_script)
        print("Таблицы успешно созданы.")


def load_csv_to_table(connection: sqlite3.Connection, table: str, columns: list[str]) -> None:
    """
    Загружает CSV-файл в указанную таблицу.

    Args:
        connection: SQLite-соединение.
        table: Название таблицы.
        columns: Список колонок таблицы.
    """
    file_path = DATA_DIR / f"{table}.csv"
    with file_path.open("r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        rows = [tuple(row[col] for col in columns) for row in reader]

    placeholders = ", ".join("?" * len(columns))
    query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"

    with connection:
        connection.executemany(query, rows)
        print(f"{table}: загружено {len(rows)} строк.")


def main() -> None:
    """
    Основная точка входа: создание БД и загрузка всех CSV.
    """
    with sqlite3.connect(DB_PATH) as conn:
        create_database(conn)

        for table_name, columns in TABLES.items():
            load_csv_to_table(conn, table_name, columns)

    print("Импорт данных завершён.")


if __name__ == "__main__":
    main()
