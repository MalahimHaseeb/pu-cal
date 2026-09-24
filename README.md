# PU GPA Calculator

A simple Streamlit app to calculate your semester GPA and CGPA using the official University of the Punjab grading scale.

Built this because I got tired of doing the math by hand every semester. You punch in your courses, credit hours and marks, and it does the rest, including combining it with your CGPA from previous semesters.

## Features

- Add courses with credit hours and marks percentage, get the letter grade and GPA instantly
- Enter your CGPA and total credit hours from before, then add the new semester to see your updated CGPA
- Separate tab if you just want to calculate CGPA from a list of semester GPAs
- Uses PU's actual grading table, not some generic 4.0 scale

## Grading Scale

| Marks % | Grade | Points |
|---|---|---|
| 85 and above | A | 4.00 |
| 80-84 | A- | 3.70 |
| 75-79 | B+ | 3.30 |
| 70-74 | B | 3.00 |
| 65-69 | B- | 2.70 |
| 61-64 | C+ | 2.30 |
| 58-60 | C | 2.00 |
| 55-57 | C- | 1.70 |
| 50-54 | D | 1.00 |
| Below 50 | F | 0.00 |

Source: [PU official grading rules](https://pu.edu.pk/dpcc/rule_grading.htm)

## Running it locally

```bash
git clone https://github.com/MalahimHaseeb/pu-cal
cd pu-cal
pip install -r requirements.txt
streamlit run main.py
```

It'll open in your browser at `localhost:8501`.

## Tech

Just Python and Streamlit. No backend, no database, everything runs in your browser session.

## Note

Minimum CGPA for a BS degree at PU is 2.00. The app flags it if your updated CGPA drops below that.