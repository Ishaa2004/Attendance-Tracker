## Employee Performance and task completion tracker

- This script provides a Flask-based API Employee performance and task completion tracker that helps track employee performance 
  based on tasks completed, attendance, and task complexity. It also supports team-level comparison.

- You can upload CSV or Excel files containing employee data and get calculated results back via an API.

## Why Performance Analysis Matters
Employee performance tracking goes beyond just attendance—it gives organizations a data-driven view of productivity, accountability, and overall efficiency. 
By combining factors like task completion, task complexity, overtime hours and attendance consistency, this tool helps convert raw data into actionable insights.

## url

- http://0.0.0.0:8050

## features

- Upload .csv or .xlsx files to analyze employee performance.
- Calculates performance scores based on:
    - Task completion
    - Task complexity (Easy, Average, Hard)
    - Attendance
    - Overtime hours
- Compares team-level average scores.
- Gives a final score and a performance status:
    - Excellent (>=90)
    - Good (>=75)
    - Needs Improvement (<75)

## Prerequisites

- Python 3.7+
- FastAPI
- Employees Data
- Pandas
- Openpyxl

## Installation:
- Install the dependencies:
   pip install fastapi pandas

## Fields required in the Excel or CSV file
   - Employee ID
   - Employee Name
   - Total Tasks
   - Completed Tasks
   - Attendance Days
   - Total Working Days
   - Task Complexity
   - Expected Hours
   - Actual Hours
   - Teams

## Usage

## 1. Start the FastAPI server
python main.py

## 2. API endpoints
  ## 1. For overall performance of employees 
         - Endpoint: '/upload'
         - Method: 'POST'
         - Description: Provides the information about all the employees and the overall performance comparison based on performance scores.
         
         ## Request
            - Under Body > form-data:
            - Key: file → Type: File → Select your .csv or .xlsx

         ## Response
            - {
                 "Employee ID": "101",
                 "Employee Name": "Alice",
                 "Team": "Team A",
                 "Final Score": 87.5,
                 "Performance Status": "Good",
                 "Task Complexity": "Average",
                 "Expected Hours": 160,
                 "Total Hours Worked": 165,
                 "Overtime Hours": 5,
                 "Overtime Bonus": 0.31
              }
 
    ## 2. For team based comparison
          - Endpoint: '/upload-team'
          - Method: 'POST'
          - Description: Provides comparison based on teams
     
          ## Request
            - Under Body > form-data:
            - Key: file → Type: File → Select your .csv or .xlsx

          ## Response
            - {
               "team": [
                   {
                     "Team": "Team A",
                     "Average Final Score": 87.45,
                     "Total Employees": 2
                   },
                  {
                     "Team": "Team B",
                     "Average Final Score": 81.30,
                     "Total Employees": 2
                  }
               ]
             }

## Notes
- Ensure that you are providing a proper excel or csv file.
- The file should have all the fields.


