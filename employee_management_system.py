import mysql.connector as mysql
import sys
import os

# ---------------- DATABASE CONFIG ----------------
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "your_password_here"   # CHANGE THIS
DB_NAME = "employee"

# ---------------- UTILITY FUNCTIONS ----------------
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def get_connection(database=None):
    return mysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=database
    )

# ---------------- DATABASE FUNCTIONS ----------------
def create_database():
    try:
        con = get_connection()
        cur = con.cursor()
        cur.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print("Database created successfully.")
        con.close()
    except mysql.Error as err:
        print("Error:", err)

def show_databases():
    try:
        con = get_connection()
        cur = con.cursor()
        cur.execute("SHOW DATABASES")
        for db in cur:
            print(db[0])
        con.close()
    except mysql.Error as err:
        print("Error:", err)

def create_table():
    try:
        con = get_connection(DB_NAME)
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS emp (
                id INT PRIMARY KEY,
                name VARCHAR(30),
                salary FLOAT
            )
        """)
        print("Table 'emp' created successfully.")
        con.close()
    except mysql.Error as err:
        print("Error:", err)

def show_tables():
    try:
        con = get_connection(DB_NAME)
        cur = con.cursor()
        cur.execute("SHOW TABLES")
        for table in cur:
            print(table[0])
        con.close()
    except mysql.Error as err:
        print("Error:", err)

# ---------------- CRUD OPERATIONS ----------------
def insert_record():
    try:
        con = get_connection(DB_NAME)
        cur = con.cursor()
        eid = int(input("Enter Employee ID: "))
        name = input("Enter Employee Name: ")
        salary = float(input("Enter Salary: "))

        query = "INSERT INTO emp (id, name, salary) VALUES (%s, %s, %s)"
        cur.execute(query, (eid, name, salary))
        con.commit()
        print("Record inserted successfully.")
        con.close()
    except mysql.Error as err:
        print("Error:", err)

def update_record():
    try:
        con = get_connection(DB_NAME)
        cur = con.cursor()
        eid = int(input("Enter Employee ID to update: "))
        name = input("Enter new name: ")
        salary = float(input("Enter new salary: "))

        query = "UPDATE emp SET name=%s, salary=%s WHERE id=%s"
        cur.execute(query, (name, salary, eid))
        con.commit()

        if cur.rowcount > 0:
            print("Record updated successfully.")
        else:
            print("Employee not found.")
        con.close()
    except mysql.Error as err:
        print("Error:", err)

def delete_record():
    try:
        con = get_connection(DB_NAME)
        cur = con.cursor()
        eid = int(input("Enter Employee ID to delete: "))

        query = "DELETE FROM emp WHERE id=%s"
        cur.execute(query, (eid,))
        con.commit()

        if cur.rowcount > 0:
            print("Record deleted successfully.")
        else:
            print("Employee not found.")
        con.close()
    except mysql.Error as err:
        print("Error:", err)

def search_record():
    try:
        con = get_connection(DB_NAME)
        cur = con.cursor()

        print("1. Search by ID")
        print("2. Search by Name")
        print("3. Search by Salary")
        choice = int(input("Enter choice: "))

        if choice == 1:
            eid = int(input("Enter ID: "))
            cur.execute("SELECT * FROM emp WHERE id=%s", (eid,))
        elif choice == 2:
            name = input("Enter name: ")
            cur.execute("SELECT * FROM emp WHERE name LIKE %s", (f"%{name}%",))
        elif choice == 3:
            salary = float(input("Enter salary: "))
            cur.execute("SELECT * FROM emp WHERE salary=%s", (salary,))
        else:
            print("Invalid choice")
            return

        records = cur.fetchall()
        if records:
            for r in records:
                print(r)
        else:
            print("No records found.")
        con.close()
    except mysql.Error as err:
        print("Error:", err)

def display_records():
    try:
        con = get_connection(DB_NAME)
        cur = con.cursor()
        cur.execute("SELECT * FROM emp")
        records = cur.fetchall()

        print("\nID\tName\t\tSalary")
        print("-" * 30)
        for r in records:
            print(f"{r[0]}\t{r[1]}\t\t{r[2]}")
        print(f"\nTotal Records: {len(records)}")
        con.close()
    except mysql.Error as err:
        print("Error:", err)

# ---------------- MAIN MENU ----------------
def menu():
    while True:
        clear_screen()
        print("===== EMPLOYEE MANAGEMENT SYSTEM =====")
        print("1. Create Database")
        print("2. Show Databases")
        print("3. Create Table")
        print("4. Show Tables")
        print("5. Insert Record")
        print("6. Update Record")
        print("7. Delete Record")
        print("8. Search Record")
        print("9. Display Records")
        print("10. Exit")

        try:
            choice = int(input("Enter choice (1-10): "))
        except ValueError:
            print("Invalid input!")
            input("Press Enter to continue...")
            continue

        if choice == 1:
            create_database()
        elif choice == 2:
            show_databases()
        elif choice == 3:
            create_table()
        elif choice == 4:
            show_tables()
        elif choice == 5:
            insert_record()
        elif choice == 6:
            update_record()
        elif choice == 7:
            delete_record()
        elif choice == 8:
            search_record()
        elif choice == 9:
            display_records()
        elif choice == 10:
            print("Exiting program...")
            sys.exit()
        else:
            print("Wrong choice!")

        input("\nPress Enter to continue...")

menu()
