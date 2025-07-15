import os
import pandas as pd
import io
from fastapi import FastAPI, File, UploadFile
import uvicorn
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Task complexity weights
COMPLEXITY_WEIGHTS = {
    "Easy": 1.0,
    "Average": 1.2,
    "Hard": 1.5
}

# Core performance calculation (returns individual results and team stats)
def calculate_performance(data):
    results = []
    team_stats = {}

    for _, row in data.iterrows():
        total_tasks = row['Total Tasks']
        completed_tasks = row['Completed Tasks']
        attendance = row['Attendance Days']
        total_working_days = row['Total Working Days']
        complexity = row['Task Complexity']
        expected_hours = row['Expected Hours']
        actual_hours = row['Actual Hours']
        team = row.get('Team', 'No Team')

        task_weight = COMPLEXITY_WEIGHTS.get(complexity, 1.0)
        attendance_percentage = (attendance / total_working_days) * 100 if total_working_days > 0 else 0
        attendance_score = attendance_percentage * 0.3
        task_score = ((completed_tasks / total_tasks) * 70 * task_weight) if total_tasks > 0 else 0
        overtime_hours = max(0, actual_hours - expected_hours)
        overtime_bonus = (overtime_hours / expected_hours) * 10 if expected_hours > 0 else 0
        final_score = round(min(task_score + attendance_score + overtime_bonus, 100), 2)

        if final_score >= 90:
            performance = "Excellent"
        elif final_score >= 75:
            performance = "Good"
        else:
            performance = "Needs Improvement"

        results.append({
            "Employee ID": row['Employee ID'],
            "Employee Name": row['Employee Name'],
            "Team": team,
            "Final Score": final_score,
            "Performance Status": performance,
            "Task Complexity": complexity,
            "Expected Hours": expected_hours,
            "Total Hours Worked": actual_hours,
            "Overtime Hours": round(overtime_hours, 2),
            "Overtime Bonus": round(overtime_bonus, 2)
        })

        if team not in team_stats:
            team_stats[team] = {
                "Total Final Score": 0,
                "Total Employees": 0
            }
        team_stats[team]["Total Final Score"] += final_score
        team_stats[team]["Total Employees"] += 1

    performance_order = {"Excellent": 1, "Good": 2, "Needs Improvement": 3}
    results.sort(key=lambda x: performance_order[x["Performance Status"]])

    # Team comparison data
    team_comparison = []
    for team, stats in team_stats.items():
        avg_score = stats["Total Final Score"] / stats["Total Employees"]
        team_comparison.append({
            "Team": team,
            "Average Final Score": round(avg_score, 2),
            "Total Employees": stats["Total Employees"]
        })
    team_comparison.sort(key=lambda x: x["Average Final Score"], reverse=True)

    return {"results": results, "team": team_comparison}


# 🔹 Route: /upload (employee-only performance)
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    file_extension = file.filename.split(".")[-1]

    try:
        if file_extension == "csv":
            data = pd.read_csv(io.StringIO(contents.decode("utf-8")))
        elif file_extension in ["xlsx", "xls"]:
            data = pd.read_excel(io.BytesIO(contents))
        else:
            return {"error": "Unsupported file format. Use CSV or Excel."}
    except Exception as e:
        return {"error": f"Failed to read the file: {str(e)}"}

    required_cols = ["Employee ID", "Employee Name", "Total Tasks", "Completed Tasks",
                     "Attendance Days", "Total Working Days", "Task Complexity",
                     "Expected Hours", "Actual Hours"]

    for col in required_cols:
        if col not in data.columns:
            return {"error": f"Missing required column: {col}"}

    result = calculate_performance(data)
    return {"results": result["results"]}  # only return employee-level data


# 🔹 Route: /upload-team (team-level only)
@app.post("/upload-team")
async def upload_team_comparison(file: UploadFile = File(...)):
    contents = await file.read()
    file_extension = file.filename.split(".")[-1]

    try:
        if file_extension == "csv":
            data = pd.read_csv(io.StringIO(contents.decode("utf-8")))
        elif file_extension in ["xlsx", "xls"]:
            data = pd.read_excel(io.BytesIO(contents))
        else:
            return {"error": "Unsupported file format. Use CSV or Excel."}
    except Exception as e:
        return {"error": f"Failed to read the file: {str(e)}"}

    if "Team" not in data.columns:
        return {"error": "Missing 'Team' column for team-based comparison."}

    result = calculate_performance(data)
    return {"team": result["team"]}  # only return team-based summary


if __name__ == '__main__':
    port = int(os.getenv("FASTAPI_PORT", 8050))
    debug = os.getenv("FASTAPI_DEBUG", "true").lower() == "true"
    
    # Pass app as string for reload to work properly
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=debug)
