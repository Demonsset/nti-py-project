import numpy as np
import pandas as pd
import operations


LATE_THRESHOLD = 3
ABSENT_THRESHOLD = 3




def _employees_df():
    return pd.DataFrame(operations.employees)
#output should look like this 
# Employee ID          Name Department
# 0           1   Amir Hassan          IT
# 1           2   Sara Youssef         HR


def _attendance_df():
    return pd.DataFrame(operations.attendance_records)


def _merged_df():# why merged? BECAUSE THE PROJECT ASKED FOR IT
   
    emp_df = _employees_df()
    att_df = _attendance_df()

    if emp_df.empty or att_df.empty:#return true if empty rows
        return pd.DataFrame()#what ? you wanna remove me DO NOT merged df is used down below and they below a data frame 
    #even if u will return an empty one



    # Working Hours from CSV are strings need to convert them to numberss
    att_df["Working Hours"] = pd.to_numeric(att_df["Working Hours"])

    merged = pd.merge(emp_df, att_df)# there are 4 types(using attributes ='how') if i want it to be further customised but no 
    return merged


def numpy_summary():

    merged = _merged_df()# return zero values cuz merged is expected to return 4 values so we did so but dict

    if merged.empty:
        return {
            "avg_attendance_pct": 0.0,
            "max_absence_count": 0,
            "max_lateness_count": 0,
            "avg_working_hours": 0.0,
        }

    emp_ids = merged["Employee ID"].unique()#YES outside help was utilised to get to this unique method 

    attendance_pcts = []
    absence_counts = []
    lateness_counts = []

    for emp_id in emp_ids:
        records = []
        for row in operations.attendance_records:
            if row["Employee ID"] == emp_id:
                records.append(row)

        present_days = 0
        for r in records:
            if r["Status"] == "Present":
                present_days += 1
        
        late_days = 0
        for r in records:
            if r["Status"] == "Late":
                late_days += 1
        
        absent_days = 0
        for r in records:
            if r["Status"] == "Absent":
                absent_days += 1
        total_days = present_days + absent_days

        if total_days > 0:
            pct = present_days / total_days * 100
        else:
            pct = 0

        attendance_pcts.append(pct)
        absence_counts.append(absent_days)
        lateness_counts.append(late_days)
#VIP why we use list instead of arrays from the very start ?
    attendance_pcts = np.array(attendance_pcts)
    absence_counts = np.array(absence_counts)
    lateness_counts = np.array(lateness_counts)
    working_hours = merged["Working Hours"].to_numpy()# numpy can easily handles the panda series so why both converting it?
    #to have a sense of CLEAN CODE
    
    return {
        "avg_attendance_pct": round(np.mean(attendance_pcts), 2),
        "max_absence_count": np.max(absence_counts),
        "max_lateness_count": np.max(lateness_counts),
        "avg_working_hours": round(np.mean(working_hours), 2),
    }
    


def pandas_report(filter_by="none", filter_value="none"):
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

    filtered = merged
    if filter_by == "employee":
        filtered = merged[merged["Employee ID"] == str(filter_value)]
    elif filter_by == "date":
        filtered = merged[merged["Date"] == str(filter_value)]
    elif filter_by == "department":
        filtered = merged[merged["Department"] == str(filter_value)]
    elif filter_by == "status":
        filtered = merged[merged["Status"] == str(filter_value)]

  
    counts = {}

    for dept, statuses in merged.groupby("Department")["Status"]:
        counts[dept] = {}
        for status in statuses:
            if status not in counts[dept]:
                counts[dept][status] = 0
            counts[dept][status] += 1

    status_by_department = pd.DataFrame(counts).fillna(0).astype(int)

  
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

  
    if not sorted_pct.empty:
        merged = _merged_df()
        dept_by_id = merged.drop_duplicates("Employee ID").set_index("Employee ID")["Department"]
        sorted_pct = sorted_pct.copy()
        sorted_pct["Department"] = sorted_pct["Employee ID"].map(dept_by_id)
        dept_comparison = sorted_pct.groupby("Department")["Attendance %"].mean().round(2)
        dept_comparison = dept_comparison.sort_values(ascending=False)

        print("\n--- Department attendance comparison (avg attendance %) ---")
        print(dept_comparison.to_string())