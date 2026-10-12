import pandas as pd
import streamlit as st
import plotly.express as px
from pathlib import Path


# =========================================
# 1. PAGE CONFIGURATION
# =========================================

st.set_page_config(
    page_title="CampusIQ | Student Success Analytics",
    page_icon="🎓",
    layout="wide"
)


# =========================================
# 2. PROJECT PATHS
# =========================================

PROJECT_DIR = Path(__file__).resolve().parent

DATA_FILE = (
    PROJECT_DIR
    / "processed"
    / "student_segments.csv"
)


# =========================================
# 3. LOAD STUDENT DATA
# =========================================

@st.cache_data
def load_student_data(file_path):

    df = pd.read_csv(file_path)

    # Convert risk reasons into strings if needed.
    # CSV files normally load these columns as strings.
    df["academic_risk_reasons"] = (
        df["academic_risk_reasons"].fillna("")
    )

    df["placement_risk_reasons"] = (
        df["placement_risk_reasons"].fillna("")
    )

    return df


if not DATA_FILE.exists():

    st.error(
        "Student dataset not found. "
        "Please run the data generation, integration, "
        "scoring, risk analysis, and segmentation programs first."
    )

    st.stop()


students = load_student_data(str(DATA_FILE))


# =========================================
# 4. HEADER
# =========================================

st.title("CampusIQ")
st.subheader(
    "Smart Campus Analytics: "
    "Predict, Optimize & Improve Student Success"
)

st.caption(
    "A data-driven prototype for student support, "
    "academic monitoring, and placement preparation."
)
# ==========================================
# KEY INSIGHTS
# ==========================================

st.header("Key Insights")

total_students = len(students)

academic_risk_count = (
    students["academic_risk"].eq("At Risk").sum()
    if "academic_risk" in students.columns
    else 0
)

placement_risk_count = (
    students["placement_risk"].eq("At Risk").sum()
    if "placement_risk" in students.columns
    else 0
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Students", total_students)

with col2:
    st.metric("Students at Academic Risk", int(academic_risk_count))

with col3:
    st.metric("Students at Placement Risk", int(placement_risk_count))

st.info(
    "Use the filters and Student Explorer below to investigate "
    "individual students and identify suitable interventions."
)
st.divider()


# =========================================
# 5. SIDEBAR FILTERS
# =========================================

st.sidebar.header("Dashboard Filters")

departments = sorted(
    students["department"].dropna().unique().tolist()
)

selected_departments = st.sidebar.multiselect(
    "Department",
    options=departments,
    default=departments
)

academic_years = sorted(
    students["academic_year"].dropna().unique().tolist()
)

selected_years = st.sidebar.multiselect(
    "Academic Year",
    options=academic_years,
    default=academic_years
)

risk_options = [
    "All Students",
    "Academic Risk",
    "Placement Risk",
    "Both Risks",
    "No Risk Flags"
]

selected_risk = st.sidebar.selectbox(
    "Risk Status",
    options=risk_options
)


# =========================================
# 6. APPLY FILTERS
# =========================================

filtered = students[
    students["department"].isin(selected_departments)
    & students["academic_year"].isin(selected_years)
].copy()


if selected_risk == "Academic Risk":

    filtered = filtered[
        filtered["academic_risk"] == "At Risk"
    ]

elif selected_risk == "Placement Risk":

    filtered = filtered[
        filtered["placement_risk"] == "At Risk"
    ]

elif selected_risk == "Both Risks":

    filtered = filtered[
        (filtered["academic_risk"] == "At Risk")
        & (filtered["placement_risk"] == "At Risk")
    ]

elif selected_risk == "No Risk Flags":

    filtered = filtered[
        (filtered["academic_risk"] == "Low Risk")
        & (filtered["placement_risk"] == "Low Risk")
    ]


# =========================================
# 7. KEY PERFORMANCE INDICATORS
# =========================================

st.header("Campus Overview")

if filtered.empty:

    st.warning(
        "No students match the selected filters. "
        "Please change your filter selections."
    )

else:

    total_students = len(filtered)

    average_success = (
        filtered["student_success_score"].mean()
    )

    average_placement = (
        filtered["placement_readiness_score"].mean()
    )

    academic_risk_count = (
        filtered["academic_risk"] == "At Risk"
    ).sum()

    placement_risk_count = (
        filtered["placement_risk"] == "At Risk"
    ).sum()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Students",
        f"{total_students}"
    )

    col2.metric(
        "Average Student Success Score",
        f"{average_success:.2f}/100"
    )

    col3.metric(
        "Average Placement Readiness",
        f"{average_placement:.2f}/100"
    )

    col4, col5 = st.columns(2)

    col4.metric(
        "Students Needing Academic Review",
        f"{academic_risk_count}"
    )

    col5.metric(
        "Students Needing Placement Review",
        f"{placement_risk_count}"
    )


