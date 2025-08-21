import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from inventory_manager import InventoryManager
from resource_path import resource_path

class InventoryApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Enterprise Inventory System")
        self.root.geometry("1000x800")
        self.root.resizable(True, True)
        self.root.iconbitmap(resource_path("app_icon.ico"))

        self.inventory_manager = InventoryManager()

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=1, fill="both")

        # Create tabs (order matters)
        self.create_inventory_tab()
        self.create_sold_tab()
        self.create_full_inventory_tab()

        # Load initial data
        self.update_inventory_list()
        self.update_sold_list()
        self.update_full_inventory()

        # Bind Enter key to search functions for all search entry widgets
        self.search_inventory_entry.bind("<Return>", lambda event: self.search_inventory())
        self.search_sold_entry.bind("<Return>", lambda event: self.search_sold_cards())
        self.search_full_inventory_entry.bind("<Return>", lambda event: self.search_full_inventory())

        # Bind automatic barcode search for all three search bars
        self.search_inventory_entry.bind(
            "<KeyRelease>", lambda event: self.auto_search_barcode(self.search_inventory_entry, self.search_inventory)
        )
        self.search_sold_entry.bind(
            "<KeyRelease>", lambda event: self.auto_search_barcode(self.search_sold_entry, self.search_sold_cards)
        )
        self.search_full_inventory_entry.bind(
            "<KeyRelease>", lambda event: self.auto_search_barcode(self.search_full_inventory_entry, self.search_full_inventory)
        )

        # Bind hotkey: Ctrl+R to refresh current tab
        self.root.bind('<Control-r>', self.refresh_current_tab)


    def auto_search_barcode(self, entry_widget, search_function):
        value = entry_widget.get().strip()
        if len(value) == 12 and value.isdigit():
            search_function()

    def refresh_current_tab(self, event=None):
        current_tab = self.notebook.select()
        tab_text = self.notebook.tab(current_tab, "text")
        if tab_text == "Inventory":
            self.update_inventory_list()
        elif tab_text == "Sold Cards":
            self.update_sold_list()
        elif tab_text == "Full Inventory":
            self.update_full_inventory()

    def create_inventory_tab(self):
        inventory_frame = ttk.Frame(self.notebook)
        self.notebook.add(inventory_frame, text="Inventory")

        ttk.Label(inventory_frame, text="Goldstar Collectibles", font=("Helvetica", 30, "bold")).pack(pady=10)

        # Search Bar
        search_frame = ttk.Frame(inventory_frame)
        search_frame.pack(fill="x", padx=20, pady=10)

        ttk.Label(search_frame, text="Search:").pack(side="left", padx=5)
        self.search_inventory_entry = ttk.Entry(search_frame)
        self.search_inventory_entry.pack(side="left", fill="x", expand=True, padx=5)
        ttk.Button(search_frame, text="Search", command=self.search_inventory).pack(side="left", padx=5)

        # Form for new entries
        form_frame = ttk.LabelFrame(inventory_frame, text="Add New Inventory Item", padding=10)
        form_frame.pack(fill="x", padx=20, pady=10)

        # Left side of the form
        ttk.Label(form_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = ttk.Entry(form_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Condition:").grid(row=1, column=0, padx=5, pady=5)
        self.condition_entry = ttk.Entry(form_frame)
        self.condition_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Card Number:").grid(row=2, column=0, padx=5, pady=5)
        self.card_number_entry = ttk.Entry(form_frame)
        self.card_number_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Buy Price:").grid(row=3, column=0, padx=5, pady=5)
        self.buy_price_entry = ttk.Entry(form_frame)
        self.buy_price_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Button(form_frame, text="ADD ENTRY", command=self.add_inventory_item).grid(row=3, column=2, columnspan=2,
                                                                                       pady=10)

        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=0, column=2, rowspan=3, padx=10, pady=5)
        ttk.Button(button_frame, text="Edit", command=self.edit_card).pack(fill="x", pady=5)
        ttk.Button(button_frame, text="Delete", command=self.delete_card).pack(fill="x", pady=5)
        ttk.Button(button_frame, text="Sell", command=self.sell_card).pack(fill="x", pady=5)

        # --- Treeview for Current Inventory with Vertical Scrollbar only ---
        list_frame = ttk.LabelFrame(inventory_frame, text="Recent Entries", padding=10)
        list_frame.pack(fill="both", padx=20, pady=10, expand=True)

        columns = ("ID", "Name", "Condition", "Card Number", "Buy Price", "Barcode")
        tree_frame = ttk.Frame(list_frame)
        tree_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.inventory_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=20)
        vsb_inventory = ttk.Scrollbar(tree_frame, orient="vertical", command=self.inventory_tree.yview)
        self.inventory_tree.configure(yscrollcommand=vsb_inventory.set)
        self.inventory_tree.pack(side="left", fill="both", expand=True)
        vsb_inventory.pack(side="right", fill="y")

        column_widths = {
            "ID": 10,
            "Name": 150,
            "Condition": 100,
            "Card Number": 120,
            "Buy Price": 100,
            "Barcode": 120,
        }
        for col in columns:
            self.inventory_tree.heading(col, text=col)
            self.inventory_tree.column(col, width=column_widths[col], anchor="center")

    def create_sold_tab(self):
        sold_frame = ttk.Frame(self.notebook)
        self.notebook.add(sold_frame, text="Sold Cards")

        ttk.Label(sold_frame, text="Sold Cards Management", font=("Helvetica", 16, "bold")).pack(pady=10)

        # Search Bar
        search_frame = ttk.Frame(sold_frame)
        search_frame.pack(fill="x", padx=20, pady=10)

        ttk.Label(search_frame, text="Search:").pack(side="left", padx=5)
        self.search_sold_entry = ttk.Entry(search_frame)
        self.search_sold_entry.pack(side="left", fill="x", expand=True, padx=5)
        ttk.Button(search_frame, text="Search", command=self.search_sold_cards).pack(side="left", padx=5)

        # Treeview for displaying sold cards with Vertical Scrollbar only
        columns = ("ID", "Name", "Condition", "Card Number", "Buy Price", "Sell Price", "Date of Sale", "Barcode")
        tree_frame = ttk.Frame(sold_frame)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.sold_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=20)
        vsb_sold = ttk.Scrollbar(tree_frame, orient="vertical", command=self.sold_tree.yview)
        self.sold_tree.configure(yscrollcommand=vsb_sold.set)
        self.sold_tree.pack(side="left", fill="both", expand=True)
        vsb_sold.pack(side="right", fill="y")

        # Define column headings and set widths
        for col in columns:
            column_widths = {
                "ID": 10,
                "Name": 150,
                "Condition": 100,
                "Card Number": 120,
                "Buy Price": 100,
                "Sell Price": 100,
                "Date of Sale": 150,
                "Barcode": 120,
            }
            self.sold_tree.heading(col, text=col)
            self.sold_tree.column(col, width=column_widths[col], anchor="center")

        # All action buttons in one row
        button_frame = ttk.Frame(sold_frame)
        button_frame.pack(fill="x", padx=20, pady=10)

        ttk.Button(button_frame, text="Edit Card", command=self.edit_sold_card).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Delete Card", command=self.delete_sold_card).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Refresh", command=self.update_sold_list).pack(side="left", padx=5)

    def create_full_inventory_tab(self):
        full_inventory_frame = ttk.Frame(self.notebook)
        self.notebook.add(full_inventory_frame, text="Full Inventory")

        ttk.Label(full_inventory_frame, text="Full Inventory View", font=("Helvetica", 16, "bold")).pack(pady=10)

        # Search Bar
        search_frame = ttk.Frame(full_inventory_frame)
        search_frame.pack(fill="x", padx=20, pady=10)

        ttk.Label(search_frame, text="Search:").pack(side="left", padx=5)
        self.search_full_inventory_entry = ttk.Entry(search_frame)
        self.search_full_inventory_entry.pack(side="left", fill="x", expand=True, padx=5)
        ttk.Button(search_frame, text="Search", command=self.search_full_inventory).pack(side="left", padx=5)

        # Treeview for displaying the full inventory with Vertical Scrollbar only
        columns = ("ID", "Name", "Condition", "Card Number", "Buy Price", "Barcode")
        tree_frame = ttk.Frame(full_inventory_frame)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.full_inventory_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=20)
        vsb_full = ttk.Scrollbar(tree_frame, orient="vertical", command=self.full_inventory_tree.yview)
        self.full_inventory_tree.configure(yscrollcommand=vsb_full.set)
        self.full_inventory_tree.pack(side="left", fill="both", expand=True)
        vsb_full.pack(side="right", fill="y")

        # Define column headings and set widths
        for col in columns:
            column_widths = {
                "ID": 10,
                "Name": 150,
                "Condition": 100,
                "Card Number": 120,
                "Buy Price": 100,
                "Barcode": 120,
            }
            self.full_inventory_tree.heading(col, text=col)
            self.full_inventory_tree.column(col, width=column_widths[col], anchor="center")

        # All action buttons in one row
        button_frame = ttk.Frame(full_inventory_frame)
        button_frame.pack(fill="x", padx=20, pady=10)

        ttk.Button(button_frame, text="Sell Card", command=self.sell_selected_card_full_inventory).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Edit Card", command=self.edit_selected_card_full_inventory).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Delete Card", command=self.delete_selected_card_full_inventory).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Refresh", command=self.update_full_inventory).pack(side="left", padx=5)

    def search_full_inventory(self):
        query = self.search_full_inventory_entry.get().strip()
        results = self.inventory_manager.search_inventory(query, latest_first=False)
        for item in self.full_inventory_tree.get_children():
            self.full_inventory_tree.delete(item)
        for card in results:
            self.full_inventory_tree.insert(
                "", "end", values=(card["id"], card["name"], card["condition"], card["card_number"], card["buy_price"],
                                   card["barcode"])
            )

    def add_inventory_item(self):
        name = self.name_entry.get().strip()
        condition = self.condition_entry.get().strip()
        card_number = self.card_number_entry.get().strip()
        buy_price = self.buy_price_entry.get().strip()

        if not name or not condition or not card_number or not buy_price:
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            buy_price = float(buy_price)
        except ValueError:
            messagebox.showerror("Error", "Buy Price must be a valid number!")
            return

        self.inventory_manager.add_card(name, condition, card_number, buy_price)
        self.update_inventory_list()
        self.update_full_inventory()

        self.name_entry.delete(0, tk.END)
        self.condition_entry.delete(0, tk.END)
        self.card_number_entry.delete(0, tk.END)
        self.buy_price_entry.delete(0, tk.END)

    def search_inventory(self):
        query = self.search_inventory_entry.get().strip()
        results = self.inventory_manager.search_inventory(query, latest_first=True)
        for item in self.inventory_tree.get_children():
            self.inventory_tree.delete(item)
        for card in results:
            self.inventory_tree.insert(
                "", "end", values=(
                    card["id"], card["name"], card["condition"], card["card_number"], card["buy_price"], card["barcode"]
                )
            )

    def edit_card(self):
        selected_item = self.inventory_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No item selected!")
            return

        card_id = self.inventory_tree.item(selected_item[0], "values")[0]
        card = self.inventory_manager.get_card_by_id(card_id)

        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Card")
        edit_window.geometry("300x200")

        ttk.Label(edit_window, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        name_entry = ttk.Entry(edit_window)
        name_entry.insert(0, card["name"])
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(edit_window, text="Condition:").grid(row=1, column=0, padx=5, pady=5)
        condition_entry = ttk.Entry(edit_window)
        condition_entry.insert(0, card["condition"])
        condition_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(edit_window, text="Card Number:").grid(row=2, column=0, padx=5, pady=5)
        card_number_entry = ttk.Entry(edit_window)
        card_number_entry.insert(0, card["card_number"])
        card_number_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(edit_window, text="Buy Price:").grid(row=3, column=0, padx=5, pady=5)
        buy_price_entry = ttk.Entry(edit_window)
        buy_price_entry.insert(0, card["buy_price"])
        buy_price_entry.grid(row=3, column=1, padx=5, pady=5)

        def save_changes():
            new_name = name_entry.get().strip()
            new_condition = condition_entry.get().strip()
            new_card_number = card_number_entry.get().strip()
            new_buy_price = buy_price_entry.get().strip()
            if not new_name or not new_condition or not new_card_number or not new_buy_price:
                messagebox.showerror("Error", "All fields are required!")
                return
            try:
                new_buy_price = float(new_buy_price)
            except ValueError:
                messagebox.showerror("Error", "Buy Price must be a valid number!")
                return
            self.inventory_manager.edit_card(card_id, new_name, new_condition, new_card_number, new_buy_price)
            edit_window.destroy()
            self.update_inventory_list()
            self.update_full_inventory()

        ttk.Button(edit_window, text="Save", command=save_changes).grid(row=4, column=0, columnspan=2, pady=10)

    def edit_selected_card_full_inventory(self):
        selected_item = self.full_inventory_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No card selected!")
            return

        card_id = self.full_inventory_tree.item(selected_item[0], "values")[0]
        card = self.inventory_manager.get_card_by_id(card_id)

        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Card")
        edit_window.geometry("400x300")
        edit_window.resizable(True, True)

        ttk.Label(edit_window, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        name_entry = ttk.Entry(edit_window)
        name_entry.insert(0, card["name"])
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(edit_window, text="Condition:").grid(row=1, column=0, padx=5, pady=5)
        condition_entry = ttk.Entry(edit_window)
        condition_entry.insert(0, card["condition"])
        condition_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(edit_window, text="Card Number:").grid(row=2, column=0, padx=5, pady=5)
        card_number_entry = ttk.Entry(edit_window)
        card_number_entry.insert(0, card["card_number"])
        card_number_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(edit_window, text="Buy Price:").grid(row=3, column=0, padx=5, pady=5)
        buy_price_entry = ttk.Entry(edit_window)
        buy_price_entry.insert(0, card["buy_price"])
        buy_price_entry.grid(row=3, column=1, padx=5, pady=5)

        def save_changes():
            new_name = name_entry.get().strip()
            new_condition = condition_entry.get().strip()
            new_card_number = card_number_entry.get().strip()
            new_buy_price = buy_price_entry.get().strip()

            if not new_name or not new_condition or not new_card_number or not new_buy_price:
                messagebox.showerror("Error", "All fields are required!")
                return

            try:
                new_buy_price = float(new_buy_price)
            except ValueError:
                messagebox.showerror("Error", "Buy Price must be a valid number!")
                return

            self.inventory_manager.edit_card(card_id, new_name, new_condition, new_card_number, new_buy_price)
            edit_window.destroy()
            self.update_full_inventory()

        ttk.Button(edit_window, text="Save", command=save_changes).grid(row=4, column=0, columnspan=2, pady=10)

    def edit_sold_card(self):
        selected_item = self.sold_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No card selected!")
            return

        card_id = self.sold_tree.item(selected_item[0], "values")[0]
        card = self.inventory_manager.get_sold_card_by_id(card_id)

        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Sold Card")
        edit_window.geometry("400x350")
        edit_window.resizable(True, True)

        ttk.Label(edit_window, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        name_entry = ttk.Entry(edit_window)
        name_entry.insert(0, card["name"])
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(edit_window, text="Condition:").grid(row=1, column=0, padx=5, pady=5)
        condition_entry = ttk.Entry(edit_window)
        condition_entry.insert(0, card["condition"])
        condition_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(edit_window, text="Card Number:").grid(row=2, column=0, padx=5, pady=5)
        card_number_entry = ttk.Entry(edit_window)
        card_number_entry.insert(0, card["card_number"])
        card_number_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(edit_window, text="Buy Price:").grid(row=3, column=0, padx=5, pady=5)
        buy_price_entry = ttk.Entry(edit_window)
        buy_price_entry.insert(0, card["buy_price"])
        buy_price_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(edit_window, text="Sell Price:").grid(row=4, column=0, padx=5, pady=5)
        sell_price_entry = ttk.Entry(edit_window)
        sell_price_entry.insert(0, card["sell_price"])
        sell_price_entry.grid(row=4, column=1, padx=5, pady=5)

        def save_changes():
            new_name = name_entry.get().strip()
            new_condition = condition_entry.get().strip()
            new_card_number = card_number_entry.get().strip()
            new_buy_price = buy_price_entry.get().strip()
            new_sell_price = sell_price_entry.get().strip()

            if not new_name or not new_condition or not new_card_number or not new_buy_price or not new_sell_price:
                messagebox.showerror("Error", "All fields are required!")
                return

            try:
                new_buy_price = float(new_buy_price)
                new_sell_price = float(new_sell_price)
            except ValueError:
                messagebox.showerror("Error", "Buy Price and Sell Price must be valid numbers!")
                return

            self.inventory_manager.edit_sold_card(card_id, new_name, new_condition, new_card_number, new_buy_price,
                                                  new_sell_price)
            edit_window.destroy()
            self.update_sold_list()

        ttk.Button(edit_window, text="Save", command=save_changes).grid(row=5, column=0, columnspan=2, pady=10)

    def delete_sold_card(self):
        selected_item = self.sold_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No card selected!")
            return

        card_id = self.sold_tree.item(selected_item[0], "values")[0]
        confirm = messagebox.askyesno("Confirm Deletion",
                                      "Are you sure you want to delete this sold card? This action cannot be undone.")
        if confirm:
            self.inventory_manager.delete_sold_item(card_id)
            self.update_sold_list()

    def delete_card(self):
        selected_item = self.inventory_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No item selected!")
            return

        card_id = self.inventory_tree.item(selected_item[0], "values")[0]
        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this item?")
        if confirm:
            self.inventory_manager.delete_inventory_item(card_id)
            self.update_inventory_list()
            self.update_full_inventory()

    def sell_card(self):
        selected_item = self.inventory_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No item selected!")
            return

        card_id = self.inventory_tree.item(selected_item[0], "values")[0]
        sell_price = simpledialog.askfloat("Sell Card", "Enter sale price:")

        if sell_price is None:
            return

        self.inventory_manager.sell_card(card_id, sell_price)
        self.update_inventory_list()
        self.update_full_inventory()
        self.update_sold_list()

    def delete_selected_card_full_inventory(self):
        selected_item = self.full_inventory_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No card selected!")
            return

        card_id = self.full_inventory_tree.item(selected_item[0], "values")[0]
        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this item?")
        if confirm:
            self.inventory_manager.delete_inventory_item(card_id)
            self.update_full_inventory()

    def sell_selected_card_full_inventory(self):
        selected_item = self.full_inventory_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No card selected!")
            return

        card_id = self.full_inventory_tree.item(selected_item[0], "values")[0]
        sell_price = simpledialog.askfloat("Sell Card", "Enter selling price:")
        if sell_price is None:
            return

        self.inventory_manager.sell_card(card_id, sell_price)
        self.update_full_inventory()

    def search_sold_cards(self):
        query = self.search_sold_entry.get().strip()
        results = self.inventory_manager.search_sold_cards(query)
        for item in self.sold_tree.get_children():
            self.sold_tree.delete(item)
        for card in results:
            self.sold_tree.insert(
                "", "end", values=(
                    card["id"], card["name"], card["condition"], card["card_number"], card["buy_price"],
                    card["sell_price"], card["sold_date"], card["barcode"]
                )
            )

    def update_inventory_list(self):
        for item in self.inventory_tree.get_children():
            self.inventory_tree.delete(item)
        inventory = self.inventory_manager.get_inventory_latest_first()
        for card in inventory:
            self.inventory_tree.insert(
                "", "end", values=(
                    card["id"], card["name"], card["condition"], card["card_number"], card["buy_price"], card["barcode"]
                )
            )

    def update_full_inventory(self):
        for item in self.full_inventory_tree.get_children():
            self.full_inventory_tree.delete(item)
        inventory = self.inventory_manager.get_inventory()
        for card in inventory:
            self.full_inventory_tree.insert(
                "", "end", values=(
                    card["id"], card["name"], card["condition"], card["card_number"], card["buy_price"],
                    card["barcode"])
            )

    def update_sold_list(self):
        sold_cards = self.inventory_manager.get_sold_cards()
        for item in self.sold_tree.get_children():
            self.sold_tree.delete(item)
        for card in sold_cards:
            self.sold_tree.insert(
                "", "end", values=(
                    card["id"],
                    card["name"],
                    card["condition"],
                    card["card_number"],
                    card["buy_price"],
                    card["sell_price"],
                    card["sold_date"],
                    card["barcode"]
                )
            )

    def get_selected_card_id(self, listbox, index):
        item = listbox.get(index)
        return int(item.split(" - ")[0])  # Assuming ID is the first part

    def update_listbox(self, listbox, data):
        listbox.delete(0, tk.END)
        for item in data:
            listbox.insert(
                tk.END,
                f"{item['id']} - {item['name']} - {item['condition']} - {item['card_number']} - Barcode: {item['barcode']}",
            )

    def run(self):
        self.root.mainloop()
