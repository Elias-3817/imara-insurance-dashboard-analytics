# 📄 Synthetic Data Generator Documentation

## Overview

This module creates synthetic insurance data to simulate real-world operations in a SACCO/insurance context.
The dataset includes agents,agents performance, premiums, claims, and commission records across multiple customers and policies.
The goal is to provide a realistic but privacy-safe dataset for testing databases, dashboards, and automation pipelines.

### Why Synthetic Data?

- **Privacy**: No real customer data is exposed.
- **Flexibility**: Easy to scale up rows and adjust distributions.
- **Reproducibility**: Anyone running this project can generate consistent datasets.
- **Complexity**: Data mimics common insurance patterns (commission payments, claims delays, commission structures, claims trends).
 
## Data Model
The generator creates multiple related tables:

**Agents Table**
Fields: AgentID,Name,HireDate,Region,PerformanceTier

**Agent performance**
Fields: AgentID,Name,Region,PerformanceTier,TotalPolicies,TotalPremium,TotalCommission,AvgPremium,CommissionRatio,NewBusiness,Renewals,RetentionRate,TPO_Sales,Comprehensive_Sales

**Customers Table**
Fields: ClientID,Name,DOB,Age,Gender,Location,JoinDate,Tier,LifetimeValue,RiskProfile

**Policies Table**
Fields: PolicyID,ClientID,AgentID,PolicyType,StartDate,EndDate,PremiumAmount,Status,Channel,PaymentStatus,RiskScore,OriginalPolicyID,RenewalNumber,BusinessType,TransactionType,CoverageType,VehicleAge,UsageType

**Claims Table**
Fields: ClaimID,PolicyID,ClaimDate,ClaimAmount,ClaimStatus,FraudFlag,ClaimType

**Monthly Metrics Table**
Fields: Month,PolicyType,PoliciesSold,PremiumRevenue,NewBusiness,Renewals,TPO_Count,Comprehensive_Count,ClaimsCount,ClaimsAmount,AvgRiskScore
Features of the Generator

**Sales Table**
Fields: SaleID,PolicyID,AgentID,CommissionAmount,SaleDate,CommissionPaidFlag,PolicyType,TransactionType,BusinessType,CommissionRate,PaymentDate,DaysToPay,DaysOutstanding

## Features of the generator

1.Random but controlled distributions:
    - Age range 18–70 with realistic skew.
    - Region assignment with weighted probabilities.
    - Policy types distributed across Life, Motor, Health, etc.


2.Date realism:
    - Payments and claims spread over months/years.
    - Join dates backdated realistically.

3.Business logic:
    - Premiums linked to policies.
    - Claims linked to active policies.
    - Commissions tied to premium collections.

4. Simulated Noise/errors:
    - Duplicated entries
    - Missing values
    - Categorical typos/unknowns
    - Outliers/entry errors
### Tech Stack:
Python (pandas, numpy, faker, random, datetime, dateutil).

How to Run

Clone the repo and install dependencies:
```bash
pip install -r requirements.txt
```

Run the generator file:
```bash
python 01_Synthetic_data_generator.py
```


Output:

CSV files saved in /data

Example:
../data/clients.csv
../data/agents.csv
../data/policies.csv
../data/sales.csv
../data/claims.csv
../data/monthly_metrics.csv
../data/agent_performance.csv

ClientID, Name, DOB, Age, Gender, Location, JoinDate, Tier ,LifetimeValue, RiskProfile

230, Phillip Wanjiku, 1974-05-02,51, Male,Nakuru CBD, 2024-10-01, Bronze, 95931.97, Medium
1142, Michael Korir, 1972-03-17,53, Female,Naivasha, 2022-10-16, Silver, 294805.35, Medium
814, Faith Kosgey, 2001-01-07,24,Male ,Nakuru CBD, 2023-05-26, Platinum, 1000951.98, Low
1985, Joyce Muchiri, 2000-12-30,24,Female, Nakuru CBD, 2022-12-19, Gold, 331669.1, Low

Next Steps
Scale data volume (e.g., 10k+ rows).



