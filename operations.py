import csv
import os

EMPLOYEES_FILE = "employees.csv"
EMPLOYEE_FIELDS = ["Employee ID", "Name", "Department"]


def load_employees():
    """Reads employees.csv and returns a list of employee dictionaries."""
    employees = []
    if os.path.exists(EMPLOYEES_FILE):
        with open(EMPLOYEES_FILE, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                employees.append(row)
    return employees


def save_employees(employees):
    """Writes the list of employee dictionaries back to employees.csv."""
    with open(EMPLOYEES_FILE, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=EMPLOYEE_FIELDS)
        writer.writeheader()
        for emp in employees:
            writer.writerow(emp)