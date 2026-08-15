import operations
# import analysis        # uncomment once Phase 3 exists
# import visualization   # uncomment once Phase 3 exists


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
12. Mark an absence / vacation
13. Save data
14. Exit
======================================
"""


def get_menu_choice():
    while True:
        choice = input("Enter your choice (1-14): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= 14:
            return int(choice)
        print("Invalid choice. Please enter a number between 1 and 14.")


def prompt_add_employee():
    employee_id = input("Employee ID: ").strip()
    name = input("Name: ").strip()
    department = input("Department: ").strip()
    operations.add_employee(employee_id, name, department)


def prompt_record_attendance():
    emp_id = input("Employee ID: ").strip()
    date = input("Date (YYYY-MM-DD): ").strip()
    arrival = input("Arrival time (HH:MM): ").strip()
    departure = input("Departure time (HH:MM): ").strip()
    operations.record_attendance(emp_id, date, arrival, departure)


def prompt_mark_absence():
    emp_id = input("Employee ID: ").strip()
    date = input("Date (YYYY-MM-DD): ").strip()
    status = input("Status (Absent/Vacation): ").strip().capitalize()
    operations.mark_absence(emp_id, date, status)


def main():
    # operations.py owns employees/attendance_records as module-level globals.
    # These calls mutate operations.employees / operations.attendance_records
    # in place and return nothing — do NOT assign their result to a variable.
    operations.load_employees()
    operations.load_attendance()

    while True:
        print(MENU_TEXT)
        choice = get_menu_choice()

        if choice == 1:
            prompt_add_employee()

        elif choice == 2:
            operations.display_employees()

        elif choice == 3:
            prompt_record_attendance()

        elif choice == 4:
            # Depends on Phase 2's update_attendance(emp_id, date, new_fields)
            print("Update attendance is not implemented yet (Phase 2).")

        elif choice == 5:
            # Depends on Phase 2's display_employee_attendance(emp_id)
            print("Display employee attendance is not implemented yet (Phase 2).")

        elif choice == 6:
            # Depends on Phase 2's search_attendance_by_date(date)
            print("Search attendance by date is not implemented yet (Phase 2).")

        elif choice == 7:
            # Depends on Phase 2's calculate_attendance_percentage(emp_id)
            print("Calculate attendance percentage is not implemented yet (Phase 2).")

        elif choice == 8:
            # Depends on Phase 3's analysis.display_late_employees()
            print("Display late employees is not implemented yet (Phase 3).")

        elif choice == 9:
            # Depends on Phase 3's analysis.display_frequently_absent_employees()
            print("Display frequently absent employees is not implemented yet (Phase 3).")

        elif choice == 10:
            # Depends on Phase 3's analysis.monthly_report()
            print("Monthly report is not implemented yet (Phase 3).")

        elif choice == 11:
            # Depends on Phase 3's visualization chart functions
            print("Attendance charts are not implemented yet (Phase 3).")

        elif choice == 12:
            prompt_mark_absence()

        elif choice == 13:
            operations.save_employees()
            operations.save_attendance()
            print("Data saved.")

        elif choice == 14:
            operations.save_employees()
            operations.save_attendance()
            print("Data saved. Goodbye!")
            break


if __name__ == "__main__":
    main()