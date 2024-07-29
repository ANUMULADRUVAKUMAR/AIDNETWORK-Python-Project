import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

# Database credentials
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

        ttk.Button(root, text="Login", command=login, style="TButton").pack(pady=20, ipadx=20, ipady=10)
        ttk.Button(root, text="Sign Up", command=sign_up, style="TButton").pack(pady=20, ipadx=20, ipady=10)

    def login():
        for widget in root.winfo_children():
            widget.destroy()

        form_frame = ttk.Frame(root, padding="20")
        form_frame.pack(expand=True, fill=tk.BOTH)

        ttk.Label(form_frame, text="Username", font=large_font).pack(pady=10)
        username_entry = ttk.Entry(form_frame, font=large_font)
        username_entry.pack(pady=10, fill='x')

        ttk.Label(form_frame, text="Password", font=large_font).pack(pady=10)
        password_entry = ttk.Entry(form_frame, show="*", font=large_font)
        password_entry.pack(pady=10, fill='x')

        def authenticate():
            entered_username = username_entry.get()
            entered_password = password_entry.get()

            query = "SELECT * FROM login WHERE username = %s AND password = %s"
            values = (entered_username, entered_password)
            cursor.execute(query, values)
            result = cursor.fetchone()

            if result:
                messagebox.showinfo("Success", "Login successful")
                show_user_menu(entered_username)
            else:
                messagebox.showerror("Error", "Invalid username or password")
                show_main_menu()

        ttk.Button(form_frame, text="Login", command=authenticate, style="TButton").pack(pady=20, ipadx=20, ipady=10)
        ttk.Button(form_frame, text="Back", command=show_main_menu, style="TButton").pack(pady=10, ipadx=20, ipady=10)

    def sign_up():
        for widget in root.winfo_children():
            widget.destroy()

        form_frame = ttk.Frame(root, padding="20")
        form_frame.pack(expand=True, fill=tk.BOTH)

        ttk.Label(form_frame, text="Username", font=large_font).pack(pady=10)
        username_entry = ttk.Entry(form_frame, font=large_font)
        username_entry.pack(pady=10, fill='x')

        ttk.Label(form_frame, text="Password", font=large_font).pack(pady=10)
        password_entry = ttk.Entry(form_frame, show="*", font=large_font)
        password_entry.pack(pady=10, fill='x')

        ttk.Label(form_frame, text="Confirm Password", font=large_font).pack(pady=10)
        confirm_password_entry = ttk.Entry(form_frame, show="*", font=large_font)
        confirm_password_entry.pack(pady=10, fill='x')

        def register():
            entered_username = username_entry.get()
            entered_password = password_entry.get()
            confirm_password = confirm_password_entry.get()

            if entered_password != confirm_password:
                messagebox.showerror("Error", "Passwords do not match")
                return

            # Check if username already exists
            try:
                query = "SELECT username FROM login WHERE username = %s"
                cursor.execute(query, (entered_username,))
                if cursor.fetchone():
                    messagebox.showerror("Error", "Username already exists")
                    return

                # Insert new user
                query = "INSERT INTO login (username, password) VALUES (%s, %s)"
                values = (entered_username, entered_password)
                cursor.execute(query, values)
                connection.commit()

                # Create user-specific table
                create_user_table(entered_username)

                messagebox.showinfo("Success", "Account created successfully")
                show_main_menu()
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error creating account: {e}")

        ttk.Button(form_frame, text="Sign Up", command=register, style="TButton").pack(pady=20, ipadx=20, ipady=10)
        ttk.Button(form_frame, text="Back", command=show_main_menu, style="TButton").pack(pady=10, ipadx=20, ipady=10)

    def create_user_table(username):
        table_name = f"user_{username}"
        try:
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    org_name VARCHAR(255),
                    help_needed VARCHAR(255),
                    problem_desc VARCHAR(255),
                    fund_needed VARCHAR(255),
                    contact_number VARCHAR(255),
                    address VARCHAR(255)
                )
            """)
            connection.commit()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error creating user table: {e}")

    def show_user_menu(username):
        for widget in root.winfo_children():
            widget.destroy()

        ttk.Button(root, text="Seek Help", command=lambda: seek_help(username), style="TButton").pack(pady=20, ipadx=20, ipady=10)
        ttk.Button(root, text="Offer Help", command=offer_help, style="TButton").pack(pady=20, ipadx=20, ipady=10)

    def seek_help(username):
        for widget in root.winfo_children():
            widget.destroy()

        def add_record():
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

            def submit_record():
                org_name = org_name_entry.get()
                help_needed = help_needed_entry.get()
                problem_desc = problem_desc_entry.get()
                fund_needed = fund_needed_entry.get()
                contact_number = contact_number_entry.get()
                address = address_entry.get()

                values = (org_name, help_needed, problem_desc, fund_needed, contact_number, address)

                try:
                    # Insert into user-specific table
                    user_table = f"{username}_requests"
                    cursor.execute(f"""
                        CREATE TABLE IF NOT EXISTS {user_table} (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            org_name VARCHAR(255),
                            help_needed VARCHAR(255),
                            problem_desc VARCHAR(255),
                            fund_needed VARCHAR(255),
                            contact_number VARCHAR(255),
                            address VARCHAR(255)
                        )
                    """)
                    connection.commit()

                    cursor.execute(f"""
                        INSERT INTO {user_table} (org_name, help_needed, problem_desc, fund_needed, contact_number, address)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, values)
                    connection.commit()

                    # Also insert into ngo table
                    cursor.execute("""
                        INSERT INTO request (org_name, help_needed, problem_desc, fund_needed, contact_number, address)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, values)
                    connection.commit()

                    messagebox.showinfo("Success", "Record added successfully")
                    seek_help(username)  # Refresh the seek help view
                except mysql.connector.Error as e:
                    messagebox.showerror("Error", f"Error adding record: {e}")

            ttk.Button(form_frame, text="Submit", command=submit_record, style="TButton").pack(pady=20, ipadx=20,
                                                                                               ipady=10)
            ttk.Button(form_frame, text="Back", command=lambda: show_user_menu(username), style="TButton").pack(pady=10,
                                                                                                                ipadx=20,
                                                                                                                ipady=10)

        def delete_record():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("Warning", "Please select a record to delete")
                return

            record_id = tree.item(selected_item)["values"][0]
            try:
                # Delete from user-specific table
                user_table = f"{username}_requests"
                cursor.execute(f"DELETE FROM {user_table} WHERE id = %s", (record_id,))
                connection.commit()

                # Also delete from ngo table
                cursor.execute("DELETE FROM request WHERE id = %s", (record_id,))
                connection.commit()

                messagebox.showinfo("Success", "Record deleted successfully")
                seek_help(username)  # Refresh the seek help view
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error deleting record: {e}")

        # Display records for the logged-in user
        user_table = f"{username}_requests"
        try:
            cursor.execute(
                f"CREATE TABLE IF NOT EXISTS {user_table} (id INT AUTO_INCREMENT PRIMARY KEY, org_name VARCHAR(255), help_needed VARCHAR(255), problem_desc VARCHAR(255), fund_needed VARCHAR(255), contact_number VARCHAR(255), address VARCHAR(255))")
            connection.commit()

            cursor.execute(f"SELECT * FROM {user_table}")
            rows = cursor.fetchall()

            tree = ttk.Treeview(root, columns=(
            "id", "org_name", "help_needed", "problem_desc", "fund_needed", "contact_number", "address"),
                                show='headings')
            tree.heading("id", text="ID")
            tree.heading("org_name", text="Org Name")
            tree.heading("help_needed", text="Help Needed")
            tree.heading("problem_desc", text="Problem")
            tree.heading("fund_needed", text="Fund Needed")
            tree.heading("contact_number", text="Contact")
            tree.heading("address", text="Address")

            for row in rows:
                tree.insert("", "end", values=row)

            tree.pack(expand=True, fill=tk.BOTH)

            ttk.Button(root, text="Add", command=add_record, style="TButton").pack(side=tk.LEFT, padx=20, pady=20,
                                                                                   ipadx=20, ipady=10)
            ttk.Button(root, text="Delete", command=delete_record, style="TButton").pack(side=tk.RIGHT, padx=20,
                                                                                         pady=20, ipadx=20, ipady=10)

        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error retrieving data: {e}")

        ttk.Button(root, text="Back", command=lambda: show_user_menu(username), style="TButton").pack(pady=20, ipadx=20,
                                                                                                      ipady=10)

        def submit_details():
            org_name = org_name_entry.get()
            help_needed = help_needed_entry.get()
            problem_desc = problem_desc_entry.get()
            fund_needed = fund_needed_entry.get()
            contact_number = contact_number_entry.get()
            address = address_entry.get()

            query = f"""
                INSERT INTO {table_name} (org_name, help_needed, problem_desc, fund_needed, contact_number, address)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (org_name, help_needed, problem_desc, fund_needed, contact_number, address)

            try:
                cursor.execute(query, values)
                connection.commit()
                cursor.execute(f"""
                    INSERT INTO request (org_name, help_needed, problem_desc, fund_needed, contact_number, address)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, values)
                connection.commit()
                messagebox.showinfo("Success", "Details submitted successfully")
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error submitting details: {e}")

            show_user_menu(username)

        ttk.Button(form_frame, text="Submit", command=submit_details, style="TButton").pack(pady=20, ipadx=20, ipady=10)
        ttk.Button(form_frame, text="Add New", command=add_record, style="TButton").pack(pady=10, ipadx=20, ipady=10)
        ttk.Button(form_frame, text="Back", command=lambda: show_user_menu(username), style="TButton").pack(pady=10, ipadx=20, ipady=10)

    def add_record():
        # Functionality to add new records
        pass

    def offer_help():
        for widget in root.winfo_children():
            widget.destroy()

        query = "SELECT * FROM request"
        try:
            cursor.execute(query)
            rows = cursor.fetchall()

            tree = ttk.Treeview(root, columns=(
            "org_name", "help_needed", "problem_desc", "fund_needed", "contact_number", "address"), show='headings')
            tree.heading("org_name", text="Org Name")
            tree.heading("help_needed", text="Help Needed")
            tree.heading("problem_desc", text="Problem")
            tree.heading("fund_needed", text="Fund Needed")
            tree.heading("contact_number", text="Contact")
            tree.heading("address", text="Address")

            for row in rows:
                tree.insert("", "end", values=row)

            tree.pack(expand=True, fill=tk.BOTH)
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error retrieving data: {e}")

        ttk.Button(root, text="Back", command=lambda: show_user_menu(username), style="TButton").pack(pady=20, ipadx=20,
                                                                                                      ipady=10)

    def show_user_menu(username):
        for widget in root.winfo_children():
            widget.destroy()

        ttk.Button(root, text="Seek Help", command=lambda: seek_help(username), style="TButton").pack(pady=20, ipadx=20,
                                                                                                      ipady=10)
        ttk.Button(root, text="Offer Help", command=offer_help, style="TButton").pack(pady=20, ipadx=20, ipady=10)

    # Ensure login table exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS login (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) UNIQUE,
            password VARCHAR(255)
        )
    """)
    connection.commit()

    # Ensure request table exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS request (
            id INT AUTO_INCREMENT PRIMARY KEY,
            org_name VARCHAR(255),
            help_needed VARCHAR(255),
            problem_desc VARCHAR(255),
            fund_needed VARCHAR(255),
            contact_number VARCHAR(255),
            address VARCHAR(255)
        )
    """)
    connection.commit()

    show_main_menu()
    root.mainloop()

if __name__ == "__main__":
    main()
