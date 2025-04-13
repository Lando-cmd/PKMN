import sqlite3
from datetime import datetime
from barcode_generator import generate_barcode


class InventoryManager:
    def __init__(self):
        self.connection = sqlite3.connect("inventory.db")
        self.connection.row_factory = sqlite3.Row  # Return rows as dictionaries
        self.create_tables()

    def create_tables(self):
        with self.connection:
            # Create tables
            self.connection.execute("""
                CREATE TABLE IF NOT EXISTS inventory (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    condition TEXT,
                    card_number TEXT,
                    barcode TEXT,
                    date_added TEXT
                )
            """)
            self.connection.execute("""
                CREATE TABLE IF NOT EXISTS sold_cards (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    condition TEXT,
                    card_number TEXT,
                    barcode TEXT,
                    sold_date TEXT,
                    sell_price REAL
                )
            """)

    def add_card(self, name, condition, card_number):
        barcode = generate_barcode()
        date_added = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self.connection:
            self.connection.execute("""
                INSERT INTO inventory (name, condition, card_number, barcode, date_added)
                VALUES (?, ?, ?, ?, ?)
            """, (name, condition, card_number, barcode, date_added))

    def get_inventory(self):
        with self.connection:
            return self.connection.execute("SELECT * FROM inventory").fetchall()

    def get_sold_cards(self):
        with self.connection:
            return self.connection.execute("SELECT * FROM sold_cards").fetchall()

    def sell_card(self, card_id, sell_price):
        with self.connection:
            card = self.get_card_by_id(card_id)
            if card:
                sold_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.connection.execute("""
                    INSERT INTO sold_cards (name, condition, card_number, barcode, sold_date, sell_price)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (card['name'], card['condition'], card['card_number'], card['barcode'], sold_date, sell_price))
                self.connection.execute("DELETE FROM inventory WHERE id = ?", (card_id,))

    def get_card_by_id(self, card_id):
        with self.connection:
            return self.connection.execute("SELECT * FROM inventory WHERE id = ?", (card_id,)).fetchone()

    def edit_card(self, card_id, name, condition, card_number):
        with self.connection:
            self.connection.execute("""
                UPDATE inventory
                SET name = ?, condition = ?, card_number = ?
                WHERE id = ?
            """, (name, condition, card_number, card_id))

    def undo_sale(self, card_id):
        with self.connection:
            card = self.connection.execute("SELECT * FROM sold_cards WHERE id = ?", (card_id,)).fetchone()
            if card:
                self.connection.execute("""
                    INSERT INTO inventory (name, condition, card_number, barcode, date_added)
                    VALUES (?, ?, ?, ?, ?)
                """, (card['name'], card['condition'], card['card_number'], card['barcode'], datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                self.connection.execute("DELETE FROM sold_cards WHERE id = ?", (card_id,))

    def delete_inventory_item(self, card_id):
        with self.connection:
            self.connection.execute("DELETE FROM inventory WHERE id = ?", (card_id,))

    def delete_sold_item(self, card_id):
        with self.connection:
            self.connection.execute("DELETE FROM sold_cards WHERE id = ?", (card_id,))

    def search_inventory(self, query):
        with self.connection:
            return self.connection.execute("""
                SELECT * FROM inventory WHERE name LIKE ? OR condition LIKE ? OR card_number LIKE ?
            """, (f"%{query}%", f"%{query}%", f"%{query}%")).fetchall()

    def search_sold_cards(self, query):
        with self.connection:
            return self.connection.execute("""
                SELECT * FROM sold_cards WHERE name LIKE ? OR condition LIKE ? OR card_number LIKE ?
            """, (f"%{query}%", f"%{query}%", f"%{query}%")).fetchall()