st.divider()


# =========================================
# 8. SCORE DISTRIBUTIONS
# =========================================

st.header("Student Performance Analysis")

if not filtered.empty:

    chart1, chart2 = st.columns(2)

    with chart1:

        fig_success = px.histogram(
            filtered,
            x="student_success_score",
            nbins=15,
            title="Student Success Score Distribution",
            labels={
                "student_success_score":
                "Student Success Score"
            }
        )

        st.plotly_chart(
            fig_success,
            use_container_width=True
        )

    with chart2:

        fig_placement = px.histogram(
            filtered,
            x="placement_readiness_score",
            nbins=15,
            title="Placement Readiness Distribution",
            labels={
                "placement_readiness_score":
                "Placement Readiness Score"
            }
        )

        st.plotly_chart(
            fig_placement,
            use_container_width=True
        )


# =========================================
# 9. STUDENT SEGMENTATION
# =========================================

st.divider()

st.header("Student Segmentation")

if not filtered.empty:

    segment_counts = (
        filtered["student_segment"]
        .value_counts()
        .rename_axis("Student Segment")
        .reset_index(name="Student Count")
    )

    fig_segments = px.bar(
        segment_counts,
        x="Student Segment",
        y="Student Count",
        title="Students by Segment",
        labels={
            "Student Segment": "Student Segment",
            "Student Count": "Number of Students"
        }
    )

    st.plotly_chart(
        fig_segments,
        use_container_width=True
    )

    st.dataframe(
        segment_counts,
        use_container_width=True,
        hide_index=True
    )


# =========================================
# 10. RISK ANALYSIS
# =========================================

st.divider()

st.header("Risk Analysis")

if not filtered.empty:

    risk_col1, risk_col2 = st.columns(2)

    with risk_col1:

        academic_counts = (
            filtered["academic_risk"]
            .value_counts()
            .rename_axis("Academic Risk Status")
            .reset_index(name="Students")
        )

        fig_academic_risk = px.pie(
            academic_counts,
            names="Academic Risk Status",
            values="Students",
            title="Academic Risk Distribution"
        )

        st.plotly_chart(
            fig_academic_risk,
            use_container_width=True
        )

    with risk_col2:

        placement_counts = (
            filtered["placement_risk"]
            .value_counts()
            .rename_axis("Placement Risk Status")
            .reset_index(name="Students")
        )

        fig_placement_risk = px.pie(
            placement_counts,
            names="Placement Risk Status",
            values="Students",
            title="Placement Risk Distribution"
        )

        st.plotly_chart(
            fig_placement_risk,
            use_container_width=True
        )


# =========================================
# 11. STUDENT EXPLORER
# =========================================

st.divider()

st.header("Student Explorer")

