import sqlite3
from datetime import datetime
from barcode_generator import generate_barcode
from PIL import Image, ImageTk
import tkinter as tk

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
            # Create a temporary window to display the PNG
            prank_window = tk.Toplevel()
            prank_window.title("Surprise!")
            prank_window.geometry("1920x1080")  # Adjust size to fit the image
            prank_window.overrideredirect(True)  # Remove window decorations

            # Load and display the image
            img = Image.open("C:\\Users\\landi\\PycharmProjects\\PKMNInventory\\Zach.jpg")
            img = img.resize((3000, 1500))  # Resize the image to fit the window
            img_tk = ImageTk.PhotoImage(img)

            label = tk.Label(prank_window, image=img_tk)
            label.pack()

            # Automatically close the window after 0.5 seconds
            prank_window.after(200, prank_window.destroy)

            # Keep a reference to the image to prevent garbage collection
            prank_window.img_tk = img_tk

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
                    INSERT INTO sold_cards (name, condition, card_number, barcode, sold_date, buy_price, sell_price)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                card['name'], card['condition'], card['card_number'], card['barcode'], sold_date, card['buy_price'],
                sell_price))
                self.connection.execute("DELETE FROM inventory WHERE id = ?", (card_id,))

    def get_card_by_id(self, card_id):
        with self.connection:
            return self.connection.execute("SELECT * FROM inventory WHERE id = ?", (card_id,)).fetchone()

    def edit_card(self, card_id, name, condition, card_number, buy_price):
        with self.connection:
            self.connection.execute("""
                UPDATE inventory
                SET name = ?, condition = ?, card_number = ?, buy_price = ?
                WHERE id = ?
            """, (name, condition, card_number, buy_price, card_id))

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

    def search_inventory(self, query, latest_first=False):
        order = "ORDER BY date_added DESC" if latest_first else ""
        with self.connection:
            return self.connection.execute(
                f"""
                SELECT * FROM inventory
                WHERE name LIKE ? OR condition LIKE ? OR card_number LIKE ?
                {order}
                """,
                (f"%{query}%", f"%{query}%", f"%{query}%")
            ).fetchall()

    def search_sold_cards(self, query):
        with self.connection:
            return self.connection.execute("""
                SELECT * FROM sold_cards WHERE name LIKE ? OR condition LIKE ? OR card_number LIKE ?
            """, (f"%{query}%", f"%{query}%", f"%{query}%")).fetchall()

    def edit_sold_card(self, card_id, name, condition, card_number, buy_price, sell_price):
        with self.connection:
            self.connection.execute("""
                UPDATE sold_cards
                SET name = ?, condition = ?, card_number = ?, buy_price = ?, sell_price = ?
                WHERE id = ?
            """, (name, condition, card_number, buy_price, sell_price, card_id))

    def get_sold_card_by_id(self, card_id):
        with self.connection:
            return self.connection.execute("SELECT * FROM sold_cards WHERE id = ?", (card_id,)).fetchone()

    def get_inventory_latest_first(self):
        with self.connection:
            return self.connection.execute("SELECT * FROM inventory ORDER BY date_added DESC").fetchall()
