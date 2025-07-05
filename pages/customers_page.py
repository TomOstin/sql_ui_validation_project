from pathlib import Path
from playwright.sync_api import Page


class CustomersPage:
    """
    Page Object для таблицы клиентов в локальном HTML-файле.
    """

    def __init__(self, page: Page):
        self.page = page
        self.table_selector = "#customers"

    def open(self) -> None:
        """
        Открывает локальный HTML-файл customers.html.
        """
        html_path = Path(__file__).resolve().parent.parent / "webapp" / "customers.html"
        self.page.goto(f"file://{html_path}")

    def get_customers(self) -> list[dict]:
        """
        Парсит таблицу клиентов и возвращает список словарей.

        Returns:
            Список клиентов с полями: id, name, email, country.
        """
        rows = self.page.locator(f"{self.table_selector} tbody tr")
        data = []
        for i in range(rows.count()):
            cells = rows.nth(i).locator("td")
            row = {
                "id": int(cells.nth(0).inner_text()),
                "name": cells.nth(1).inner_text(),
                "email": cells.nth(2).inner_text(),
                "country": cells.nth(3).inner_text(),
            }
            data.append(row)
        return data
