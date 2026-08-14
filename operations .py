import csv
from datetime import datetime

# Lists to store data
employees = []
attendance_records = []

def load_employees():
    global employees
    try:
        with open("employees.csv", "r", newline="") as file:
            reader = csv.DictReader(file)
            employees = list(reader)

    except FileNotFoundError:
        employees = []


def save_employees():
    with open("employees.csv", "w", newline="") as file:
        fieldnames = ["Employee ID", "Name", "Department"]
        writer = csv.DictWriter(file,fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(employees)


def add_employee(employee_id, name, department):
    # Validate empty fields
    if not employee_id or not name or not department:
        print("All fields are required.")
        return False

    # Prevent duplicate Employee ID
    for employee in employees:
        if employee["Employee ID"] == employee_id:
            print("Employee ID already exists.")
            return False

    employee = {
        "Employee ID": employee_id,
        "Name": name,
        "Department": department
    }

    employees.append(employee)

    save_employees()

    print("Employee added successfully.")

    return True


def display_employees():
    if not employees:
        print("No employees found.")
        return
    for employee in employees:
        print(
            f"ID: {employee['Employee ID']} | "
            f"Name: {employee['Name']} | "
            f"Department: {employee['Department']}"
        )


# Attendance

def load_attendance():
    global attendance_records
    try:
        with open("attendance.csv", "r", newline="") as file:
            reader = csv.DictReader(file)
            attendance_records = list(reader)

    except FileNotFoundError:
        attendance_records = []


def save_attendance():

    with open("attendance.csv", "w", newline="") as file:

        fieldnames = ["Employee ID","Date","Arrival Time","Departure Time","Status","Working Hours"]
        writer = csv.DictWriter(file,fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(attendance_records)


def record_attendance(emp_id, date, arrival, departure):

    # Check if employee exists
    employee_exists = False
    for employee in employees:
        if employee["Employee ID"] == emp_id:
            employee_exists = True
            break

    if not employee_exists:
        print("Employee does not exist.")
        return False

    # Prevent duplicate attendance
    for record in attendance_records:

        if (
            record["Employee ID"] == emp_id
            and record["Date"] == date
        ):
            print("Attendance already recorded for this employee on this date.")

    # Calculate working hours
    try:
        arrival_time = datetime.strptime(arrival, "%H:%M")
        departure_time = datetime.strptime(departure, "%H:%M")
        working_hours = (departure_time - arrival_time).total_seconds() / 3600
        working_hours = round(working_hours, 2)

    except ValueError:
        print("Invalid time format. Use HH:MM.")

    # Determine status
    if arrival > "09:00":
        status = "Late"
    else:
        status = "Present"

    record = {
        "Employee ID": emp_id,
        "Date": date,
        "Arrival Time": arrival,
        "Departure Time": departure,
        "Status": status,
        "Working Hours": working_hours
    }

    attendance_records.append(record)

    save_attendance()

    print("Attendance recorded successfully.")

    return True