import matplotlib.pyplot as plt
import operations


def chart_attendance_by_employee():#BAAAAR CHART
    names = []
    percentages = []

    for employee in operations.employees:
        emp_id = employee["Employee ID"]
        pct = operations.calculate_attendance_percentage(emp_id)
        names.append(employee["Name"])
        percentages.append(pct)

    if not names:
        print("No employee data to chart.")
        return

    plt.figure()
    plt.bar(names, percentages, color="steelblue")
    plt.xlabel("Employee")
    plt.ylabel("Attendance %")
    plt.title("Attendance Percentage by Employee")
    plt.xticks(rotation=45, ha="right")#horizontal alignment
    plt.grid()
    plt.tight_layout()
    plt.show()


def chart_status_breakdown():
    counts = {"Present": 0, "Late": 0, "Absent": 0, "Vacation": 0}

    for record in operations.attendance_records:
        status = record["Status"]
        if status in counts:
            counts[status] += 1

    labels = [status for status, count in counts.items() if count > 0]
    values = []
    for count in counts.values():
     if count > 0:
        values.append(count)
     if not values:
        print("No attendance records to chart.")
        return

    plt.figure()
    plt.pie(values, labels=labels, autopct="%1.1f%%")
    plt.title("Attendance Status Breakdown")
    plt.tight_layout()
    plt.show()


def chart_absences_by_department():
    
    dept_by_id = {}
    for emp in operations.employees:
     dept_by_id[emp["Employee ID"]] = emp["Department"]

    dept_absences = {}
    for record in operations.attendance_records:
        if record.get("Status") == "Absent":
            emp_id = record["Employee ID"]
            department = dept_by_id.get(emp_id)
            if department:
                dept_absences[department] = dept_absences.get(department, 0) + 1

    if not dept_absences:
        print("No absence data to chart.")
        return

    departments = list(dept_absences.keys())
    counts = list(dept_absences.values())

    plt.figure()
    plt.bar(departments, counts, color="indianred")
    plt.xlabel("Department")
    plt.ylabel("Absences")
    plt.title("Absences by Department")
    plt.grid()
    plt.tight_layout()
    plt.show()


def show_all_charts():
    chart_attendance_by_employee()
    chart_status_breakdown()
    chart_absences_by_department()