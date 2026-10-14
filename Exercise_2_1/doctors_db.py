"""
Exercise 2-1: Doctors Database with SQLite3
============================================
This program creates a SQLite database for doctors and demonstrates
CRUD (Create, Read, Update, Delete) operations using functions.

Database: doctors.db
Table: doctors (id, first_name, last_name, joining_date, salary, address)
"""

import sqlite3
import os

# ---------------------------------------------------------------------------
# Database path (same directory as this script)
# ---------------------------------------------------------------------------
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "doctors.db")


# ===========================================================================
# CRUD Functions
# ===========================================================================

def create_table():
    """Create the 'doctors' table if it does not already exist."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS doctors (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name    TEXT    NOT NULL,
                last_name     TEXT    NOT NULL,
                joining_date  TEXT    NOT NULL,
                salary        REAL    NOT NULL,
                address       TEXT
            )
        """)
        conn.commit()
    print("[OK] Table 'doctors' is ready.")


def insert_doctor(first_name, last_name, joining_date, salary, address):
    """
    Insert a new doctor into the database.

    Parameters:
        first_name   (str):   Doctor's first name.
        last_name    (str):   Doctor's last name.
        joining_date (str):   Date of joining (YYYY-MM-DD).
        salary       (float): Monthly salary.
        address      (str):   Home / clinic address.

    Returns:
        int: The id of the newly inserted doctor.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO doctors (first_name, last_name, joining_date, salary, address) "
            "VALUES (?, ?, ?, ?, ?)",
            (first_name, last_name, joining_date, salary, address),
        )
        conn.commit()
        return cursor.lastrowid


def get_all_doctors():
    """
    Retrieve every doctor from the database.

    Returns:
        list[tuple]: A list of tuples, each representing a doctor row.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM doctors")
        return cursor.fetchall()


def get_doctor_by_id(doctor_id):
    """
    Retrieve a single doctor by id.

    Parameters:
        doctor_id (int): The doctor's primary-key id.

    Returns:
        tuple | None: The doctor row, or None if not found.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM doctors WHERE id = ?", (doctor_id,))
        return cursor.fetchone()


def update_doctor(doctor_id, first_name, last_name, joining_date, salary, address):
    """
    Update an existing doctor's information.

    Parameters:
        doctor_id    (int):   The id of the doctor to update.
        first_name   (str):   New first name.
        last_name    (str):   New last name.
        joining_date (str):   New joining date (YYYY-MM-DD).
        salary       (float): New salary.
        address      (str):   New address.

    Returns:
        int: Number of rows affected (0 if doctor not found).
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE doctors "
            "SET first_name = ?, last_name = ?, joining_date = ?, salary = ?, address = ? "
            "WHERE id = ?",
            (first_name, last_name, joining_date, salary, address, doctor_id),
        )
        conn.commit()
        return cursor.rowcount


def delete_doctor(doctor_id):
    """
    Delete a doctor by id.

    Parameters:
        doctor_id (int): The id of the doctor to delete.

    Returns:
        int: Number of rows affected (0 if doctor not found).
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM doctors WHERE id = ?", (doctor_id,))
        conn.commit()
        return cursor.rowcount


# ===========================================================================
# Helper: Pretty-print a list of doctors
# ===========================================================================

def display_doctors(doctors):
    """Print a formatted table of doctors to the console."""
    if not doctors:
        print("  (No records found)")
        return

    header = f"{'ID':<5} {'First Name':<15} {'Last Name':<15} {'Joining Date':<15} {'Salary':>15} {'Address'}"
    print(header)
    print("-" * len(header))
    for doc in doctors:
        doc_id, fname, lname, jdate, salary, addr = doc
        print(f"{doc_id:<5} {fname:<15} {lname:<15} {jdate:<15} {salary:>15,.2f} {addr}")


# ===========================================================================
# Demo / Main
# ===========================================================================

def main():
    """Run a complete CRUD demonstration."""

    # --- Step 1: Create table ---
    print("=" * 65)
    print("  STEP 1: CREATE DATABASE & TABLE")
    print("=" * 65)
    create_table()
    print()

    # --- Step 2: Insert sample doctors ---
    print("=" * 65)
    print("  STEP 2: INSERT SAMPLE DOCTORS")
    print("=" * 65)
    sample_doctors = [
        ("John",    "Smith",    "2020-03-15", 75000.00, "123 Main St, New York"),
        ("Sarah",   "Johnson",  "2019-07-22", 82000.00, "456 Oak Ave, Chicago"),
        ("Michael", "Williams", "2021-01-10", 69000.00, "789 Pine Rd, Houston"),
        ("Emily",   "Brown",    "2022-06-05", 91000.00, "321 Elm St, San Francisco"),
        ("David",   "Jones",    "2023-11-18", 65000.00, "654 Maple Dr, Boston"),
    ]
    for fname, lname, jdate, salary, addr in sample_doctors:
        new_id = insert_doctor(fname, lname, jdate, salary, addr)
        print(f"  [OK] Inserted: {fname} {lname}  (ID: {new_id})")
    print()

    # --- Step 3: Select all doctors ---
    print("=" * 65)
    print("  STEP 3: SELECT ALL DOCTORS")
    print("=" * 65)
    doctors = get_all_doctors()
    display_doctors(doctors)
    print()

    # --- Step 4: Update a doctor ---
    print("=" * 65)
    print("  STEP 4: UPDATE DOCTOR (ID = 2)")
    print("=" * 65)
    rows = update_doctor(2, "Sarah", "Johnson-Lee", "2019-07-22", 95000.00, "100 Lake Shore, Chicago")
    if rows:
        print("  [OK] Doctor ID 2 updated successfully.")
        print("  Updated record:")
        doc = get_doctor_by_id(2)
        display_doctors([doc])
    else:
        print("  [WARN] Doctor ID 2 not found.")
    print()

    # --- Step 5: Delete a doctor ---
    print("=" * 65)
    print("  STEP 5: DELETE DOCTOR (ID = 5)")
    print("=" * 65)
    rows = delete_doctor(5)
    if rows:
        print("  [OK] Doctor ID 5 deleted successfully.")
    else:
        print("  [WARN] Doctor ID 5 not found.")
    print()

    # --- Step 6: Final state ---
    print("=" * 65)
    print("  STEP 6: FINAL STATE OF DATABASE")
    print("=" * 65)
    doctors = get_all_doctors()
    display_doctors(doctors)
    print()
    print("Done! Database file saved at:", DB_PATH)


if __name__ == "__main__":
    main()
