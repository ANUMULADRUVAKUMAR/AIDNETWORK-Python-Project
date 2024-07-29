import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

username = "root"
password = "Druva@0724"
host = "localhost"
database = "ngo"

# Connect to the MySQL database
try:
    connection = mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=database
    )
    cursor = connection.cursor()
    print("Successfully connected to MySQL Database")
except mysql.connector.Error as e:
    print(f"Error connecting to MySQL: {e}")
    exit(1)


def main():
    root = tk.Tk()
    root.title("Help Application")
    root.geometry("600x400")

    # Define a large font
    large_font = ("Arial", 16)
    button_font = ("Arial", 14)

    def show_main_menu():
        for widget in root.winfo_children():
            widget.destroy()

        ttk.Button(root, text="Seek Help", command=seek_help, style="TButton").pack(pady=20, ipadx=20, ipady=10)
        ttk.Button(root, text="Offer Help", command=offer_help, style="TButton").pack(pady=20, ipadx=20, ipady=10)

    def seek_help():
        for widget in root.winfo_children():
            widget.destroy()

        form_frame = ttk.Frame(root, padding="20")
        form_frame.pack(expand=True, fill=tk.BOTH)

        ttk.Label(form_frame, text="Organization/Person Name", font=large_font).pack(pady=10)
        org_name_entry = ttk.Entry(form_frame, font=large_font)
        org_name_entry.pack(pady=10, fill='x')

        ttk.Label(form_frame, text="Help Needed", font=large_font).pack(pady=10)
        help_needed_entry = ttk.Entry(form_frame, font=large_font)
        help_needed_entry.pack(pady=10, fill='x')

        ttk.Label(form_frame, text="Problem Description", font=large_font).pack(pady=10)
        problem_desc_entry = ttk.Entry(form_frame, font=large_font)
        problem_desc_entry.pack(pady=10, fill='x')

        ttk.Label(form_frame, text="Fund Needed", font=large_font).pack(pady=10)
        fund_needed_entry = ttk.Entry(form_frame, font=large_font)
        fund_needed_entry.pack(pady=10, fill='x')

        ttk.Label(form_frame, text="Contact Number", font=large_font).pack(pady=10)
        contact_number_entry = ttk.Entry(form_frame, font=large_font)
        contact_number_entry.pack(pady=10, fill='x')

        ttk.Label(form_frame, text="Address", font=large_font).pack(pady=10)
        address_entry = ttk.Entry(form_frame, font=large_font)
        address_entry.pack(pady=10, fill='x')

        def submit_details():
            org_name = org_name_entry.get()
            help_needed = help_needed_entry.get()
            problem_desc = problem_desc_entry.get()
            fund_needed = fund_needed_entry.get()
            contact_number = contact_number_entry.get()
            address = address_entry.get()

            query = """
                INSERT INTO request (org_name, help_needed, problem_desc, fund_needed, contact_number, address)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (org_name, help_needed, problem_desc, fund_needed, contact_number, address)

            try:
                cursor.execute(query, values)
                connection.commit()
                messagebox.showinfo("Success", "Details submitted successfully")
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error submitting details: {e}")

            show_main_menu()

        ttk.Button(form_frame, text="Submit", command=submit_details, style="TButton").pack(pady=20, ipadx=20, ipady=10)
        ttk.Button(form_frame, text="Back", command=show_main_menu, style="TButton").pack(pady=10, ipadx=20, ipady=10)

    def offer_help():
        for widget in root.winfo_children():
            widget.destroy()

        query = "SELECT * FROM request"
        try:
            cursor.execute(query)
            rows = cursor.fetchall()

            tree = ttk.Treeview(root, columns=("org_name", "help_needed", "problem_desc", "fund_needed", "contact_number", "address"), show='headings')
            tree.heading("org_name", text="Org Name")
            tree.heading("help_needed", text="Help Needed")
            tree.heading("problem_desc", text="Problem")
            tree.heading("fund_needed", text="Fund Needed")
            tree.heading("contact_number", text="Contact")
            tree.heading("address", text="Address")

            for row in rows:
                tree.insert("", "end", values=row[1:])

            tree.pack(expand=True, fill=tk.BOTH)
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error retrieving data: {e}")

        ttk.Button(root, text="Back", command=show_main_menu, style="TButton").pack(pady=20, ipadx=20, ipady=10)

    show_main_menu()
    root.mainloop()


if __name__ == "__main__":
    main()
