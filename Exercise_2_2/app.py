"""
Exercise 2-2: Flask Web Application for Doctors Database
=========================================================
A web application that allows users to:
  - View all doctors in a table.
  - Add a new doctor via a form.
  - Edit an existing doctor.
  - Delete a doctor.
"""

from flask import Flask, render_template, request, redirect, url_for, flash
import db_helper

app = Flask(__name__)
app.secret_key = "doctors_secret_key_2024"


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    """Home page – display the list of all doctors."""
    doctors = db_helper.get_all_doctors()
    return render_template("doctor_list.html", doctors=doctors)


@app.route("/add", methods=["GET", "POST"])
def add_doctor():
    """Show the add-doctor form (GET) or process the form submission (POST)."""
    if request.method == "POST":
        first_name = request.form["first_name"].strip()
        last_name = request.form["last_name"].strip()
        joining_date = request.form["joining_date"]
        salary = float(request.form["salary"])
        address = request.form["address"].strip()

        db_helper.insert_doctor(first_name, last_name, joining_date, salary, address)
        flash(f"Doctor {first_name} {last_name} added successfully!", "success")
        return redirect(url_for("index"))

    return render_template("add_doctor.html")


@app.route("/edit/<int:doctor_id>", methods=["GET", "POST"])
def edit_doctor(doctor_id):
    """Show the edit form pre-filled with existing data (GET) or save changes (POST)."""
    doctor = db_helper.get_doctor_by_id(doctor_id)
    if doctor is None:
        flash("Doctor not found.", "danger")
        return redirect(url_for("index"))

    if request.method == "POST":
        first_name = request.form["first_name"].strip()
        last_name = request.form["last_name"].strip()
        joining_date = request.form["joining_date"]
        salary = float(request.form["salary"])
        address = request.form["address"].strip()

        db_helper.update_doctor(doctor_id, first_name, last_name, joining_date, salary, address)
        flash(f"Doctor {first_name} {last_name} updated successfully!", "success")
        return redirect(url_for("index"))

    return render_template("add_doctor.html", doctor=doctor, edit_mode=True)


@app.route("/delete/<int:doctor_id>", methods=["POST"])
def delete_doctor(doctor_id):
    """Delete a doctor and redirect back to the list."""
    doctor = db_helper.get_doctor_by_id(doctor_id)
    if doctor:
        db_helper.delete_doctor(doctor_id)
        flash(f"Doctor {doctor['first_name']} {doctor['last_name']} deleted.", "warning")
    else:
        flash("Doctor not found.", "danger")
    return redirect(url_for("index"))


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    db_helper.create_table()
    print("Starting Flask server at http://127.0.0.1:5000")
    app.run(debug=True)
