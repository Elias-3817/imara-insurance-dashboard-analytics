# 🚀 Automated BI & Monitoring System for Insurance Analytics  

Insurance & SACCOs are drowning in spreadsheets. Reports take days, are prone to errors, and rarely give leaders the real-time visibility they need. This project proves how any mid-sized financial institution can move from manual reporting chaos → automated, insight-driven decision making. By combining PostgreSQL, Python ETL, Power BI dashboards, and automated anomaly alerts, it replicates exactly what a real insurance broker or SACCO would deploy — giving executives instant clarity on revenue, risk, and performance while cutting reporting time from days to minutes.

## 📌 Project Overview  
This project demonstrates how to build a **complete end-to-end BI solution** — starting from **synthetic data generation**, storing and cleaning it in a **PostgreSQL database**, building **interactive dashboards in Power BI**, and automating a **monitoring + email alerting system**.  

The goal: replicate what a **SACCO, bank, or insurance broker companies** would need in real life — moving from messy manual spreadsheets to a **centralized, automated, and insight-driven system.**  

---

## 📂 Repository Structure

imara-insurance-dashboard-analytics/
│── Dashboard/ # Power BI dashboards (.pbix files, visuals)
│
│── Data/ # Synthetic & processed datasets
│
│── Documentation/ # Project documentation (markdown guides)
│ ├── synthetic_data_generator.md
│ ├── database_design.md
│ ├── sql_schema_data_cleaning.md
│ ├── dashboard_design.md
│ ├── monitor_&_alert_system.md
│ ├── data_dictionary.md
│
│── Scripts/ # Automation & ETL scripts
│ ├── Python_Scripts/
│ │ ├── synthetic_data_generator.py
│ │ ├── new_entry_data_generator.py
│ │ ├── monitoring_alert_system.py
│ │ ├── ml_sales_prediction.py
│ │
│ ├── SQL_Scripts/
│ │ ├── table_entries.sql
│ │ ├── data_checks.sql
│ │ ├── data_cleaning.sql
│ │
│ ├── Automated_Run_Scripts/ # Batch / cron / scheduled tasks
│
│── Snapshots/ # Dashboard screenshots, demo images
│
│── LICENSE # License file
│── README.md # Project overview & documentation
│── requirements.txt # Python dependencies


## 🏗️ System Architecture  
Synthetic Data → PostgreSQL Database → Python ETL Scripts → Power BI Dashboards → Monitoring & Email Alerts

## 🔑 Project Phases

### Synthetic Data Generation
- Created realistic datasets for customers, agents, policies, sales, claims, and commissions.
- Simulated daily transactions, renewals, and claims processing.
- Introduced variability & anomalies (e.g., missing data, duplicates, outliers) to mimic real-world noise.

[*Click here for a deep dive into synthetic data generation docs*](Documentantion/01_Synthetic_Data_Generator_Documentation.md)

### Database Setup (PostgreSQL)
- Designed a normalized schema for insurance operations.
- Enforced relationships (clients → policies → claims → sales).
- Loaded synthetic datasets into PostgreSQL using Python scripts.

### Data Cleaning & Processing (ETL)
- SQL scripts for cleaning and validation.
- Removed duplicates, fixed categorical typos, handled nulls.
- Stored curated data into reporting tables.

[*Click here for detailed documented explanations for the database set-up and data cleaning*](Documentantion/02_SQL_Schema_Data_Cleaning.md)

### Interactive Dashboards (Power BI)
- Connected Power BI to PostgreSQL.
- Built executive dashboards with key KPIs:
    - Premium collections
    - Claims analysis
    - Commission payouts
    - Renewal trends
- Added slicers and drill-downs for interactivity.
- Included a “How to Use” guide for non-technical users.

[*Click here for the dashboard design docs*](Documentantion/03_Dashboard_design.md)

### Monitoring & Alerting System
- Python monitoring script tracks:
- Sudden drops in premiums
- Abnormal spikes in commissions (will also track abnormal spikes in claims in the future.)
- Sends automated email alerts with AI-generated summaries.
- Scheduled via batch script for continuous monitoring.

[*click here for the monitoring & alert system docs*](Documentantion/04_Monitor_&_Alert_System.md)

### ⚙️ Tech Stack
- Python (pandas, psycopg2, smtplib, faker, numpy)
- PostgreSQL (relational database)
- Power BI (interactive dashboards & KPI monitoring)
- Batch scripting (task scheduling)
- OpenAI API (AI-generated anomaly summaries)

📊 Key Features
✅ End-to-end pipeline: from raw data → insights → action
✅ Automated cleaning, validation, and storage in PostgreSQL
✅ Executive dashboards with KPI tracking & drill-downs
✅ Real-time monitoring and email alerting
✅ Scalable to cloud deployment & ML forecasting

## 🚀 Getting Started

### 1. Clone the repository
```bash
Copy code
git clone https://github.com/Elias-3817/imara-insurance-dashboard-analytics
cd <C:User/imara-insurance-dashboard-analytics>
```

### 2. Create a virtual environment (recommended)
```bash
Copy code
python -m venv venv
# Activate the venv
# On Windows
venv\Scripts\activate
# On Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
Copy code
pip install -r requirements.txt
```

### 4. Run the project
Synthetic Data Generator (notebook):
Open [synthetic_data_generator.ipynb](Scripts/python_scripts/01_Synthetic_data_generator.ipynb) in Jupyter or VSCode.

Automated Data Entry
```bash
python New_entry_data_generator.py
```
Monitoring & Alerts
```bash
python monitoring_alert_system.py
```

ML Sales Forecasting (Prophet model)
```bash
python ML_sales_prediction.py
```

📌 Store your API keys and database credentials in a .env file:
```bash
OPENAI_API_KEY=your_api_key_here
DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/dbname
```

📷 Demo Screenshots

![Dashboard Overview](Snapshots/Executive-insights.png) 

![Agent Performance Breakdown](Snapshots/Agent_Analysis.png)

![Dashboard help and guide page](Snapshots/Guide_&_Insights.png)

![Automated Email Alert Example](Snapshots/E-mail_alerts.png)


## 📌 Next Steps
- Deploy and host Database, ETL + monitoring scripts to Azure/AWS/Heroku
- Move monitoring from batch to real-time API-based alerts
- Extend Power BI with predictive analytics (ML models)
- Add role-based dashboards for executives, agents, and risk managers

# 📍 **Problem → Solution → Impact**
## Problem
Small and medium-sized Insurance & SACCOs rely on manual Excel reports — error-prone, time-consuming, and not scalable.

## Solution
This repo demonstrates a fully automated BI system:
1. Synthetic data simulating insurance operations
2. PostgreSQL database for structured storage
3. Python ETL for cleaning, validation, and monitoring
4. Power BI dashboards for executives & managers
5. Automated alerts for anomalies

## **Impact**
⏱️ Reporting time reduced from days → minutes
❌ Eliminates manual errors
📈 Provides real-time beautiful dashboards and actionable insights for decision-makers

### ✍️ Author
Elias Gichuru
BI Developer | Data Analyst | Aspiring ML Engineer

📎 (Linkedin)[https://www.linkedin.com/in/elias-gichuru-56a2a3250] | ✉️ Email: Eliasinsights@proton.me

