import pandas as pd
from pathlib import Path


# -----------------------------------------
# 1. PROJECT DIRECTORIES
# -----------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = PROJECT_DIR / "processed" / "student_scores.csv"

OUTPUT_FILE = PROJECT_DIR / "processed" / "student_risk_analysis.csv"


# -----------------------------------------
# 2. LOAD STUDENT SCORES
# -----------------------------------------

students = pd.read_csv(INPUT_FILE)

print("Student score data loaded successfully.")
print("Total students:", len(students))


# -----------------------------------------
# 3. IDENTIFY ACADEMIC RISK
# -----------------------------------------

def identify_academic_risk(row):

    reasons = []

    if row["student_success_score"] < 50:
        reasons.append("Low Student Success Score")

    if row["attendance_percentage"] < 75:
        reasons.append("Low Attendance")

    if row["cgpa"] < 6.0:
        reasons.append("Low CGPA")

    if row["backlogs"] >= 2:
        reasons.append("Multiple Backlogs")

    return reasons


students["academic_risk_reasons"] = students.apply(
    identify_academic_risk,
    axis=1
)

students["academic_risk"] = students[
    "academic_risk_reasons"
].apply(
    lambda reasons: "At Risk" if reasons else "Low Risk"
)


# -----------------------------------------
# 4. IDENTIFY PLACEMENT RISK
# -----------------------------------------

def identify_placement_risk(row):

    reasons = []

    if row["placement_readiness_score"] < 60:
        reasons.append("Low Placement Readiness Score")

    if row["coding_score"] < 50:
        reasons.append("Low Coding Score")

    return reasons


students["placement_risk_reasons"] = students.apply(
    identify_placement_risk,
    axis=1
)

students["placement_risk"] = students[
    "placement_risk_reasons"
].apply(
    lambda reasons: "At Risk" if reasons else "Low Risk"
)


# -----------------------------------------
# 5. CREATE HUMAN-READABLE REASONS
# -----------------------------------------

students["academic_risk_reasons"] = students[
    "academic_risk_reasons"
].apply(
    lambda reasons: "; ".join(reasons) if reasons else "No rule triggered"
)

students["placement_risk_reasons"] = students[
    "placement_risk_reasons"
].apply(
    lambda reasons: "; ".join(reasons) if reasons else "No rule triggered"
)


# -----------------------------------------
# 6. SAVE RESULTS
# -----------------------------------------

students.to_csv(OUTPUT_FILE, index=False)


# -----------------------------------------
# 7. DISPLAY SUMMARY
# -----------------------------------------

academic_count = (students["academic_risk"] == "At Risk").sum()

placement_count = (students["placement_risk"] == "At Risk").sum()

print("\nRISK ANALYSIS COMPLETED")
print("-" * 40)

print("Students needing academic review:", academic_count)

print("Students needing placement review:", placement_count)


# -----------------------------------------
# 8. DISPLAY SAMPLE RESULTS
# -----------------------------------------

print("\nFIRST TEN STUDENT RISK RECORDS")
print("-" * 40)

columns_to_display = [
    "student_id",
    "student_success_score",
    "academic_risk",
    "academic_risk_reasons",
    "placement_readiness_score",
    "placement_risk",
    "placement_risk_reasons"
]

print(
    students[columns_to_display]
    .head(10)
    .to_string(index=False)
)


print("\nResults saved to:")
print(OUTPUT_FILE)