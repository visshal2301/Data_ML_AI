import sys
import sqlite3
import os

# Get the absolute path to the CH3 directory containing this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Construct the path to the SalesDB folder inside CH3
DB_DIR = os.path.join(BASE_DIR, "SalesDB")

os.makedirs(DB_DIR, exist_ok=True)
db_path = os.path.join(DB_DIR, "sales.db")

conn = sqlite3.connect(db_path)

cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
id INTEGER PRIMARY KEY AUTOINCREMENT,
customer_name TEXT NOT NULL,
product_name TEXT NOT NULL,
quantity INTEGER NOT NULL,
price REAL NOT NULL,
total REAL NOT NULL
)
""")


cursor.execute("""
INSERT INTO orders (customer_name, product_name, quantity, price, total) VALUES
("John Doe", "Laptop", 1, 1000.00, 1000.00),
("Jane Smith", "Smartphone", 2, 500.00, 1000.00),
("Bob Johnson", "Tablet", 3, 200.00, 600.00)
""")

conn.commit()
conn.close()