if not filtered.empty:

    student_ids = sorted(
        filtered["student_id"].astype(str).tolist()
    )

    selected_student_id = st.selectbox(
        "Select a student",
        options=student_ids
    )

    student = filtered[
        filtered["student_id"].astype(str)
        == selected_student_id
    ].iloc[0]

    st.subheader(
        f"Student ID: {selected_student_id}"
    )

    detail1, detail2, detail3 = st.columns(3)

    detail1.metric(
        "CGPA",
        f"{student['cgpa']:.2f}/10"
    )

    detail2.metric(
        "Attendance",
        f"{student['attendance_percentage']:.1f}%"
    )

    detail3.metric(
        "Backlogs",
        f"{int(student['backlogs'])}"
    )

    detail4, detail5 = st.columns(2)

    detail4.metric(
        "Student Success Score",
        f"{student['student_success_score']:.2f}/100"
    )

    detail5.metric(
        "Placement Readiness Score",
        f"{student['placement_readiness_score']:.2f}/100"
    )

    st.write(
        "**Department:**",
        student["department"]
    )

    st.write(
        "**Academic Year:**",
        student["academic_year"]
    )

    st.write(
        "**Student Segment:**",
        student["student_segment"]
    )
    st.subheader("Why Does This Student Have This Success Score?")

    score_contributions = pd.DataFrame({
        "Indicator": [
            "CGPA",
            "Attendance",
            "Internal Marks",
            "LMS Activity",
            "Engagement",
            "Skills",
            "Student Satisfaction"
        ],
        "Indicator Score": [
            student["cgpa_score"],
            student["attendance_score"],
            student["internal_score"],
            student["lms_score"],
            student["engagement_score"],
            student["skills_score"],
            student["feedback_score"]
        ],
        "Weight (%)": [
            25, 20, 15, 10, 10, 15, 5
        ]
    })

    score_contributions["Contribution to Success Score"] = (
        score_contributions["Indicator Score"]
        * score_contributions["Weight (%)"] / 100
    )

    score_contributions["Indicator Score"] = (
        score_contributions["Indicator Score"].round(2)
    )

    score_contributions["Contribution to Success Score"] = (
        score_contributions["Contribution to Success Score"].round(2)
    )

    st.write(
        "Each indicator is converted to a score out of 100. "
        "Its contribution is calculated using the assigned weight."
    )

    st.dataframe(
        score_contributions,
        use_container_width=True,
        hide_index=True
    )

    fig_contributions = px.bar(
        score_contributions,
        x="Indicator",
        y="Contribution to Success Score",
        title="Contribution of Each Indicator",
        labels={
            "Indicator": "Success Indicator",
            "Contribution to Success Score": "Weighted Contribution"
        }
    )

    st.plotly_chart(
        fig_contributions,
        use_container_width=True
    )

    st.metric(
        "Calculated Student Success Score",
        f"{score_contributions['Contribution to Success Score'].sum():.2f}/100"
    )
    st.subheader("Why Does This Student Have This Placement Readiness Score?")

    placement_contributions = pd.DataFrame({
        "Indicator": [
            "Aptitude",
            "Coding",
            "Mock Interview",
            "Technical Skills",
            "Communication Skills",
            "CGPA"
        ],
        "Indicator Score": [
            student["aptitude_score"],
            student["coding_score"],
            student["mock_interview_score"],
            student["technical_skills"],
            student["communication_skills"],
            student["cgpa_score"]
        ],
        "Weight (%)": [
            25, 25, 20, 15, 10, 5
        ]
    })

    placement_contributions["Weighted Contribution"] = (
        placement_contributions["Indicator Score"]
        * placement_contributions["Weight (%)"] / 100
    )

    placement_contributions["Indicator Score"] = (
        placement_contributions["Indicator Score"].round(2)
    )

    placement_contributions["Weighted Contribution"] = (
        placement_contributions["Weighted Contribution"].round(2)
    )

    st.write(
        "Each placement indicator contributes to the final "
        "Placement Readiness Score according to its assigned weight."
    )

    st.dataframe(
        placement_contributions,
        use_container_width=True,
        hide_index=True
    )

    fig_placement_contributions = px.bar(
        placement_contributions,
        x="Indicator",
        y="Weighted Contribution",
        title="Contribution of Each Placement Indicator",
        labels={
            "Indicator": "Placement Indicator",
            "Weighted Contribution": "Weighted Contribution"
        }
    )

    st.plotly_chart(
        fig_placement_contributions,
        use_container_width=True
    )

    st.metric(
        "Calculated Placement Readiness Score",
        f"{placement_contributions['Weighted Contribution'].sum():.2f}/100"
    )
    st.subheader("Explainable Risk Flags")

    st.write(
        "**Academic Risk:**",
        student["academic_risk"]
    )

    st.write(
        "**Academic Risk Reasons:**",
        student["academic_risk_reasons"]
    )

    st.write(
        "**Placement Risk:**",
        student["placement_risk"]
    )

    st.write(
        "**Placement Risk Reasons:**",
        student["placement_risk_reasons"]
    )

    st.subheader("Recommended Intervention")

    st.info(
        student["recommended_intervention"]
    )


# =========================================
# 12. STUDENT TABLE
# =========================================

st.divider()

st.header("Student Records")

if not filtered.empty:

    display_columns = [
        "student_id",
        "department",
        "academic_year",
        "cgpa",
        "attendance_percentage",
        "backlogs",
        "student_success_score",
        "placement_readiness_score",
        "academic_risk",
        "placement_risk",
        "student_segment"
    ]

    st.dataframe(
        filtered[display_columns].sort_values(
            by="student_success_score"
        ),
        use_container_width=True,
        hide_index=True
    )

    csv_data = filtered.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download Filtered Student Data",
        data=csv_data,
        file_name="campusiq_student_data.csv",
        mime="text/csv"
    )


# =========================================
# 13. FOOTER
# =========================================

st.divider()

st.caption(
    "CampusIQ Hackathon Prototype | "
    "Synthetic demonstration data | "
    "Risk flags support human review and are not definitive predictions."
)