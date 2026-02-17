import sqlite3
from pathlib import Path


DB_PATH = Path('demo.db')


def create_database() -> None:
    """Create a demo SQLite database with sample schema and data."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.executescript(
        """
        DROP TABLE IF EXISTS customers;
        DROP TABLE IF EXISTS orders;

        CREATE TABLE customers (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            country TEXT NOT NULL
        );

        CREATE TABLE orders (
            id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        );
        """
    )

    customers = [
        (1, 'Alice', 'USA'),
        (2, 'Bob', 'Germany'),
        (3, 'Charlie', 'USA'),
    ]

    orders = [
        (1, 1, 120.5, '2024-01-10'),
        (2, 1, 75.0, '2024-02-12'),
        (3, 2, 300.0, '2024-03-01'),
        (4, 3, 50.0, '2024-03-15'),
    ]

    cursor.executemany('INSERT INTO customers VALUES (?, ?, ?);', customers)
    cursor.executemany('INSERT INTO orders VALUES (?, ?, ?, ?);', orders)

    conn.commit()
    conn.close()


if __name__ == '__main__':
    create_database()
    print('Demo database created at demo.db')
