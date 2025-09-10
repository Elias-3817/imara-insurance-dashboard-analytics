# 🚀 Automated BI & Monitoring System for Insurance Analytics  

## Imara Insurance Analytics – Case Study

This project simulates an end-to-end analytics system for a fictional insurance company called Imara. The aim is to demonstrate how data pipelines, machine learning, and interactive dashboards can power real-time decision-making in insurance operations.

By generating realistic synthetic data, storing it in a structured PostgreSQL database, and layering on Power BI dashboards, Python ETL, and automated anomaly alerts, the system replicates both the challenges and solutions that insurers face daily. The outcome is a production-style analytics and monitoring ecosystem that executives could use to gain instant clarity on revenue, risk, and performance while cutting reporting time from days to minutes.


```mermaid
  flowchart LR
  direction LR

  %% Data generation (files)
  SDG[/Synthetic Data Generator\n(python, Faker/ipynb)/] --> CSV[/Raw CSVs & Exported Files/]

  %% ETL & cleaning
  CSV --> ETL[/"Python ETL & Cleaning\n(scripts: new_entry, generator)"/]
  ETL --> SQL[SQL_Scripts\n(table_entries, data_checks, data_cleaning.sql)]

  %% Database (cylinder)
  SQL --> DB[(PostgreSQL Database)]

  %% Downstream: dashboards + ML + monitoring
  DB -->|Scheduled refresh| PBIX[Power BI Dashboards\n(.pbix / Live connection)]
  DB --> ML[ML Sales Forecasting\n(Prophet / sklearn)]
  ML -->|Predictions written back| DB

  %% Monitoring & alerts
  DB --> MON[Monitoring & Alerting\n(python monitoring_alert_system.py)]
  MON --> AI((AI Summary\n(OpenAI)) )
  AI --> EMAIL[Email Alerts to Executives / Stakeholders]
  MON --> EMAIL

  %% Automation scheduler
  SCHED[(Automated Run Scripts / Scheduler\n(batch / cron / Windows Task Scheduler)] --> SDG
  SCHED --> MON
  SCHED --> ML

  %% Visuals / artifacts
  PBIX --> SNAP[Snapshots / Guide Pages / Screenshots]
  SNAP --> README[README / Documentation]

  %% Optional: manual / ad-hoc exploration
  Analyst[(Analysts / BI Users)] --> PBIX
  Analyst --> README
  ```

---

## 📂 Repository Structure

```plaintext
📂 imara-insurance-dashboard-analytics/
├── Dashboard/                # Power BI dashboards (.pbix files, visuals)
├── Data/                     # Synthetic & processed datasets
├── Documentation/            # Project documentation (markdown guides)
│   ├── 01_Synthetic_Data_Generator_Documentation.md
│   ├── 02_Database_design.md
│   ├── 02_SQL_Schema_Data_Cleaning.md
│   ├── 03_Dashboard_design.md
│   ├── 04_Monitor_&_Alert_System.md
│   ├── 05_Data_Dictionary.md
│
├── Scripts/                  # Automation & ETL scripts
│   ├── Python_Scripts/
│   │   ├── 01_Synthetic_data_generator.ipynb
│   │   ├── 02_New_entry_data_generator.py
│   │   ├── 03_monitoring_alert_system.py
│   │   ├── 04_ML_Sales_Prediction.ipynb
│   │
│   ├── SQL_Scripts/
│   │   ├── 01_Table_Entries.sql
│   │   ├── 02_Data_Checks.sql
│   │   ├── 03_Data_Cleaning.sql
│   │
│   └── Automated_run_script.bat
│
├── Snapshots/                # Dashboard screenshots & demo images
│   ├── Executive-insights.png
│   ├── Agent_Analysis.png
│   ├── Policy_Analysis.png
│   ├── Relationships_and_schema.png
│   └── Guide_&_Insights.png
│
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```



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

**Executive Summary**
![Dashboard Overview](Snapshots/Executive-insights.png) 

**Agent performance**
![Agent Performance Breakdown](Snapshots/Agent_Analysis.png)

**Help and guide page**
![Dashboard help and guide page](Snapshots/Guide_&_Insights.png)

**Automated Email Alert example**
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

