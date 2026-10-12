# CampusIQ — Student Success Analytics and Placement Readiness Dashboard

## 1. Project Overview

CampusIQ is a student analytics dashboard designed to help educational institutions identify students who may need academic support and students who require additional preparation for placements.

The system integrates academic performance, attendance, Learning Management System (LMS) activity, student engagement, technical skills, placement assessment results, and student feedback into a unified analytical platform.

CampusIQ calculates a Student Success Score (SSS) and a Placement Readiness Score (PRS), identifies potential risks, and provides insights to support data-driven academic and placement interventions.

## 2. Problem Statement

Educational institutions often maintain student information across multiple datasets and departments. This makes it difficult to identify struggling students early and coordinate suitable interventions.

CampusIQ addresses this problem by integrating student data, calculating interpretable scores, identifying risk indicators, and presenting the results through an interactive dashboard.

## 3. Key Features

- Integration of multiple student datasets.
- Student Success Score (SSS) calculation.
- Placement Readiness Score (PRS) calculation.
- Academic risk identification.
- Placement risk identification.
- Academic risk severity classification.
- Student segmentation and intervention recommendations.
- Interactive dashboard with charts and key performance indicators.
- Filters for department, academic year, and risk status.
- Individual Student Explorer.
- Score explainability to show how each component contributes to the final score.
- Downloadable student analysis data.

## 4. Student Success Score (SSS)

The Student Success Score summarizes selected indicators of academic progress and student engagement.

| Component | Weight |
|---|---:|
| CGPA | 25% |
| Attendance | 20% |
| Internal Marks | 15% |
| LMS Activity | 10% |
| Student Engagement | 10% |
| Skills | 15% |
| Student Feedback | 5% |
| **Total** | **100%** |

Each component is converted to a score on a 0–100 scale before applying its weight.

**Formula:**

SSS = (CGPA Score × 0.25) + (Attendance Score × 0.20) + (Internal Marks Score × 0.15) + (LMS Score × 0.10) + (Engagement Score × 0.10) + (Skills Score × 0.15) + (Feedback Score × 0.05)

## 5. Placement Readiness Score (PRS)

The Placement Readiness Score summarizes selected indicators of a student's preparation for recruitment.

| Component | Weight |
|---|---:|
| Aptitude | 25% |
| Coding | 25% |
| Mock Interview | 20% |
| Technical Skills | 15% |
| Communication | 10% |
| CGPA | 5% |
| **Total** | **100%** |

**Formula:**

PRS = (Aptitude Score × 0.25) + (Coding Score × 0.25) + (Mock Interview Score × 0.20) + (Technical Skills Score × 0.15) + (Communication Score × 0.10) + (CGPA Score × 0.05)

Both scores range from 0 to 100.

These weights and thresholds are prototype design assumptions. They should be validated against institutional requirements and real student outcomes before being used for high-stakes decisions.

## 6. Risk Analysis

### Academic Risk

The prototype identifies academic risk using indicators such as:

- Low Student Success Score.
- Attendance below 75%.
- CGPA below 6.
- Two or more backlogs.

Academic risk severity is also classified to help prioritize student support.

### Placement Risk

The prototype identifies placement risk using indicators such as:

- Low Placement Readiness Score.
- Low coding score.

The dashboard displays risk indicators and reasons to help faculty understand why a student has been flagged.

These indicators are intended to support faculty review, not to replace professional judgment.

## 7. Student Segmentation and Interventions

CampusIQ groups students into support-oriented segments and suggests possible interventions.

Examples include:

- Attendance monitoring and parent counselling.
- Remedial classes and academic mentoring.
- Individual academic improvement plans.
- Coding practice and technical workshops.
- Mock interviews and communication training.
- Faculty mentoring and progress reviews.

Interventions should be selected after reviewing each student's circumstances.

## 8. Dashboard Features

The interactive dashboard includes:

- Overall student statistics.
- Average Student Success Score.
- Average Placement Readiness Score.
- Academic and placement risk summaries.
- Academic risk severity distribution.
- Score distribution charts.
- Student segmentation visualizations.
- Department and academic-year filters.
- Individual student details and risk explanations.
- Downloadable analysis results.

## 9. Technology Stack

- Python
- Pandas
- NumPy
- Streamlit
- Plotly
- CSV-based datasets

## 10. Project Structure

```text
CampusIQ/
├── app.py
├── requirements.txt
├── .gitignore
├── data/
├── processed/
└── src/
    ├── generate_data.py
    ├── data_integration.py
    ├── scoring.py
    ├── risk_analysis.py
    └── segmentation.py
```

## 11. How to Run the Application

### Prerequisites

- Python 3.12 or a compatible Python version.
- Git, if cloning the repository.

### Step 1: Clone the repository

```bash
git clone https://github.com/balireddyparimala/CampusIQ.git
cd CampusIQ
```

### Step 2: Create a virtual environment

```bash
python -m venv .venv
```

### Step 3: Activate the virtual environment

On Windows:

```bash
.venv\Scripts\activate
```

### Step 4: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Run the dashboard

```bash
streamlit run app.py
```

The application will display a local URL in the terminal. Open that URL in your browser.

## 12. Live Demo

**Live Dashboard:** https://campusiq-balireddy.streamlit.app/

**Source Code:** https://github.com/balireddyparimala/CampusIQ

## 13. Data and Responsible Use

This prototype uses synthetic student data for demonstration and development.

The scores and risk indicators are intended to demonstrate an analytics workflow. They are not validated predictions of academic failure or placement success.

Before using the system with real student data, institutions should establish appropriate privacy safeguards, access controls, data-quality checks, and validation procedures.

Student records and risk classifications should be reviewed by authorized faculty. The dashboard should support student development rather than automatically determine academic progression, financial benefits, or placement eligibility.

## 14. Expected Impact

CampusIQ demonstrates how integrated student data and explainable analytics can help institutions:

- Identify students who may need support.
- Prioritize academic mentoring.
- Monitor placement preparation.
- Understand the factors contributing to student scores.
- Plan targeted interventions.
- Support evidence-informed educational decisions.

## 15. Future Enhancements

- Validate score weights using historical student outcomes.
- Add longitudinal student performance tracking.
- Improve intervention tracking and outcome measurement.
- Introduce role-based access controls.
- Add privacy-preserving integration with institutional systems.
- Evaluate predictive models only when suitable, representative, and ethically governed data is available.

---

**CampusIQ — Turning Student Data into Actionable Insights.**
