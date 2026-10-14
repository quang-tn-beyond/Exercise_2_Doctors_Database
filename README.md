# Exercise 2 – Doctors Database (SQLite & Flask)

## Overview

This repository contains two sub-projects for **Exercise 2**:

| Sub-project | Description | Technology |
|---|---|---|
| **Exercise 2-1** | Python program that creates a SQLite database for doctors and performs CRUD operations | Python 3 + `sqlite3` (standard library) |
| **Exercise 2-2** | Flask web application that collects doctor information via a form and displays it on a web page | Python 3 + Flask + `sqlite3` |

---

## Exercise 2-1 – SQLite CRUD Operations

### How to run

```bash
cd Exercise_2_1
python doctors_db.py
```

The program will:
1. Create the `doctors.db` database and `doctors` table.
2. Insert sample doctor records.
3. Display all doctors (SELECT).
4. Update a doctor's information (UPDATE).
5. Delete a doctor (DELETE).
6. Display the final state of the database.

---

## Exercise 2-2 – Flask Web Application

### Setup

```bash
cd Exercise_2_2
pip install -r requirements.txt
```

### How to run

```bash
python app.py
```

Then open your browser and navigate to `http://127.0.0.1:5000`.

### Features

- **Home page** (`/`): Displays the list of all doctors in a table.
- **Add Doctor** (`/add`): A form to input new doctor information.
- **Edit Doctor** (`/edit/<id>`): Edit an existing doctor's information.
- **Delete Doctor** (`/delete/<id>`): Remove a doctor from the database.

---

## Database Schema

| Column | Type | Constraints |
|---|---|---|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT |
| `first_name` | TEXT | NOT NULL |
| `last_name` | TEXT | NOT NULL |
| `joining_date` | TEXT | NOT NULL (format: YYYY-MM-DD) |
| `salary` | REAL | NOT NULL |
| `address` | TEXT | — |

---

## Author

Student Exercise – Python & Flask with SQLite
