import csv
import random
from faker import Faker
from datetime import date
from pathlib import Path

# Константы генерации
NUM_CUSTOMERS = 50
NUM_ORDERS = 200

# Инициализация Faker и фиксирование random seed
faker = Faker()
Faker.seed(42)
random.seed(42)

# Директория для сохранения CSV-файлов
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)


def generate_customers(num_customers: int) -> list[dict]:
    """
    Генерирует список клиентов.

    Args:
        num_customers: Количество клиентов для генерации.

    Returns:
        Список словарей с данными клиентов.
    """
    customers = []
    for i in range(1, num_customers + 1):
        email = faker.email() if random.random() > 0.05 else ""  # 5% клиентов с пустым email
        customers.append({
            "id": i,
            "name": faker.name(),
            "email": email,
            "country": faker.country()
        })
    return customers


def generate_orders(customers: list[dict], num_orders: int) -> list[dict]:
    """
    Генерирует список заказов.

    Args:
        customers: Список клиентов.
        num_orders: Количество заказов для генерации.

    Returns:
        Список словарей с заказами (с пустым total_amount).
    """
    orders = []
    for i in range(1, num_orders + 1):
        customer = random.choice(customers)
        order_date = faker.date_between(start_date='-1y', end_date='today')
        orders.append({
            "id": i,
            "customer_id": customer["id"],
            "order_date": order_date,
            "total_amount": 0.0  # Будет пересчитано после генерации позиций
        })
    return orders


def generate_order_items(orders: list[dict]) -> list[dict]:
    """
    Генерирует список позиций заказов и пересчитывает total_amount для каждого заказа.

    Args:
        orders: Список заказов.

    Returns:
        Список позиций заказов.
    """
    order_items = []
    item_id = 1
    for order in orders:
        num_items = random.randint(1, 5)
        order_total = 0.0

        for _ in range(num_items):
            quantity = random.randint(1, 3)
            price = round(random.uniform(5.0, 200.0), 2)
            order_total += quantity * price

            order_items.append({
                "id": item_id,
                "order_id": order["id"],
                "product_name": faker.word().capitalize(),
                "quantity": quantity,
                "price": price
            })
            item_id += 1

        order["total_amount"] = round(order_total, 2)

    return order_items


def write_csv(filename: str, fieldnames: list[str], rows: list[dict]) -> None:
    """
    Сохраняет данные в CSV-файл.

    Args:
        filename: Название файла.
        fieldnames: Заголовки столбцов.
        rows: Список строк для записи.
    """
    file_path = DATA_DIR / filename
    with file_path.open(mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    """Точка входа: генерация клиентов, заказов и позиций."""
    customers = generate_customers(NUM_CUSTOMERS)
    orders = generate_orders(customers, NUM_ORDERS)
    order_items = generate_order_items(orders)

    write_csv("customers.csv", ["id", "name", "email", "country"], customers)
    write_csv("orders.csv", ["id", "customer_id", "order_date", "total_amount"], orders)
    write_csv("order_items.csv", ["id", "order_id", "product_name", "quantity", "price"], order_items)

    print("Данные успешно сгенерированы в папку /data")


if __name__ == "__main__":
    main()
