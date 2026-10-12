import pandas as pd
from pathlib import Path


# -----------------------------------------
# 1. PROJECT DIRECTORIES
# -----------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = PROJECT_DIR / "processed" / "integrated_student_data.csv"

OUTPUT_FILE = PROJECT_DIR / "processed" / "student_scores.csv"


# -----------------------------------------
# 2. LOAD INTEGRATED STUDENT DATA
# -----------------------------------------

student_data = pd.read_csv(INPUT_FILE)

print("Integrated student data loaded successfully.")
print("Number of students:", len(student_data))


# -----------------------------------------
# 3. NORMALIZE INDICATORS
# -----------------------------------------

# CGPA is out of 10, so convert it to 0-100.
student_data["cgpa_score"] = (
    student_data["cgpa"].clip(0, 10) / 10 * 100
)

# Internal marks are already on a 0-100 scale.
student_data["internal_score"] = (
    student_data["internal_marks"].clip(0, 100)
)

# Attendance is already on a 0-100 scale.
student_data["attendance_score"] = (
    student_data["attendance_percentage"].clip(0, 100)
)

# LMS activity combines login frequency and assignment completion.
# Login frequency is capped at 15 logins per week.
student_data["lms_score"] = (
    (
        student_data["logins_per_week"].clip(0, 15) / 15 * 100
    ) * 0.30
    +
    student_data["assignment_completion"].clip(0, 100) * 0.70
)

# Engagement combines events and certifications.
# Event participation is capped at 10 events.
# Certifications are capped at 5.
student_data["engagement_score"] = (
    (
        student_data["events_attended"].clip(0, 10) / 10 * 100
    ) * 0.50
    +
    (
        student_data["certifications"].clip(0, 5) / 5 * 100
    ) * 0.50
)

# Skills score combines technical and communication skills.
student_data["skills_score"] = (
    student_data["technical_skills"].clip(0, 100) * 0.60
    +
    student_data["communication_skills"].clip(0, 100) * 0.40
)

# Feedback is rated from 1 to 5.
# Convert it to a 0-100 scale.
student_data["feedback_score"] = (
    student_data["satisfaction_score"].clip(1, 5) / 5 * 100
)


# -----------------------------------------
# 4. CALCULATE STUDENT SUCCESS SCORE
# -----------------------------------------

student_data["student_success_score"] = (
    student_data["cgpa_score"] * 0.25
    +
    student_data["attendance_score"] * 0.20
    +
    student_data["internal_score"] * 0.15
    +
    student_data["lms_score"] * 0.10
    +
    student_data["engagement_score"] * 0.10
    +
    student_data["skills_score"] * 0.15
    +
    student_data["feedback_score"] * 0.05
).round(2)


# -----------------------------------------
# 5. CALCULATE PLACEMENT READINESS SCORE
# -----------------------------------------

student_data["placement_readiness_score"] = (
    student_data["aptitude_score"].clip(0, 100) * 0.25
    +
    student_data["coding_score"].clip(0, 100) * 0.25
    +
    student_data["mock_interview_score"].clip(0, 100) * 0.20
    +
    student_data["technical_skills"].clip(0, 100) * 0.15
    +
    student_data["communication_skills"].clip(0, 100) * 0.10
    +
    student_data["cgpa_score"] * 0.05
).round(2)


# -----------------------------------------
# 6. CHECK SCORE VALIDITY
# -----------------------------------------

score_columns = [
    "student_success_score",
    "placement_readiness_score"
]

for column in score_columns:

    if not student_data[column].between(0, 100).all():
        raise ValueError(
            f"Invalid score detected in {column}."
        )


# -----------------------------------------
# 7. SAVE SCORED STUDENT DATA
# -----------------------------------------

student_data.to_csv(OUTPUT_FILE, index=False)

print("\nScoring completed successfully!")

print("\nAverage Student Success Score:")
print(student_data["student_success_score"].mean().round(2))

print("\nAverage Placement Readiness Score:")
print(student_data["placement_readiness_score"].mean().round(2))

print("\nFirst five student scores:")

print(
    student_data[
        [
            "student_id",
            "cgpa",
            "attendance_percentage",
            "student_success_score",
            "placement_readiness_score"
        ]
    ].head().to_string(index=False)
)

print("\nSaved scored dataset to:")
print(OUTPUT_FILE)