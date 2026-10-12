import pandas as pd
import numpy as np
from pathlib import Path

# Set a fixed random seed so results are reproducible
np.random.seed(42)

# Find the CampusIQ project folder
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"

# Create the data folder if it does not exist
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Number of synthetic students
NUM_STUDENTS = 200

# Generate student IDs
student_ids = [
    f"STU{i:03d}"
    for i in range(1, NUM_STUDENTS + 1)
]

# Generate synthetic academic records
academic_data = pd.DataFrame({
    "student_id": student_ids,
    "department": np.random.choice(
        ["Mechanical", "Civil", "EEE", "ECE", "CSE"],
        NUM_STUDENTS
    ),
    "academic_year": np.random.choice(
        ["II Year", "III Year", "IV Year"],
        NUM_STUDENTS
    ),
    "cgpa": np.round(
        np.random.uniform(4.0, 10.0, NUM_STUDENTS),
        2
    ),
    "internal_marks": np.random.randint(
        30, 101, NUM_STUDENTS
    ),
    "backlogs": np.random.randint(
        0, 6, NUM_STUDENTS
    )
})

# Save the academic dataset
output_file = DATA_DIR / "academic_data.csv"

academic_data.to_csv(output_file, index=False)

print("Academic dataset created successfully!")
print(f"Total student records: {len(academic_data)}")
print(f"Saved to: {output_file}")

# Display the first five records
print("\nFirst five academic records:")
print(academic_data.head())
# -----------------------------------------
# DATASET 2: ATTENDANCE DATA
# -----------------------------------------

attendance_data = pd.DataFrame({
    "student_id": student_ids,
    "attendance_percentage": np.random.randint(
        45, 101, NUM_STUDENTS
    )
})

attendance_data.to_csv(
    DATA_DIR / "attendance_data.csv",
    index=False
)


# -----------------------------------------
# DATASET 3: LMS DATA
# -----------------------------------------

lms_data = pd.DataFrame({
    "student_id": student_ids,
    "logins_per_week": np.random.randint(
        0, 16, NUM_STUDENTS
    ),
    "assignment_completion": np.random.randint(
        20, 101, NUM_STUDENTS
    )
})

lms_data.to_csv(
    DATA_DIR / "lms_data.csv",
    index=False
)


# -----------------------------------------
# DATASET 4: ENGAGEMENT DATA
# -----------------------------------------

engagement_data = pd.DataFrame({
    "student_id": student_ids,
    "events_attended": np.random.randint(
        0, 11, NUM_STUDENTS
    ),
    "certifications": np.random.randint(
        0, 6, NUM_STUDENTS
    )
})

engagement_data.to_csv(
    DATA_DIR / "engagement_data.csv",
    index=False
)


# -----------------------------------------
# DATASET 5: PLACEMENT DATA
# -----------------------------------------

placement_data = pd.DataFrame({
    "student_id": student_ids,
    "aptitude_score": np.random.randint(
        20, 101, NUM_STUDENTS
    ),
    "coding_score": np.random.randint(
        15, 101, NUM_STUDENTS
    ),
    "mock_interview_score": np.random.randint(
        20, 101, NUM_STUDENTS
    )
})

placement_data.to_csv(
    DATA_DIR / "placement_data.csv",
    index=False
)


# -----------------------------------------
# DATASET 6: SKILLS DATA
# -----------------------------------------

skills_data = pd.DataFrame({
    "student_id": student_ids,
    "technical_skills": np.random.randint(
        25, 101, NUM_STUDENTS
    ),
    "communication_skills": np.random.randint(
        25, 101, NUM_STUDENTS
    )
})

skills_data.to_csv(
    DATA_DIR / "skills_data.csv",
    index=False
)


# -----------------------------------------
# DATASET 7: FEEDBACK DATA
# -----------------------------------------

feedback_data = pd.DataFrame({
    "student_id": student_ids,
    "satisfaction_score": np.round(
        np.random.uniform(1, 5, NUM_STUDENTS),
        1
    )
})

feedback_data.to_csv(
    DATA_DIR / "feedback_data.csv",
    index=False
)


# -----------------------------------------
# DISPLAY DATA GENERATION RESULTS
# -----------------------------------------

print("\nAll seven datasets created successfully!")

print("Total students:", NUM_STUDENTS)

print("\nFiles created:")

for file_path in sorted(DATA_DIR.glob("*.csv")):
    print(file_path.name)