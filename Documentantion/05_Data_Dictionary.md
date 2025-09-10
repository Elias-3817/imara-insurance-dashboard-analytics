📖 Data Dictionary

This document defines all key tables, columns, metrics, and DAX measures used in the project.
It ensures clarity for both technical stakeholders (developers, analysts) and business stakeholders (managers, executives).

1. Table & Column Dictionary
Table: customers
Column Name	Data Type	Description	Example
customer_id	Integer	Unique identifier for each customer	101
name	String	Full name of the customer	John Doe
signup_date	Date	Date the customer joined	2024-02-15
churn_flag	Boolean	1 if customer churned, 0 otherwise	0
Table: policies
Column Name	Data Type	Description	Example
policy_id	Integer	Unique identifier for each insurance policy	P-2031
customer_id	Integer	Links to customers.customer_id	101
premium_amount	Decimal	Monthly premium paid	5,000.00
start_date	Date	Policy start date	2024-01-01
end_date	Date	Policy end date (if churned/expired)	2025-01-01
2. Metric Dictionary (Business KPIs)
Metric	Formula / Definition	Business Meaning
Customer Lifetime Value (LTV)	Avg. Revenue per Customer × Avg. Lifespan	How much revenue one customer contributes over their entire relationship
Churn Rate	(# of churned customers ÷ total customers) × 100	Percentage of customers lost in a period
Premium Growth Rate	((Premium_today – Premium_last_period) ÷ Premium_last_period) × 100	Growth of insurance premiums collected over time
Active Policies	Count of policy_id where end_date ≥ today	Total number of policies currently active
3. DAX Measures (Power BI Layer)
Measure Name	DAX Formula	Explanation
Total Premiums	SUM(policies[premium_amount])	Total premiums collected
Active Customers	CALCULATE(DISTINCTCOUNT(customers[customer_id]), customers[churn_flag] = 0)	Unique customers who haven’t churned
Avg Premium per Customer	DIVIDE([Total Premiums], [Active Customers])	Average premium per active customer
Monthly Premium Growth	VAR CurrentMonth = [Total Premiums] VAR PrevMonth = CALCULATE([Total Premiums], DATEADD('Date'[Date], -1, MONTH)) RETURN DIVIDE(CurrentMonth - PrevMonth, PrevMonth)	Growth rate of premiums compared to previous month