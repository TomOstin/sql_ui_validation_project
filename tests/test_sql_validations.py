import sqlite3
from pathlib import Path
import pytest

DB_PATH = Path(__file__).resolve().parent.parent / "db" / "database.db"
SQL_DIR = Path(__file__).resolve().parent.parent / "sql_queries"


def run_sql_file(filename: str) -> list[tuple]:
    """
    Исполняет SQL-файл и возвращает результат выборки.

    Args:
        filename: Название SQL-файла в директории sql_queries.

    Returns:
        Список строк результата (list of tuples).
    """
    sql_path = SQL_DIR / filename
    with sql_path.open("r", encoding="utf-8") as file:
        query = file.read()

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.execute("BEGIN")
        result = cursor.execute(query).fetchall()
        return result


def test_no_invalid_emails():
    """
    Проверяет, что нет клиентов с пустыми e-mail.
    """
    rows = run_sql_file("invalid_emails.sql")
    assert len(rows) == 0, f"Найдены клиенты с пустым e-mail: {rows}"


def test_no_order_discrepancies():
    """
    Проверяет, что сумма total_amount в orders совпадает с суммой позиций.
    """
    rows = run_sql_file("order_discrepancies.sql")
    assert len(rows) == 0, f"Обнаружены расхождения в заказах: {rows}"


def test_top_customers_limit():
    """
    Проверяет, что запрос top_customers возвращает ровно 5 строк.
    """
    rows = run_sql_file("top_customers.sql")
    assert len(rows) == 5, f"Ожидалось 5 клиентов, получено: {len(rows)}"
