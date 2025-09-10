CREATE TABLE clients (
 ClientID INTEGER PRIMARY KEY,
 Name VARCHAR(100),
 DOB DATE,
 Age INTEGER,
 Gender VARCHAR(10),
 Location VARCHAR(25),
 JoinDate DATE,
 Tier VARCHAR(20),
 LifeTimeValue DECIMAL(12,2),
 RiskProfile VARCHAR(20)
);

CREATE TABLE agents (
AgentId INTEGER PRIMARY KEY,
Name VARCHAR (50),
HireDate DATE,
Region VARCHAR (20),
PerformanceTier VARCHAR(20)
);

CREATE TABLE claims (
ClaimId INTEGER PRIMARY KEY,
PolicyID INTEGER,
ClaimDate DATE,
ClaimAmount DECIMAL(13,2),
ClaimStatus VARCHAR (20),
FraudFlag INTEGER,
ClaimType VARCHAR(20)
);

CREATE TABLE policies(
PolicyID INTEGER PRIMARY KEY,
ClientID INTEGER,
AgentID INTEGER,
PolicyType VARCHAR (20),
StartDate DATE,
EndDate DATE,
PremiumAmount Decimal(13,2),
Status VARCHAR(20),
Channel VARCHAR (20),
PaymentStatus VARCHAR(15),
RiskScore Decimal(10,3),
OriginalPolicyId Decimal(10,1),
RenewalNumber INTEGER,
BusinessType VARCHAR(20),
TransactionType VARCHAR(20),
CoverageType VARCHAR(20),
VehicleAge DECIMAL(3,2),
UsageType VARCHAR (16)
);

CREATE TABLE agent_performance (
    AgentID INTEGER PRIMARY KEY,
    Name VARCHAR(50),
    Region VARCHAR(20),
    PerformanceTier VARCHAR(20),
    TotalPolicies INTEGER,
    TotalPremium DECIMAL(12,2),
    TotalCommission DECIMAL(12,2),
    AvgPremium DECIMAL(10,2),
    CommissionRatio DECIMAL(5,3),
    NewBusiness INTEGER,
    Renewals INTEGER,
    RetentionRate DECIMAL(8,6),
    TPO_Sales INTEGER,
    Comprehensive_Sales INTEGER
);

CREATE TABLE monthly_metrics (
    Month DATE,
    PolicyType VARCHAR(20),
    PoliciesSold INTEGER,
    PremiumRevenue DECIMAL(12,2),
    NewBusiness INTEGER,
    Renewals INTEGER,
    TPO_Count INTEGER,
    Comprehensive_Count INTEGER,
    ClaimsCount INTEGER,
    ClaimsAmount DECIMAL(12,2),
    AvgRiskScore DECIMAL(5,3),
    PRIMARY KEY (Month, PolicyType)
);

CREATE TABLE sales (
    SaleID INTEGER PRIMARY KEY,
    PolicyID INTEGER,
    AgentID INTEGER,
    CommissionAmount DECIMAL(12,2),
    SaleDate DATE,
    CommissionPaidFlag INTEGER,
    PolicyType VARCHAR(20),
    TransactionType VARCHAR(20),
    BusinessType VARCHAR(20),
    PaymentDate DATE,
    DaysToPay DECIMAL(5,1),
    DaysOutstanding INTEGER
);
