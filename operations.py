import csv
from datetime import datetime

# THE GLOBALS WE USE
employees = []
attendance_records = []
start_time="09:00"


def load_employees():
    global employees #global to have the ability to reflect on the employees list globally
    try:
        with open("employees.csv", "r", newline="") as file:
            reader = csv.DictReader(file) #return from CSV as a dictionary
            #header is the key while the value is the data
            employees = list(reader)# auto append the dictionaries

    except FileNotFoundError:
        employees = []


def save_employees():
    with open("employees.csv", "w", newline="") as file:
        fieldnames = ["Employee ID", "Name", "Department"]#defines a system for the
        #CSV to follow along, like to look for these keys and grab their data
        writer = csv.DictWriter(file,fieldnames=fieldnames)
        writer.writeheader()#define the headers of the csv file
        writer.writerows(employees)#now puts in the actual data


def add_employee(employee_id, name, department):
    # Validate empty fields and using the not opperand to invert them
    if not employee_id or not name or not department:
        print("All fields are required.")
        return False

    # Prevent duplicate Employee ID
    for employee in employees:
        if employee["Employee ID"] == employee_id:#employee is a list holding dictionaries
            #of the employees data so accessing a data would be through indexing
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

def determine_status(arrival):
    try:
        arrival_time = datetime.strptime(arrival, "%H:%M")
        start = datetime.strptime(start_time, "%H:%M")
    except ValueError:
        print("Invalid arrival time format.")
        return "null"

    if arrival_time > start:
        return "Late"
    else:
        return "Present"

def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, "%d-%m-%Y")
        return True
    except (ValueError, TypeError):
        return False

def is_valid_status(status):
    return status in {"Present", "Late", "Absent", "Vacation"}

def mark_absence(emp_id, date, status):

    # Check employee exists
    employee_exists = False
    for employee in employees:
        if employee["Employee ID"] == emp_id:
            employee_exists = True
            break

    if not employee_exists:
        print("Employee does not exist.")
        return False

    # Validate status
    if status not in ("Absent", "Vacation"):
        print("Invalid status. Must be 'Absent' or 'Vacation'.")
        return False

    # Prevent duplicate record for same employee
    for record in attendance_records:
        if record["Employee ID"] == emp_id and record["Date"] == date:
            print("Attendance already recorded for this employee on this date.")
            return False

    record = {
        "Employee ID": emp_id,
        "Date": date,
        "Arrival Time": "",
        "Departure Time": "",
        "Status": status,
        "Working Hours": 0
    }

    attendance_records.append(record)
    save_attendance()

    print("Absence recorded successfully.")
    return True

def record_attendance(emp_id, date, arrival, departure):#date format must be %d-%m-%Y

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
    # The prevention happens logically b4 we hit the save part
    for record in attendance_records:

        if (
            record["Employee ID"] == emp_id and record["Date"] == date
        ):
            print("Attendance already recorded for this employee on this date.")
            return False

    # Calculate working hours
    try:
        arrival_time = datetime.strptime(arrival, "%H:%M")
        departure_time = datetime.strptime(departure, "%H:%M")
        working_hours = (departure_time - arrival_time).total_seconds() / 3600
        working_hours = round(working_hours, 2)
        # A disaster is on its way if an employee sumbits a departure time before arriving

    except ValueError:
        print("Invalid time format. Use HH:MM.")
        return False
        
    status = determine_status(arrival)

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

 
def update_attendance(emp_id, date, new_fields):
    target_record = None
    # Find the record to update
    for record in attendance_records:
        if record["Employee ID"] == emp_id and record["Date"] == date:
            target_record = record
            break
        
    if not target_record:
        print("Attendance record not found.")
        return False

    # Update the fields
    for field, val in new_fields.items():
        if field == "Status":
            if not is_valid_status(val):
                print(f"Invalid status value: {val}")
                return False
            target_record["Status"] = val
        elif field == "Arrival Time":
            target_record["Arrival Time"] = val
        elif field == "Departure Time":
            target_record["Departure Time"] = val

    if "Arrival Time" in new_fields or "Departure Time" in new_fields:
        arr = target_record.get("Arrival Time", "")
        dep = target_record.get("Departure Time", "")
        if arr and dep:
            try:
                arr_dt = datetime.strptime(arr, "%H:%M")
                dep_dt = datetime.strptime(dep, "%H:%M")
                wh = (dep_dt - arr_dt).total_seconds() / 3600
                target_record["Working Hours"] = round(wh, 2)
            except ValueError:
                print("Invalid time format in record.")
                return False
        
        if "Status" not in new_fields:
            target_record["Status"] = determine_status(arr)

    save_attendance()
    print("Attendance record updated successfully.")
    return True


def display_employee_attendance(emp_id):
    emp_exists = any(emp["Employee ID"] == emp_id for emp in employees)
    if not emp_exists:
        print(f"Employee with ID {emp_id} does not exist.")
        return

    records = [r for r in attendance_records if r["Employee ID"] == emp_id]
    if not records:
        print(f"No attendance records found for Employee ID: {emp_id}")
        return

    print(f"\n--- Attendance Records for Employee ID: {emp_id} ---")
    for r in records:
        print(
            f"Date: {r['Date']} | "
            f"Arrival: {r['Arrival Time'] or 'N/A'} | "
            f"Departure: {r['Departure Time'] or 'N/A'} | "
            f"Status: {r['Status']} | "
            f"Working Hours: {r['Working Hours']}"
        )


def search_attendance_by_date(date):
    if not is_valid_date(date):
        print("Invalid date format. Use DD-MM-YYYY.")
        return

    records = [r for r in attendance_records if r["Date"] == date]
    if not records:
        print(f"No attendance records found for Date: {date}")
        return

    print(f"\n--- Attendance Records for Date: {date} ---")
    for r in records:
        print(
            f"Employee ID: {r['Employee ID']} | "
            f"Arrival: {r['Arrival Time'] or 'N/A'} | "
            f"Departure: {r['Departure Time'] or 'N/A'} | "
            f"Status: {r['Status']} | "
            f"Working Hours: {r['Working Hours']}"
        )


def calculate_attendance_percentage(emp_id):
    records = [r for r in attendance_records if r["Employee ID"] == emp_id]
    if not records:
        print(f"No attendance records found for Employee ID: {emp_id}")
        return 0.0

    present_days = sum(1 for r in records if r["Status"] in ("Present", "Late"))
    total_days = sum(1 for r in records if r["Status"] in ("Present", "Late", "Absent"))

    if total_days == 0:
        percentage = 100.0
    else:
        percentage = (present_days / total_days) * 100

    if percentage < 75.0:
        print(f"[WARNING] Attendance percentage for Employee {emp_id} is {percentage:.2f}%, which is below the 75% threshold!")

    return round(percentage, 2)