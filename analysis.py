import numpy as np
import pandas as pd

import operations

# Spec (image 2) never defines these two thresholds -- PROJECT.md flagged
# them as a team decision that was never written down. Locked here so
# there's one place to change them if the team agrees on different numbers.
LATE_THRESHOLD = 3
ABSENT_THRESHOLD = 3

ATTENDANCE_PCT_WARNING = 75.0  # matches operations.calculate_attendance_percentage


def _employees_df():
    return pd.DataFrame(operations.employees)


def _attendance_df():
    return pd.DataFrame(operations.attendance_records)


def _merged_df():
    """
    Merge attendance onto employees (image 1: 'Merge employee and
    attendance records', pandas requirements).

    Uses an INNER merge on Employee ID, not a left merge. Attendance
    records for an Employee ID that doesn't exist in employees.csv
    (e.g. leftover/orphaned rows) have no real employee to report on --
    an inner merge drops them instead of producing a Name: NaN row in
    every report built on top of this function.
    """
    emp_df = _employees_df()
    att_df = _attendance_df()

    if emp_df.empty or att_df.empty:
        return pd.DataFrame()

    # Working Hours arrives from CSV as strings; every numeric report
    # downstream needs it as float.
    att_df = att_df.copy()
    att_df["Working Hours"] = pd.to_numeric(att_df["Working Hours"], errors="coerce").fillna(0.0)

    merged = pd.merge(emp_df, att_df, on="Employee ID", how="inner")
    return merged


def numpy_summary():
    """
    NumPy requirements (image 2):
      - average attendance percentage
      - max absence count / max lateness count (any single employee)
      - average working hours

    Returns a dict of the three stats, computed with NumPy over the
    per-employee arrays (not just pandas .mean()/.max(), since this is
    explicitly the NumPy-requirements function).
    """
    merged = _merged_df()

    if merged.empty:
        return {
            "avg_attendance_pct": 0.0,
            "max_absence_count": 0,
            "max_lateness_count": 0,
            "avg_working_hours": 0.0,
        }

    emp_ids = merged["Employee ID"].unique()

    attendance_pcts = []
    absence_counts = []
    lateness_counts = []

    for emp_id in emp_ids:
        records = merged[merged["Employee ID"] == emp_id]

        present_days = (records["Status"].isin(["Present", "Late"])).sum()
        absent_days = (records["Status"] == "Absent").sum()
        late_days = (records["Status"] == "Late").sum()
        total_days = present_days + absent_days

        pct = (present_days / total_days * 100) if total_days > 0 else 100.0

        attendance_pcts.append(pct)
        absence_counts.append(absent_days)
        lateness_counts.append(late_days)

    attendance_pcts = np.array(attendance_pcts, dtype=float)
    absence_counts = np.array(absence_counts, dtype=int)
    lateness_counts = np.array(lateness_counts, dtype=int)
    working_hours = merged["Working Hours"].to_numpy(dtype=float)

    return {
        "avg_attendance_pct": round(float(np.mean(attendance_pcts)), 2),
        "max_absence_count": int(np.max(absence_counts)),
        "max_lateness_count": int(np.max(lateness_counts)),
        "avg_working_hours": round(float(np.mean(working_hours)), 2),
    }


def pandas_report(filter_by=None, filter_value=None):
    """
    pandas requirements (image 2):
      - filter attendance by employee, date, department, or status
      - group attendance by department
      - count each attendance status
      - sort employees by attendance percentage
      - merge employee and attendance records

    filter_by: one of "employee", "date", "department", "status", or None
    filter_value: the value to filter on, required if filter_by is set

    Returns a dict with the filtered view (if requested), status counts
    per department, and employees sorted by attendance percentage.
    """
    merged = _merged_df()

    if merged.empty:
        return {
            "filtered": pd.DataFrame(),
            "status_by_department": pd.DataFrame(),
            "sorted_by_attendance_pct": pd.DataFrame(),
        }

    # --- Filter ---
    filtered = merged
    if filter_by == "employee":
        filtered = merged[merged["Employee ID"] == str(filter_value)]
    elif filter_by == "date":
        filtered = merged[merged["Date"] == str(filter_value)]
    elif filter_by == "department":
        filtered = merged[merged["Department"] == str(filter_value)]
    elif filter_by == "status":
        filtered = merged[merged["Status"] == str(filter_value)]

    # --- Group by department, count each status ---
    status_by_department = (
        merged.groupby("Department")["Status"]
        .value_counts()
        .unstack(fill_value=0)
    )

    # --- Sort employees by attendance percentage ---
    per_employee = []
    for emp_id, records in merged.groupby("Employee ID"):
        name = records["Name"].iloc[0]
        present_days = (records["Status"].isin(["Present", "Late"])).sum()
        absent_days = (records["Status"] == "Absent").sum()
        total_days = present_days + absent_days
        pct = (present_days / total_days * 100) if total_days > 0 else 100.0
        per_employee.append({"Employee ID": emp_id, "Name": name, "Attendance %": round(pct, 2)})

    sorted_by_attendance_pct = pd.DataFrame(per_employee).sort_values(
        by="Attendance %", ascending=False
    ).reset_index(drop=True)

    return {
        "filtered": filtered,
        "status_by_department": status_by_department,
        "sorted_by_attendance_pct": sorted_by_attendance_pct,
    }


