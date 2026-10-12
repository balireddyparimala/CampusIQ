import pandas as pd
from pathlib import Path

# -----------------------------------------
# 1. DEFINE PROJECT DIRECTORIES
# -----------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_DIR / "data"
PROCESSED_DIR = PROJECT_DIR / "processed"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


# -----------------------------------------
# 2. LOAD ALL SEVEN DATASETS
# -----------------------------------------

academic = pd.read_csv(DATA_DIR / "academic_data.csv")

attendance = pd.read_csv(DATA_DIR / "attendance_data.csv")

lms = pd.read_csv(DATA_DIR / "lms_data.csv")

engagement = pd.read_csv(DATA_DIR / "engagement_data.csv")

placement = pd.read_csv(DATA_DIR / "placement_data.csv")

skills = pd.read_csv(DATA_DIR / "skills_data.csv")

feedback = pd.read_csv(DATA_DIR / "feedback_data.csv")


# -----------------------------------------
# 3. CHECK THE INPUT DATA
# -----------------------------------------

datasets = {
    "Academic": academic,
    "Attendance": attendance,
    "LMS": lms,
    "Engagement": engagement,
    "Placement": placement,
    "Skills": skills,
    "Feedback": feedback
}

print("DATASET VALIDATION")
print("-" * 40)

for name, df in datasets.items():

    print(
        f"{name}: {len(df)} records, "
        f"{df['student_id'].nunique()} unique students"
    )

    if df["student_id"].isna().any():
        raise ValueError(
            f"{name} contains missing student IDs."
        )

    if df["student_id"].duplicated().any():
        raise ValueError(
            f"{name} contains duplicate student IDs."
        )


# -----------------------------------------
# 4. MERGE THE SEVEN DATASETS
# -----------------------------------------

student_data = academic.copy()

other_datasets = [
    attendance,
    lms,
    engagement,
    placement,
    skills,
    feedback
]

for df in other_datasets:

    student_data = student_data.merge(
        df,
        on="student_id",
        how="left",
        validate="one_to_one"
    )


# -----------------------------------------
# 5. VALIDATE THE INTEGRATED DATA
# -----------------------------------------

print("\nINTEGRATION VALIDATION")
print("-" * 40)

print("Total student records:", len(student_data))

print(
    "Unique student IDs:",
    student_data["student_id"].nunique()
)

print(
    "Total columns:",
    len(student_data.columns)
)

print(
    "Missing values:",
    student_data.isna().sum().sum()
)

if student_data["student_id"].duplicated().any():
    raise ValueError(
        "Duplicate student IDs found after integration."
    )

if len(student_data) != len(academic):
    raise ValueError(
        "The integrated record count does not match the academic dataset."
    )


# -----------------------------------------
# 6. SAVE THE INTEGRATED DATASET
# -----------------------------------------

output_file = PROCESSED_DIR / "integrated_student_data.csv"

student_data.to_csv(output_file, index=False)

print("\nIntegrated dataset saved successfully!")
print(output_file)


# -----------------------------------------
# 7. DISPLAY SAMPLE RECORDS
# -----------------------------------------

print("\nFIRST FIVE INTEGRATED STUDENT RECORDS")
print("-" * 40)

print(student_data.head().to_string(index=False))

print("\nINTEGRATED COLUMN NAMES")
print(list(student_data.columns))