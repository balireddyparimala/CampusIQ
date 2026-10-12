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

    # Load academic risk severity from risk analysis results
    risk_file = PROJECT_DIR / "processed" / "student_risk_analysis.csv"
    if risk_file.exists():
        risk_data = pd.read_csv(risk_file)

        if "academic_risk_severity" in risk_data.columns:
            df = df.merge(
                risk_data[["student_id", "academic_risk_severity"]],
                on="student_id",
                how="left"
            )

        if "academic_risk_severity" not in df.columns:
            if "academic_risk" in df.columns:
                df["academic_risk_severity"] = df["academic_risk"].map(
                    {
                        "At Risk": "Moderate Risk",
                        "Low Risk": "Low Risk",
                    }
                ).fillna("Not Available")
            else:
                df["academic_risk_severity"] = "Not Available"

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
    "Understand Risk, Support Students & Improve Readiness"
)

st.caption(
    "A data-driven prototype for student support, "
    "academic monitoring, and placement preparation."
)

st.markdown(
    """
    <style>
    div[data-testid="stMetric"] {
        background: rgba(128, 128, 128, 0.08);
        border: 1px solid rgba(128, 128, 128, 0.22);
        padding: 12px 14px;
        border-radius: 10px;
    }
    .risk-high { color: #d62728; font-weight: 700; }
    .risk-medium { color: #d98200; font-weight: 700; }
    .risk-low { color: #218739; font-weight: 700; }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.expander("How CampusIQ works"):
    st.markdown(
        """
        1. **Integrate:** combine academic, attendance, LMS, engagement,
           skills, placement, and feedback data using student IDs.
        2. **Calculate:** compute the weighted Student Success Score (SSS)
           and Placement Readiness Score (PRS).
        3. **Identify indicators:** apply transparent prototype thresholds
           to flag students who may need academic or placement support.
        4. **Explain:** show the contribution of each score component and
           the reasons behind risk flags.
        5. **Support action:** use the results to guide faculty review,
           mentoring, and student-specific improvement plans.

        **Important:** this prototype uses synthetic data. Scores and risk
        flags support human review; they are not validated predictions.
        """
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
    academic_risk_percentage = (
        academic_risk_count / total_students * 100
        if total_students > 0 else 0
    )

    st.metric(
        "Students at Academic Risk",
        int(academic_risk_count),
        f"{academic_risk_percentage:.1f}% of students"
    )

with col3:
    placement_risk_percentage = (
        placement_risk_count / total_students * 100
        if total_students > 0 else 0
    )

    st.metric(
        "Students at Placement Risk",
        int(placement_risk_count),
        f"{placement_risk_percentage:.1f}% of students"
    )

st.info(
    "Use the filters and Student Explorer below to investigate "
    "individual students and identify suitable interventions."
)
# Academic Risk Severity Summary
st.subheader("Academic Risk Severity Summary")

if "academic_risk_severity" in students.columns:
    high_risk_count = (
        students["academic_risk_severity"] == "High Risk"
    ).sum()

    moderate_risk_count = (
        students["academic_risk_severity"] == "Moderate Risk"
    ).sum()

    low_risk_count = (
        students["academic_risk_severity"] == "Low Risk"
    ).sum()

    risk_col1, risk_col2, risk_col3 = st.columns(3)

    with risk_col1:
        st.metric("High Academic Risk", int(high_risk_count))

    with risk_col2:
        st.metric("Moderate Academic Risk", int(moderate_risk_count))

    with risk_col3:
        st.metric("Low Academic Risk", int(low_risk_count))
else:
    st.warning(
        "Academic risk severity is unavailable. "
        "Please regenerate the student risk analysis data."
    )
# Academic Risk Distribution Chart
st.subheader("Academic Risk Distribution")

risk_chart_data = pd.DataFrame({
    "Risk Severity": pd.Categorical(
        ["High Risk", "Moderate Risk", "Low Risk"],
        categories=["High Risk", "Moderate Risk", "Low Risk"],
        ordered=True
    ),
    "Number of Students": [
        int(high_risk_count),
        int(moderate_risk_count),
        int(low_risk_count)
    ]
})
st.bar_chart(
    risk_chart_data,
    x="Risk Severity",
    y="Number of Students"
)    
st.divider()


# =========================================
# 5. SIDEBAR FILTERS
# =========================================

st.sidebar.header("Dashboard Filters")

with st.sidebar.expander("Use a prepared CSV dataset"):
    uploaded_file = st.file_uploader(
        "Upload a CampusIQ-format student CSV",
        type=["csv"],
        help=(
            "Upload a processed student dataset containing the same columns "
            "as the current CampusIQ student table. Raw source files need "
            "integration and scoring before they can be used here."
        ),
        key="campusiq_csv_upload",
    )
    if uploaded_file is not None:
        try:
            uploaded_students = pd.read_csv(uploaded_file)
            required_upload_columns = {
                "student_id", "department", "academic_year", "cgpa",
                "attendance_percentage", "backlogs",
                "student_success_score", "placement_readiness_score",
                "academic_risk", "placement_risk", "student_segment",
                "cgpa_score", "attendance_score", "internal_score",
                "lms_score", "engagement_score", "skills_score",
                "feedback_score", "aptitude_score", "coding_score",
                "mock_interview_score", "technical_skills",
                "communication_skills", "academic_risk_reasons",
                "placement_risk_reasons", "recommended_intervention",
            }
            missing_upload_columns = sorted(
                required_upload_columns - set(uploaded_students.columns)
            )
            if missing_upload_columns:
                st.sidebar.error(
                    "This CSV is missing required CampusIQ columns: "
                    + ", ".join(missing_upload_columns)
                )
            else:
                if "academic_risk_severity" not in uploaded_students.columns:
                    uploaded_students["academic_risk_severity"] = "Not Available"
                students = uploaded_students.copy()
                st.sidebar.success(
                    f"Loaded {len(students)} students from the uploaded CSV."
                )
        except Exception as exc:
            st.sidebar.error(f"Could not read the CSV: {exc}")

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
# SUPPORT PRIORITY AND RISK VISUAL GUIDE
# =========================================

st.header("Student Support Priority List")
st.caption(
    "Priority is based on the prototype's existing risk flags and scores. "
    "Faculty should review the underlying circumstances before taking action."
)

priority = filtered.copy()
if not priority.empty:
    priority["academic_risk_severity"] = (
        priority["academic_risk_severity"]
        .fillna("Not Available")
        .astype(str)
    )
    severity_order = {
        "High Risk": 0,
        "Moderate Risk": 1,
        "Low Risk": 2,
        "Not Available": 3,
    }
    priority["_severity_order"] = (
        priority["academic_risk_severity"].map(severity_order).fillna(4)
    )
    priority["_academic_flag"] = (
        priority["academic_risk"].eq("At Risk").astype(int)
    )
    priority["_placement_flag"] = (
        priority["placement_risk"].eq("At Risk").astype(int)
    )
    priority["_risk_count"] = (
        priority["_academic_flag"] + priority["_placement_flag"]
    )
    priority = priority.sort_values(
        ["_severity_order", "_risk_count", "student_success_score",
         "placement_readiness_score"],
        ascending=[True, False, True, True],
    )
    priority_columns = [
        "student_id", "department", "academic_year",
        "student_success_score", "placement_readiness_score",
        "academic_risk_severity", "academic_risk", "placement_risk",
    ]
    priority_columns = [
        c for c in priority_columns if c in priority.columns
    ]
    st.dataframe(
        priority[priority_columns].head(10).round(2),
        use_container_width=True,
        hide_index=True,
    )
    st.caption(
        "This is a rule-based support queue, not a validated ranking of "
        "student outcomes."
    )
else:
    st.info("No students match the current filters.")

st.markdown(
    "**Risk guide:** 🔴 High Risk  ·  🟠 Moderate Risk  ·  🟢 Low Risk"
)

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
# DEPARTMENT AND YEAR RISK HEATMAP
# =========================================

st.divider()
st.header("Risk Concentration by Department and Year")

if not filtered.empty:
    heatmap_data = filtered.copy()
    heatmap_data["_academic_at_risk"] = (
        heatmap_data["academic_risk"].eq("At Risk").astype(int)
    )
    risk_pivot = heatmap_data.pivot_table(
        index="department",
        columns="academic_year",
        values="_academic_at_risk",
        aggfunc="mean",
        fill_value=0,
    ) * 100
    if not risk_pivot.empty:
        risk_pivot = risk_pivot.round(1)
        fig_heatmap = px.imshow(
            risk_pivot,
            text_auto=".1f",
            aspect="auto",
            color_continuous_scale=["#2ca25f", "#fee08b", "#d73027"],
            labels={
                "x": "Academic Year",
                "y": "Department",
                "color": "Academic risk (%)",
            },
            title="Percentage of Students Flagged for Academic Risk",
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)
        st.caption(
            "Each cell shows the percentage flagged by the current prototype "
            "rules within that department/year group. Small groups should be "
            "interpreted cautiously."
        )
else:
    st.info("Apply filters to view the risk heatmap.")

# =========================================
# 11. STUDENT EXPLORER
# =========================================

st.divider()

st.header("Student Explorer")

if not filtered.empty:

    student_ids = sorted(
        filtered["student_id"].astype(str).tolist()
    )

    search_student_id = st.text_input(
        "Search by Student ID",
        placeholder="Enter an ID, e.g. STU001",
        key="student_id_search",
    ).strip()

    matching_student_ids = [
        sid for sid in student_ids
        if search_student_id.lower() in sid.lower()
    ] if search_student_id else student_ids

    if not matching_student_ids:
        st.warning("No student ID matches your search and current filters.")
        st.stop()

    selected_student_id = st.selectbox(
        "Select a student",
        options=matching_student_ids
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
    "**Academic Risk Severity:**",
    student["academic_risk_severity"]
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

    st.subheader("What-if Simulator")
    st.caption(
        "Change selected indicators to see the mathematical effect on the "
        "weighted scores. These are simulations, not predictions of future outcomes."
    )

    sim_col1, sim_col2 = st.columns(2)
    with sim_col1:
        simulated_attendance = st.slider(
            "Simulated attendance (%)",
            min_value=0,
            max_value=100,
            value=int(round(float(student["attendance_percentage"]))),
            key=f"sim_attendance_{selected_student_id}",
        )
    with sim_col2:
        simulated_coding = st.slider(
            "Simulated coding score",
            min_value=0,
            max_value=100,
            value=int(round(float(student["coding_score"]))),
            key=f"sim_coding_{selected_student_id}",
        )

    current_sss = float(student["student_success_score"])
    current_prs = float(student["placement_readiness_score"])
    simulated_sss = (
        current_sss
        + (simulated_attendance - float(student["attendance_percentage"])) * 0.20
    )
    simulated_prs = (
        current_prs
        + (simulated_coding - float(student["coding_score"])) * 0.25
    )
    sim_metric1, sim_metric2 = st.columns(2)
    sim_metric1.metric(
        "Simulated Student Success Score",
        f"{simulated_sss:.2f}/100",
        delta=f"{simulated_sss - current_sss:+.2f}",
    )
    sim_metric2.metric(
        "Simulated Placement Readiness Score",
        f"{simulated_prs:.2f}/100",
        delta=f"{simulated_prs - current_prs:+.2f}",
    )
    st.caption(
        "Assumption: attendance and coding are directly scaled to 0–100 in "
        "the weighted formulas. Other components remain unchanged."
    )

    st.subheader("Suggested Four-Week Improvement Plan")
    coding_value = float(student["coding_score"])
    attendance_value = float(student["attendance_percentage"])
    plan_rows = []
    if coding_value < 50:
        plan_rows.extend([
            {"Week": "1", "Focus": "Programming fundamentals",
             "Suggested activity": "Practise variables, conditions, loops, and functions.",
             "Review measure": "Complete 10 beginner problems."},
            {"Week": "2", "Focus": "Core problem solving",
             "Suggested activity": "Practise arrays, strings, and basic algorithms.",
             "Review measure": "Complete 10 problems and review mistakes."},
            {"Week": "3", "Focus": "Timed coding practice",
             "Suggested activity": "Solve introductory problems under a time limit.",
             "Review measure": "Complete one timed practice set."},
            {"Week": "4", "Focus": "Progress review",
             "Suggested activity": "Attempt a short coding assessment with a mentor.",
             "Review measure": "Compare the new result with the starting score."},
        ])
    elif attendance_value < 75:
        plan_rows.extend([
            {"Week": "1", "Focus": "Understand attendance barriers",
             "Suggested activity": "Meet the student and faculty mentor to discuss missed classes.",
             "Review measure": "Agree on a realistic attendance plan."},
            {"Week": "2", "Focus": "Attendance routine",
             "Suggested activity": "Track class attendance and follow up on absences.",
             "Review measure": "Review attendance at the end of the week."},
            {"Week": "3", "Focus": "Catch up on learning",
             "Suggested activity": "Identify missed topics and arrange support where needed.",
             "Review measure": "Review completion of missed work."},
            {"Week": "4", "Focus": "Progress review",
             "Suggested activity": "Review attendance and barriers with the mentor.",
             "Review measure": "Compare attendance with the starting point."},
        ])
    else:
        plan_rows.extend([
            {"Week": "1", "Focus": "Set a student goal",
             "Suggested activity": "Review the student's lowest score component with a mentor.",
             "Review measure": "Agree on one measurable improvement goal."},
            {"Week": "2", "Focus": "Targeted practice",
             "Suggested activity": "Complete practice activities for the selected skill.",
             "Review measure": "Record practice completion and feedback."},
            {"Week": "3", "Focus": "Apply and review",
             "Suggested activity": "Attempt a short assignment or mock assessment.",
             "Review measure": "Identify remaining gaps."},
            {"Week": "4", "Focus": "Mentor review",
             "Suggested activity": "Review progress and agree on next steps.",
             "Review measure": "Compare initial and follow-up results."},
        ])
    st.dataframe(
        pd.DataFrame(plan_rows),
        use_container_width=True,
        hide_index=True,
    )
    st.caption(
        "This is a rule-based example plan. Faculty should personalize it "
        "after discussing the student's circumstances."
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

# ==========================================
# PERSONALIZED STUDENT ACTION PLAN
# ==========================================

st.header("Personalized Student Action Plan")

st.write(
    "CampusIQ recommends specific actions based on the selected student's "
    "academic performance and placement readiness."
)

# Identify students who need priority support
priority_students = filtered[
    (filtered["academic_risk"] == "At Risk")
    | (filtered["placement_risk"] == "At Risk")
].copy()
if not priority_students.empty:

    action_student_id = st.selectbox(
        "Select a student for a personalized action plan",
        options=priority_students["student_id"].astype(str).tolist(),
        key="action_plan_student"
    )

    action_student = priority_students[
        priority_students["student_id"].astype(str) == action_student_id
    ].iloc[0]

    st.subheader(f"Action Plan for {action_student_id}")

    # Academic improvement actions
    academic_actions = []

    if action_student["attendance_percentage"] < 75:
        academic_actions.append(
            "Attendance: Meet the student, identify the reasons for low "
            "attendance, and monitor attendance weekly."
        )

    if action_student["cgpa"] < 6:
        academic_actions.append(
            "Academic performance: Arrange remedial classes, faculty "
            "mentoring, and a weekly subject-wise progress review."
        )

    if action_student["backlogs"] >= 2:
        academic_actions.append(
            "Backlogs: Prepare a subject-wise backlog clearance plan "
            "with examination preparation milestones."
        )

    # Placement improvement actions
    placement_actions = []

    if action_student["coding_score"] < 50:
        placement_actions.append(
            "Coding: Practise basic programming for 30 minutes daily, "
            "complete at least three coding problems each week, and "
            "review mistakes with a mentor."
        )

    if action_student["mock_interview_score"] < 50:
        placement_actions.append(
            "Interview preparation: Attend one mock interview each week "
            "and improve answers based on faculty feedback."
        )

    if action_student["technical_skills"] < 50:
        placement_actions.append(
            "Technical skills: Complete one relevant technical assignment "
            "each week and demonstrate the work to a faculty mentor."
        )

    if action_student["communication_skills"] < 50:
        placement_actions.append(
            "Communication: Practise a two-minute self-introduction daily "
            "and participate in one group discussion each week."
        )

    if academic_actions:
        st.subheader("Academic Improvement")
        for action in academic_actions:
            st.write(f"- {action}")

    if placement_actions:
        st.subheader("Placement Preparation")
        for action in placement_actions:
            st.write(f"- {action}")


    if not academic_actions and not placement_actions:
        st.info(
            "No specific action was triggered by the current thresholds. "
            "A faculty member should review the student's individual needs."
        )

    st.info(
        "These recommendations are rule-based suggestions using the "
        "prototype's thresholds. Faculty should review them before "
        "deciding on interventions."
    )

else:
    st.success("No students currently match the action-plan priority criteria.")

# =========================================
# 13. FOOTER
# =========================================

st.divider()

st.caption(
    "CampusIQ Hackathon Prototype | "
    "Synthetic demonstration data | "
    "Risk flags support human review and are not definitive predictions."
)
