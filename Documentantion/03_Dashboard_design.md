# 📊 Dashboard Design Documentation

## 1. Overview
The Power BI dashboard provides a multi-page reporting solution tailored for SACCO/insurance operations. It transforms transactional data (clients, agents, policies, sales, claims) into executive insights that drive decision-making.

The design follows three principles:
**1.Clarity** → Each page addresses a specific audience (executives, managers, agents).
**2.Actionability** → Metrics and visuals link directly to business decisions (renewals, claims management, agent performance).
**3.Scalability** → Built to refresh automatically from PostgreSQL and expand with new data sources.

## 2. Page Layouts
### 🏢 Executive Summary
- KPIs: Total Premiums, Total Claims, Active Policies, Retention Rate.
- Trend Line: Premium vs. Claims over time.
- Churn / Renewals Gauge: Highlights business health.
Purpose: One-page “CEO view” for quick decision-making.

### 📑 Policy Analysis
- Breakdown by Policy Type: Motor, Health, Life, etc.
- KPIs: Premium Revenue, Renewals, New Business split.
- Risk Analysis: Average risk score per policy type.
**Purpose**: Identify high-value vs. high-risk policy lines and claim trend analysis across diff months per year.

### 👥 Agent Overview & Performance
- Leaderboards: Top agents by Premium, Commission, Retention.
- KPIs: New Business vs Renewals, Commission Ratio.
- Regional Analysis: Performance split by region.
**Purpose**: Incentive planning, performance reviews, training needs.

### 🧑‍🤝‍🧑 Client Segmentation
- Demographics: Age, Gender, Location.
- Tiers: Bronze / Silver / Gold / Platinum.
- Lifetime Value Distribution: High-value clients vs. churn risk.
**Purpose**: Support targeted marketing, customer retention.

### 💡 Guide & Key Insights
- A how to use guide to help the user understand how to navigate across pages,filter through visuals.
- Final summary on key important insights.
- Client Segmentantion (page 4) insights.
**Purpose**: Comprehensive Guide/Bridge between analytics and action.

## 3. Design Principles
Color Coding:
- Green → Growth / Good performance.
- Red → Risks / Underperformance.
- Neutral palette for background to keep focus on visuals.
Consistency: KPIs displayed in same format.
Filters & Interactivity:
- Slicers for Date, Region, Policy Type.
Accessibility:
- Large KPI cards for executives.
- Tooltip explanations for complex visuals.

## 4. Data Flow
Source: PostgreSQL (synthetic dataset).
Transformation: SQL cleaning scripts ([**See sql_schema_data_cleaning.md*](02_SQL_Schema_Data_Cleaning.md))
Modeling: Power BI star schema (clients, agents, policies, sales, claims as fact tables; agent_performance, monthly_metrics as aggregates).
Visualization: Power BI multi-page dashboard.
Automation: Scheduled refresh + email alerts when thresholds are met. ([**See Monitor_&_Alert_System.md*](03_Dashboard_design,md))