def display_late_employees():
    """Option 8. Lists employees late LATE_THRESHOLD or more times."""
    merged = _merged_df()

    if merged.empty:
        print("No attendance data available.")
        return

    late_counts = merged[merged["Status"] == "Late"].groupby("Employee ID").size()
    late_counts = late_counts[late_counts >= LATE_THRESHOLD]

    if late_counts.empty:
        print(f"No employees late {LATE_THRESHOLD} or more times.")
        return

    names = merged.drop_duplicates("Employee ID").set_index("Employee ID")["Name"]

    print(f"\n--- Employees Late {LATE_THRESHOLD}+ Times ---")
    for emp_id, count in late_counts.sort_values(ascending=False).items():
        print(f"ID: {emp_id} | Name: {names.get(emp_id, 'Unknown')} | Late days: {count}")


def display_frequently_absent_employees():
    """Option 9. Lists employees absent ABSENT_THRESHOLD or more times."""
    merged = _merged_df()

    if merged.empty:
        print("No attendance data available.")
        return

    absent_counts = merged[merged["Status"] == "Absent"].groupby("Employee ID").size()
    absent_counts = absent_counts[absent_counts >= ABSENT_THRESHOLD]

    if absent_counts.empty:
        print(f"No employees absent {ABSENT_THRESHOLD} or more times.")
        return

    names = merged.drop_duplicates("Employee ID").set_index("Employee ID")["Name"]

    print(f"\n--- Employees Absent {ABSENT_THRESHOLD}+ Times ---")
    for emp_id, count in absent_counts.sort_values(ascending=False).items():
        print(f"ID: {emp_id} | Name: {names.get(emp_id, 'Unknown')} | Absent days: {count}")


def monthly_report():
    """
    Option 10. Combines numpy_summary() and pandas_report() into the
    full report required by image 1 / image 2:
      - attendance percentage (per employee, sorted)
      - late days / absent days (department status counts)
      - most punctual employee / most frequently absent employee
      - department attendance comparison
    """
    summary = numpy_summary()
    report = pandas_report()

    sorted_pct = report["sorted_by_attendance_pct"]
    status_by_dept = report["status_by_department"]

    print("\n=== Monthly Report ===")
    print(f"Average attendance percentage: {summary['avg_attendance_pct']}%")
    print(f"Max lateness count (any employee): {summary['max_lateness_count']}")
    print(f"Max absence count (any employee): {summary['max_absence_count']}")
    print(f"Average working hours: {summary['avg_working_hours']}")

    if not status_by_dept.empty:
        print("\n--- Status counts by department ---")
        print(status_by_dept)

    if not sorted_pct.empty:
        print("\n--- Attendance percentage, sorted (highest first) ---")
        print(sorted_pct.to_string(index=False))

        most_punctual = sorted_pct.iloc[0]
        most_absent = sorted_pct.iloc[-1]
        print(f"\nMost punctual employee: {most_punctual['Name']} ({most_punctual['Attendance %']}%)")
        print(f"Most frequently absent employee: {most_absent['Name']} ({most_absent['Attendance %']}%)")

    # Department attendance comparison (image 1: distinct bullet from the
    # status-count table above -- this is attendance % per department,
    # not a raw status count).
    if not sorted_pct.empty:
        merged = _merged_df()
        dept_by_id = merged.drop_duplicates("Employee ID").set_index("Employee ID")["Department"]
        sorted_pct = sorted_pct.copy()
        sorted_pct["Department"] = sorted_pct["Employee ID"].map(dept_by_id)
        dept_comparison = sorted_pct.groupby("Department")["Attendance %"].mean().round(2)
        dept_comparison = dept_comparison.sort_values(ascending=False)

        print("\n--- Department attendance comparison (avg attendance %) ---")
        print(dept_comparison.to_string())