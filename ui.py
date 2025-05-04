import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from inventory_manager import InventoryManager


class InventoryApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Enterprise Inventory System")
        self.root.geometry("1000x800")
        self.root.resizable(False, False)

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

    def create_inventory_tab(self):
        inventory_frame = ttk.Frame(self.notebook)
        self.notebook.add(inventory_frame, text="Inventory")

        ttk.Label(inventory_frame, text="King's Foreskin", font=("Helvetica", 30, "bold")).pack(pady=10)

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

        # New field for Buy Price
        ttk.Label(form_frame, text="Buy Price:").grid(row=3, column=0, padx=5, pady=5)
        self.buy_price_entry = ttk.Entry(form_frame)
        self.buy_price_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Button(form_frame, text="ADD ENTRY", command=self.add_inventory_item).grid(row=3, column=2, columnspan=2, pady=10)

        # Right side of the form - Buttons for Edit, Delete, and Sell
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=0, column=2, rowspan=3, padx=10, pady=5)

        ttk.Button(button_frame, text="Edit", command=self.edit_card).pack(fill="x", pady=5)
        ttk.Button(button_frame, text="Delete", command=self.delete_card).pack(fill="x", pady=5)
        ttk.Button(button_frame, text="Sell", command=self.sell_card).pack(fill="x", pady=5)

        # Inventory List
        list_frame = ttk.LabelFrame(inventory_frame, text="Current Inventory", padding=10)
        list_frame.pack(fill="both", padx=20, pady=10, expand=True)
        self.inventory_list = tk.Listbox(list_frame, font=("Courier New", 10), height=15)
        self.inventory_list.pack(fill="both", expand=True, padx=5, pady=5)

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

        # Treeview for displaying sold cards
        columns = ("ID", "Name", "Condition", "Card Number", "Sell Price", "Date of Sale", "Barcode")
        self.sold_tree = ttk.Treeview(sold_frame, columns=columns, show="headings", height=20)
        self.sold_tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Define column headings and set widths
        for col in columns:
            column_widths = {
                "ID": 10,
                "Name": 150,
                "Condition": 100,
                "Card Number": 120,
                "Sell Price": 100,
                "Date of Sale": 150,
                "Barcode": 120,
            }
            self.sold_tree.heading(col, text=col)
            self.sold_tree.column(col, width=column_widths[col], anchor="center")

        # Refresh button to update the sold cards view
        ttk.Button(sold_frame, text="Refresh", command=self.update_sold_list).pack(pady=10)

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

        # Treeview for displaying the full inventory
        columns = ("ID", "Name", "Condition", "Card Number", "Buy Price", "Barcode")
        self.full_inventory_tree = ttk.Treeview(full_inventory_frame, columns=columns, show="headings", height=20)
        self.full_inventory_tree.pack(fill="both", expand=True, padx=5, pady=10)

        # Define column headings
        for col in columns:
            self.full_inventory_tree.heading(col, text=col)
            self.full_inventory_tree.column(col, anchor="center")

        # Button Frame for actions
        button_frame = ttk.Frame(full_inventory_frame)
        button_frame.pack(fill="x", padx=20, pady=10)

        # Add Sell Card Button
        ttk.Button(button_frame, text="Sell Card", command=self.sell_selected_card_full_inventory).pack(side="left",
                                                                                                        padx=5)

        # Add Edit Card Button
        ttk.Button(button_frame, text="Edit Card", command=self.edit_selected_card_full_inventory).pack(side="left",
                                                                                                        padx=5)

        # Add Delete Card Button
        ttk.Button(button_frame, text="Delete Card", command=self.delete_selected_card_full_inventory).pack(side="left",
                                                                                                            padx=5)

        # Refresh button to update the inventory view
        ttk.Button(full_inventory_frame, text="Refresh", command=self.update_full_inventory).pack(pady=10)

    def search_full_inventory(self):
        query = self.search_full_inventory_entry.get().strip()
        results = self.inventory_manager.search_inventory(query)

        # Clear the Treeview
        for item in self.full_inventory_tree.get_children():
            self.full_inventory_tree.delete(item)

        # Populate the Treeview with search results
        for card in results:
            self.full_inventory_tree.insert(
                "", "end", values=(card["id"], card["name"], card["condition"], card["card_number"], card["barcode"])
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
        results = self.inventory_manager.search_inventory(query)
        self.update_listbox(self.inventory_list, results)

    def edit_card(self):
        selected = self.inventory_list.curselection()
        if not selected:
            messagebox.showerror("Error", "No item selected!")
            return

        card_id = self.get_selected_card_id(self.inventory_list, selected[0])
        card = self.inventory_manager.get_card_by_id(card_id)

        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Card")

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

        ttk.Button(edit_window, text="Save", command=save_changes).grid(row=3, column=0, columnspan=2, pady=10)

    def edit_selected_card_full_inventory(self):
        selected_item = self.full_inventory_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No card selected!")
            return

        card_id = self.full_inventory_tree.item(selected_item[0], "values")[0]
        card = self.inventory_manager.get_card_by_id(card_id)

        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Card")

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

        def save_changes():
            new_name = name_entry.get().strip()
            new_condition = condition_entry.get().strip()
            new_card_number = card_number_entry.get().strip()

            if not new_name or not new_condition or not new_card_number:
                messagebox.showerror("Error", "All fields are required!")
                return

            self.inventory_manager.edit_card(card_id, new_name, new_condition, new_card_number)
            self.update_full_inventory()
            edit_window.destroy()

        ttk.Button(edit_window, text="Save", command=save_changes).grid(row=3, column=0, columnspan=2, pady=10)

        edit_window.transient(self.root)
        edit_window.grab_set()
        self.root.wait_window(edit_window)

    def delete_card(self):
        selected = self.inventory_list.curselection()
        if not selected:
            messagebox.showerror("Error", "No item selected!")
            return

        card_id = self.get_selected_card_id(self.inventory_list, selected[0])
        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this item?")
        if confirm:
            self.inventory_manager.delete_inventory_item(card_id)
            self.update_inventory_list()
            self.update_full_inventory()

    def sell_card(self):
        selected = self.inventory_list.curselection()
        if not selected:
            messagebox.showerror("Error", "No item selected!")
            return

        card_id = self.get_selected_card_id(self.inventory_list, selected[0])
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
        query = self.search_sold_entry.get().strip()  # Get the search query from the entry field
        results = self.inventory_manager.search_sold_cards(query)  # Query the InventoryManager for matching sold cards

        # Clear the Treeview
        for item in self.sold_tree.get_children():
            self.sold_tree.delete(item)

        # Populate the Treeview with search results
        for card in results:
            self.sold_tree.insert(
                "", "end", values=(
                    card["id"], card["name"], card["condition"], card["card_number"], card["sell_price"],
                    card["sold_date"], card["barcode"]
                )
            )

    def update_inventory_list(self):
        inventory = self.inventory_manager.get_inventory()
        self.update_listbox(self.inventory_list, inventory)

    def update_full_inventory(self):
        # Clear the Treeview
        for item in self.full_inventory_tree.get_children():
            self.full_inventory_tree.delete(item)

        # Populate the Treeview with inventory data
        inventory = self.inventory_manager.get_inventory()
        for card in inventory:
            self.full_inventory_tree.insert(
                "", "end", values=(
                card["id"], card["name"], card["condition"], card["card_number"], card["buy_price"], card["barcode"])
            )

    def update_sold_list(self):
        sold_cards = self.inventory_manager.get_sold_cards()

        # Clear the Treeview
        for item in self.sold_tree.get_children():
            self.sold_tree.delete(item)

        # Populate the Treeview with sold cards data
        for card in sold_cards:
            self.sold_tree.insert(
                "", "end", values=(
                    card["id"],
                    card["name"],
                    card["condition"],
                    card["card_number"],
                    card["sell_price"],
                    card["sold_date"],
                    card["barcode"]  # Include barcode here
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
