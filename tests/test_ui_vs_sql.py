import sqlite3
import pytest
from pages.customers_page import CustomersPage
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "db" / "database.db"


def fetch_customers_from_sql() -> list[dict]:
    """
    Загружает клиентов из SQLite в формате list[dict].
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        rows = cursor.execute("SELECT id, name, email, country FROM customers").fetchall()
        return [
            {"id": row[0], "name": row[1], "email": row[2], "country": row[3]}
            for row in rows
        ]


def test_ui_matches_sql(page):
    """
    Сравнивает данные из UI и SQL по клиентам (id, name, email, country).
    """
    ui_page = CustomersPage(page)
    ui_page.open()
    ui_customers = ui_page.get_customers()
    sql_customers = fetch_customers_from_sql()

    for customer in ui_customers:
        assert customer in sql_customers, f"Клиент из UI не найден в SQL: {customer}"
