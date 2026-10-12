import pandas as pd
from pathlib import Path


# -----------------------------------------
# 1. PROJECT DIRECTORIES
# -----------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_DIR
    / "processed"
    / "student_risk_analysis.csv"
)

OUTPUT_FILE = (
    PROJECT_DIR
    / "processed"
    / "student_segments.csv"
)


# -----------------------------------------
# 2. LOAD STUDENT RISK DATA
# -----------------------------------------

students = pd.read_csv(INPUT_FILE)

print("Student risk data loaded successfully.")
print("Total students:", len(students))


# -----------------------------------------
# 3. ASSIGN STUDENT SEGMENTS
# -----------------------------------------

def assign_segment(row):

    success_score = row["student_success_score"]

    placement_score = row["placement_readiness_score"]

    academic_risk = row["academic_risk"]

    placement_risk = row["placement_risk"]

    # Segment 1: Strong academics but low placement readiness
    if success_score >= 65 and placement_score < 60:
        return "Strong Academics, Low Placement Readiness"

    # Segment 2: Academic support required
    elif academic_risk == "At Risk":
        return "Academic Support Needed"

    # Segment 3: Placement preparation required
    elif placement_risk == "At Risk":
        return "Placement Preparation Needed"

    # Segment 4: Doing well in both areas
    else:
        return "Doing Well in Both Areas"


students["student_segment"] = students.apply(
    assign_segment,
    axis=1
)


# -----------------------------------------
# 4. RECOMMEND INTERVENTIONS
# -----------------------------------------

def recommend_intervention(row):

    segment = row["student_segment"]

    recommendations = {
        "Strong Academics, Low Placement Readiness":
            "Provide aptitude practice, coding exercises, "
            "and mock interview sessions.",

        "Academic Support Needed":
            "Arrange faculty mentoring, review subject "
            "performance, and prepare an academic improvement plan.",

        "Placement Preparation Needed":
            "Provide placement training, coding practice, "
            "resume preparation, and mock interviews.",

        "Doing Well in Both Areas":
            "Encourage advanced projects, internships, "
            "certifications, and leadership activities."
    }

    return recommendations[segment]


students["recommended_intervention"] = students.apply(
    recommend_intervention,
    axis=1
)


# -----------------------------------------
# 5. SAVE THE RESULTS
# -----------------------------------------

students.to_csv(OUTPUT_FILE, index=False)


# -----------------------------------------
# 6. DISPLAY SEGMENT SUMMARY
# -----------------------------------------

print("\nSTUDENT SEGMENTATION COMPLETED")
print("-" * 50)

segment_summary = (
    students["student_segment"]
    .value_counts()
    .rename_axis("Student Segment")
    .reset_index(name="Number of Students")
)

print(segment_summary.to_string(index=False))


# -----------------------------------------
# 7. DISPLAY SAMPLE RECOMMENDATIONS
# -----------------------------------------

print("\nSAMPLE STUDENT RECOMMENDATIONS")
print("-" * 50)

columns_to_display = [
    "student_id",
    "student_success_score",
    "placement_readiness_score",
    "student_segment",
    "recommended_intervention"
]

print(
    students[columns_to_display]
    .head(10)
    .to_string(index=False)
)


print("\nResults saved to:")
print(OUTPUT_FILE)