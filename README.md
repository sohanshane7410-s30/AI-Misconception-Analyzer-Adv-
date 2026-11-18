# 🧠 AI Misconception Analyzer

**A Student Learning Intelligence Platform**

[🌐 Live Demo](https://9tkknuuu5g9btt26iy76bh.streamlit.app/)

## Overview

AI Misconception Analyzer is an educational analytics application designed to help investigate student errors, identify potential misconceptions, analyze student reasoning, and recommend targeted learning interventions.

It combines Python-based analysis, interactive Streamlit dashboards, and Supabase cloud storage.

## Key Features

- **Misconception Detection:** Analyzes student answers and identifies potential misconceptions.
- **Diagnostic Question Generation:** Generates follow-up questions to investigate student understanding.
- **Student Reasoning Analysis:** Examines students' explanations and provides feedback.
- **Learning Analytics Dashboard:** Tracks assessment totals, accuracy, and misconception frequency.
- **Student Performance Tracking:** Compares assessment outcomes across students.
- **CSV Export:** Downloads assessment reports.
- **Cloud Database:** Stores student assessments and reasoning results using Supabase.
- **Persistent Storage:** Retrieves saved assessment records after application refreshes.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Streamlit | Interactive web application |
| Pandas | Data processing and analytics |
| Supabase | Cloud database |
| GitHub | Source code and version control |

## Application Workflow

1. Enter student assessment information.
2. Analyze the student's answer.
3. Identify a potential misconception.
4. Generate a diagnostic question.
5. Analyze the student's reasoning.
6. Recommend an intervention.
7. Save the assessment and reasoning to Supabase.
8. Explore learning analytics and download reports.

## Database

The application uses a Supabase PostgreSQL table named `student_assessments`.

It stores assessment information, misconception analysis, diagnostic questions, and reasoning results.

Database credentials are configured through Streamlit Secrets and are not stored in the repository.

## Local Setup

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
git clone https://github.com/sohanshane7410-s30/AI-Misconception-Analyzer-Adv-.git
cd AI-Misconception-Analyzer-Adv-
cd YOUR_PROJECT_FOLDER
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create `.streamlit/secrets.toml`:

```toml
SUPABASE_URL = "YOUR_SUPABASE_PROJECT_URL"
SUPABASE_KEY = "YOUR_SUPABASE_SECRET_KEY"
```

Run the application:

```bash
streamlit run app.py
```

**Security:** Never commit `secrets.toml` or expose your Supabase secret key.

## Project Purpose

This project demonstrates practical skills in:

- Educational data analysis
- Student misconception investigation
- Personalized intervention design
- Python application development
- Database integration
- Interactive dashboard development
- Cloud application deployment

## Live Application

[Launch AI Misconception Analyzer](https://9tkknuuu5g9btt26iy76bh.streamlit.app/)

---

**Project:** AI Misconception Analyzer  
**Deployment:** Streamlit Community Cloud  
**Database:** Supabase  
**Status:** Deployed

## Data Privacy and Responsible Use

- Use fictional student names and sample data when testing this application.
- Do not enter real student personal information or confidential academic records.
- Assessment records are stored in a Supabase database.
- This is a portfolio demonstration, not a production student-record management system.
- Access to the public demo may allow visitors to submit sample assessments.
