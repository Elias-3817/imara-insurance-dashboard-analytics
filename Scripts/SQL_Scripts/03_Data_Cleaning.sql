WITH dupes AS (
    SELECT clientid, startdate, enddate, premiumamount
    FROM policies
    GROUP BY clientid, startdate, enddate, premiumamount
    HAVING COUNT(*) > 1
)
SELECT p.*
FROM policies p
JOIN dupes d
ON p.clientid = d.clientid
AND p.startdate = d.startdate
AND p.enddate = d.enddate
AND p.premiumamount = d.premiumamount
ORDER BY p.clientid, p.startdate;


WITH dupes as (
	SELECT clientid,name,location,joindate
	FROM clients
	GROUP BY clientid,name,location,joindate 
	HAVING COUNT(*) > 1
)
SELECT c.* 
FROM clients c
JOIN dupes
ON c.clientid = dupes.clientid
AND c.name = dupes.name
AND c.location = dupes.location
AND c.joindate = dupes.joindate
ORDER BY c.clientid, c.joindate;

SELECT name,clientid
FROM clients
GROUP BY clientid,name 
HAVING COUNT(*) > 1;

-- 1. Remove duplicate clients (keep lowest row ID)
DELETE FROM clients 
WHERE ctid NOT IN(
	SELECT MIN(ctid)
	FROM clients
	GROUP BY clientid
);

--2. Remove duplicate policies
DELETE FROM policies
WHERE ctid NOT IN(
	SELECT MIN(ctid)
	FROM policies
	GROUP BY policYid
);

--3. Fix the typo issue in polices
UPDATE policies
SET Status = 'Active'
WHERE Status = 'Actiev';

--4. Fix the missing gender values
UPDATE clients
SET gender = 'Unknown'
WHERE gender IS null;

--5. Fix the missing values in channel
UPDATE policies
SET channel = 'Unknown'
WHERE channel IS NULL;



