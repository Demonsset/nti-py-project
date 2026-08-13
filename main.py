import operations
import analysis
import visualization


MENU_TEXT = """
==== Employee Attendance System ====
 1. Add an employee
 2. Display employees
 3. Record attendance
 4. Update attendance
 5. Display employee attendance
 6. Search attendance by date
 7. Calculate attendance percentage
 8. Display late employees
 9. Display frequently absent employees
10. Generate a monthly report
11. Show attendance charts
12. Save data
13. Exit
======================================
"""


def get_menu_choice():
    while True:
        choice = input("Enter your choice (1-13): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= 13:
            return int(choice)
        print("Invalid choice. Please enter a number between 1 and 13.")


def main():
    employees = operations.load_employees()
    attendance = operations.load_attendance()

    while True:
        print(MENU_TEXT)
        choice = get_menu_choice()

        if choice == 1:
            operations.add_employee(employees)

        elif choice == 2:
            operations.display_employees(employees)

        elif choice == 3:
            operations.record_attendance(employees, attendance)

        elif choice == 4:
            operations.update_attendance(attendance)

        elif choice == 5:
            emp_id = input("Enter Employee ID: ").strip()
            operations.display_employee_attendance(attendance, emp_id)

        elif choice == 6:
            date = input("Enter date (YYYY-MM-DD): ").strip()
            operations.search_attendance_by_date(attendance, date)

        elif choice == 7:
            emp_id = input("Enter Employee ID: ").strip()
            pct = operations.calculate_attendance_percentage(attendance, emp_id)
            print(f"Attendance percentage: {pct:.2f}%")

        elif choice == 8:
            analysis.display_late_employees(attendance)

        elif choice == 9:
            analysis.display_frequently_absent_employees(attendance)

        elif choice == 10:
            analysis.monthly_report(employees, attendance)

        elif choice == 11:
            visualization.chart_attendance_by_employee(attendance)
            visualization.chart_status_breakdown(attendance)
            visualization.chart_absences_by_department(employees, attendance)

        elif choice == 12:
            operations.save_employees(employees)
            operations.save_attendance(attendance)
            print("Data saved.")

        elif choice == 13:
            operations.save_employees(employees)
            operations.save_attendance(attendance)
            print("Data saved. Goodbye!")
            break


if __name__ == "__main__":
    main()