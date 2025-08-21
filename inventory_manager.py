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
                    buy_price REAL,
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
                    buy_price REAL,
                    sell_price REAL
                )
            """)

    def add_card(self, name, condition, card_number, buy_price):
        barcode, _ = generate_barcode(name, condition)  # Extract barcode number from tuple
        date_added = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self.connection:
            self.connection.execute("""
                INSERT INTO inventory (name, condition, card_number, buy_price, barcode, date_added)
                 VALUES (?, ?, ?, ?, ?, ?)
            """, (name, condition, card_number, buy_price, barcode, date_added))  # Pass only the barcode number

        # Check if the card name contains "Blastoise"
        if "Blastoise" in name:
            self.prank()

    def prank(self):
        import tkinter as tk
        from PIL import Image, ImageTk
        from resource_path import resource_path

        # Create a window to display the PNG
        prank_window = tk.Toplevel()
        prank_window.title("Surprise!")
        prank_window.geometry("1920x1080")  # You can adjust size as needed
        prank_window.overrideredirect(True)  # Remove window decorations

        # Use resource_path to find the image wherever the app is run
        img_path = resource_path("Zach.jpg")  # or "Zach.jpg" if you keep JPG

        img = Image.open(img_path)
        img = img.resize((1920, 1080))  # Resize the image to fit the window

        img_tk = ImageTk.PhotoImage(img)

        label = tk.Label(prank_window, image=img_tk)
        label.pack(expand=True, fill="both")

        # Automatically close the window after 0.5 seconds
        prank_window.after(500, prank_window.destroy)  # 500 ms = 0.5 seconds

        # Keep a reference to the image to prevent garbage collection
        prank_window.img_tk = img_tk

    def get_inventory(self):
        with self.connection:
            return self.connection.execute("SELECT * FROM inventory").fetchall()

    def get_inventory_latest_first(self):
        with self.connection:
            return self.connection.execute("SELECT * FROM inventory ORDER BY id DESC").fetchall()

    def get_sold_cards(self):
        with self.connection:
            return self.connection.execute("SELECT * FROM sold_cards").fetchall()

    def get_card_by_id(self, card_id):
        with self.connection:
            return self.connection.execute("SELECT * FROM inventory WHERE id = ?", (card_id,)).fetchone()

    def delete_inventory_item(self, card_id):
        with self.connection:
            self.connection.execute("DELETE FROM inventory WHERE id = ?", (card_id,))

    def delete_sold_item(self, card_id):
        with self.connection:
            self.connection.execute("DELETE FROM sold_cards WHERE id = ?", (card_id,))

    def sell_card(self, card_id, sell_price):
        with self.connection:
            card = self.get_card_by_id(card_id)
            if card:
                sold_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.connection.execute("""
                    INSERT INTO sold_cards (name, condition, card_number, barcode, sold_date, buy_price, sell_price)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    card['name'], card['condition'], card['card_number'], card['barcode'], sold_date, card['buy_price'],
                    sell_price))
                self.connection.execute("DELETE FROM inventory WHERE id = ?", (card_id,))

    def search_inventory(self, query, latest_first=False):
        query = query.strip()
        order_clause = "ORDER BY id DESC" if latest_first else ""
        if not query:
            return self.get_inventory_latest_first() if latest_first else self.get_inventory()
        with self.connection:
            return self.connection.execute(f"""
                SELECT * FROM inventory
                WHERE
                    name LIKE ? OR
                    condition LIKE ? OR
                    card_number LIKE ? OR
                    barcode LIKE ?
                {order_clause}
            """, (
                f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%"
            )).fetchall()

    def search_sold_cards(self, query):
        query = query.strip()
        if not query:
            return self.get_sold_cards()
        with self.connection:
            return self.connection.execute("""
                SELECT * FROM sold_cards
                WHERE
                    name LIKE ? OR
                    condition LIKE ? OR
                    card_number LIKE ? OR
                    barcode LIKE ?
                ORDER BY id DESC
            """, (
                f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%"
            )).fetchall()

    def edit_card(self, card_id, name, condition, card_number, buy_price):
        with self.connection:
            self.connection.execute("""
                UPDATE inventory
                SET name = ?, condition = ?, card_number = ?, buy_price = ?
                WHERE id = ?
            """, (name, condition, card_number, buy_price, card_id))

    def edit_sold_card(self, card_id, name, condition, card_number, buy_price, sell_price):
        with self.connection:
            self.connection.execute("""
                UPDATE sold_cards
                SET name = ?, condition = ?, card_number = ?, buy_price = ?, sell_price = ?
                WHERE id = ?
            """, (name, condition, card_number, buy_price, sell_price, card_id))

    def get_sold_card_by_id(self, card_id):
        with self.connection:
            return self.connection.execute(
                "SELECT * FROM sold_cards WHERE id = ?", (card_id,)
            ).fetchone()
