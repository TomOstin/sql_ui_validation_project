import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "db" / "database.db"
OUTPUT_PATH = Path(__file__).resolve().parent / "customers.html"


def fetch_customers() -> list[tuple]:
    """
    Извлекает всех клиентов из базы данных.

    Returns:
        Список кортежей (id, name, email, country).
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email, country FROM customers")
        return cursor.fetchall()


def render_html(customers: list[tuple]) -> str:
    """
    Создаёт HTML-таблицу с клиентами.

    Args:
        customers: Список клиентов.

    Returns:
        HTML-контент как строка.
    """
    rows = "\n".join(
        f"<tr><td>{c[0]}</td><td>{c[1]}</td><td>{c[2]}</td><td>{c[3]}</td></tr>"
        for c in customers
    )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Customers Table</title>
</head>
<body>
    <h1>Customers</h1>
    <table id="customers">
        <thead>
            <tr><th>ID</th><th>Name</th><th>Email</th><th>Country</th></tr>
        </thead>
        <tbody>
            {rows}
        </tbody>
    </table>
</body>
</html>"""
    return html


def main():
    customers = fetch_customers()
    html = render_html(customers)
    with OUTPUT_PATH.open("w", encoding="utf-8") as file:
        file.write(html)
    print(f"HTML сгенерирован: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
