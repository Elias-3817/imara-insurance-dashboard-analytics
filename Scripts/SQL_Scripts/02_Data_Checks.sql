-- confirm if data loaded in well
SELECT 'agent_performance' AS table_name, COUNT(*) AS rows FROM agent_performance
UNION ALL
SELECT 'agents', COUNT(*) FROM agents
UNION ALL
SELECT 'claims', COUNT(*) FROM claims
UNION ALL
SELECT 'clients', COUNT(*) FROM clients
UNION ALL
SELECT 'monthly_metrics', COUNT(*) FROM monthly_metrics
UNION ALL
SELECT 'policies', COUNT(*) FROM policies
UNION ALL
SELECT 'sales', COUNT(*) FROM sales;


-- Check if all policies have valid clients
SELECT COUNT(*) as policies_with_invalid_clients
FROM policies p
LEFT JOIN clients c ON p.ClientID = c.ClientID
WHERE c.ClientID IS NULL;

-- Check if all sales have valid policies
SELECT COUNT(*) as sales_with_invalid_policies  
FROM sales s
LEFT JOIN policies p ON s.PolicyID = p.PolicyID
WHERE p.PolicyID IS NULL;

--Check for any inconsistencies in categorical columns
SELECT DISTINCT PolicyType FROM policies;
SELECT DISTINCT Gender FROM clients;      --nulls
SELECT DISTINCT ClaimStatus FROM claims;
SELECT DISTINCT Status FROM policies;          --typo and duplicated categorical 
SELECT DISTINCT Channel FROM policies;          --nulls
SELECT DISTINCT PaymentStatus FROM policies; 
SELECT DISTINCT performancetier FROM agents;
SELECT DISTINCT ClaimType FROM claims;      

-- Calculate percentage of nulls in gender
SELECT Gender,COUNT(*) AS count,
ROUND(COUNT(*) * 100.0/ (SELECT COUNT(*) FROM clients), 2) as percentage
FROM clients
GROUP BY Gender
ORDER By count DESC; -- less than 1%

--Understand the spread of the nulls
SELECT 
    RiskProfile,
    Tier,
    COUNT(*) as null_gender_count
FROM clients 
WHERE Gender IS NULL
GROUP BY RiskProfile, Tier
ORDER BY null_gender_count DESC;  --They are scattered/random.

SELECT channel, COUNT(*) AS count,
ROUND(COUNT(*) *100.0/ (SELECT COUNT(*) FROM policies),2) AS percentage
FROM policies
GROUP BY channel
ORDER BY count; -- less than 1%

--Check for duplicates -------
SELECT 'clients' AS table_name, SUM(count_dupes) 
FROM (SELECT COUNT(*) - 1 AS count_dupes
		FROM clients
		GROUP BY clientid
		HAVING COUNT(*) > 1)    --10 duplicates
AS sub
UNION ALL 
SELECT 'policies', SUM(count_dupes)
FROM (SELECT COUNT(*) - 1 AS count_dupes
		FROM policies 
		GROUP BY policyid
		HAVING COUNT(*) > 1)   -- 50 duplicates
AS sub
UNION ALL
SELECT 'sales', SUM(count_dupe)
FROM ( SELECT COUNT(*) - 1 AS count_dupe
		FROM sales
		GROUP BY saleid
		HAVING COUNT(*) > 1)
AS sub;

--REFERENTIAL INTEGRITY (orphaned records)
SELECT 'claims_without_policies' as issue, COUNT(*)
FROM claims c LEFT JOIN policies p ON c.policyid = p.policyid 
WHERE p.policyid IS NULL;  -- 0

SELECT c.name,c.joindate,
--Issues we found
--1. Nulls in gender column in clients table
--2. Nulls in channel column in polcies table
--3. Typo and duplicated categorical type in status from policies table
--4. 10 duplicates in clients id
--5. 50 duplicates in policy id