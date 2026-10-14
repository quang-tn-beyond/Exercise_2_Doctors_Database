"""
db_helper.py – Database helper module for the Flask application.
=================================================================
Provides functions to interact with the doctors SQLite database.
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "doctors.db")


def get_connection():
    """Create and return a new database connection with Row factory."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn


def create_table():
    """Create the 'doctors' table if it does not already exist."""
    with get_connection() as conn:
        conn.execute("""
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


def insert_doctor(first_name, last_name, joining_date, salary, address):
    """Insert a new doctor and return the new row id."""
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO doctors (first_name, last_name, joining_date, salary, address) "
            "VALUES (?, ?, ?, ?, ?)",
            (first_name, last_name, joining_date, salary, address),
        )
        conn.commit()
        return cursor.lastrowid


def get_all_doctors():
    """Return all doctors as a list of sqlite3.Row objects."""
    with get_connection() as conn:
        return conn.execute("SELECT * FROM doctors ORDER BY id").fetchall()


def get_doctor_by_id(doctor_id):
    """Return a single doctor by id, or None."""
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM doctors WHERE id = ?", (doctor_id,)
        ).fetchone()


def update_doctor(doctor_id, first_name, last_name, joining_date, salary, address):
    """Update an existing doctor. Returns number of rows affected."""
    with get_connection() as conn:
        cursor = conn.execute(
            "UPDATE doctors "
            "SET first_name = ?, last_name = ?, joining_date = ?, salary = ?, address = ? "
            "WHERE id = ?",
            (first_name, last_name, joining_date, salary, address, doctor_id),
        )
        conn.commit()
        return cursor.rowcount


def delete_doctor(doctor_id):
    """Delete a doctor by id. Returns number of rows affected."""
    with get_connection() as conn:
        cursor = conn.execute("DELETE FROM doctors WHERE id = ?", (doctor_id,))
        conn.commit()
        return cursor.rowcount
