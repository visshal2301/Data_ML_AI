import sqlite3
import os

# Get the absolute path to the CH3 directory containing this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Construct the path to the SalesDB folder inside CH3
DB_DIR = os.path.join(BASE_DIR, "SalesDB")
db_path = os.path.join(DB_DIR, "sales.db")

if not os.path.exists(db_path):
    print(f"Database not found at {db_path}. Please run init.py first.")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    cursor.execute("SELECT * FROM orders")
    rows = cursor.fetchall()
    
    print("--- Orders Table ---")
    print(f"{'ID':<5} | {'Customer Name':<15} | {'Product Name':<15} | {'Qty':<5} | {'Price':<8} | {'Total':<8}")
    print("-" * 65)
    for row in rows:
        print(f"{row[0]:<5} | {row[1]:<15} | {row[2]:<15} | {row[3]:<5} | ${row[4]:<7.2f} | ${row[5]:<7.2f}")
except sqlite3.OperationalError as e:
    print(f"Error querying table: {e}")
finally:
    conn.close()
