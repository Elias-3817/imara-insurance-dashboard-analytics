# data_generation.py
# Usage: python data_generation.py
# Optional env var: DAILY_NEW_CLIENTS (int)
#
# WARNING: This script will write data to your PostgreSQL database.
# DB defaults are set from what you provided. Change if needed.

import os
import random
from datetime import datetime
from dateutil.relativedelta import relativedelta

import pandas as pd
from faker import Faker
from sqlalchemy import create_engine, text

# ---------- CONFIG ----------
# You provided these credentials; change if you want to use env vars instead:
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DAILY_NEW_CLIENTS = int(os.getenv("DAILY_NEW_CLIENTS", "3"))
MAX_POLICIES_PER_CLIENT = int(os.getenv("MAX_POLICIES_PER_CLIENT", "2"))

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

fake = Faker()
Faker.seed(42)
random.seed(42)

engine = create_engine(DATABASE_URL, future=True)

# Lookup tables / lists
REGIONS = ['Nakuru CBD', 'Gilgil', 'Naivasha', 'Molo', 'Rongai']
POLICY_TYPES = ['Life', 'Health', 'Motor', 'Property']
CHANNELS = ['Branch', 'Phone', 'Agent Visit', 'Online', 'Referral']

# ---------- DB helpers ----------
def get_max_ids(conn):
    q = {
        'clients': "SELECT COALESCE(MAX(clientid), 0) AS m FROM clients",
        'policies': "SELECT COALESCE(MAX(policyid), 0) AS m FROM policies",
        'sales': "SELECT COALESCE(MAX(saleid), 0) AS m FROM sales",
        'claims': "SELECT COALESCE(MAX(claimid), 0) AS m FROM claims",
        'agents': "SELECT COALESCE(MAX(agentid), 0) AS m FROM agents",
    }
    out = {}
    for k, sql in q.items():
        r = conn.execute(text(sql)).fetchone()
        out[k] = int(r[0]) if r is not None else 0
    return out

def get_agent_ids(conn):
    r = conn.execute(text("SELECT agentid FROM agents")).all()
    if not r:
        return []
    return [row[0] for row in r]

def ensure_at_least_one_agent(conn):
    # If there are no agents, add a small fallback agent so we can assign policies
    agent_ids = get_agent_ids(conn)
    if len(agent_ids) == 0:
        print("[WARN] No agents found in DB. Creating a fallback agent (AgentID=1).")
        conn.execute(text(
            "INSERT INTO agents (agentid, name, hiredate, region, performancetier) VALUES (:id, :name, :hd, :reg, :tier)"
        ), [{"id": 1, "name": "Fallback Agent", "hd": datetime.now().date(), "reg": REGIONS[0], "tier": "Medium"}])
        conn.commit()
        return [1]
    return agent_ids

# ---------- Generators ----------
def generate_client(next_client_id):
    name = fake.first_name() + " " + fake.last_name()
    dob = fake.date_of_birth(minimum_age=20, maximum_age=75)
    age = (pd.Timestamp('today') - pd.to_datetime(dob)).days // 365
    gender = random.choice(['Male', 'Female'])
    location = random.choices(REGIONS, weights=[0.5,0.15,0.15,0.1,0.1])[0]
    join_date = datetime.now().date()
    tier = random.choices(['Bronze','Silver','Gold','Platinum'], weights=[0.4,0.35,0.2,0.05])[0]
    base_ltv = random.uniform(50000, 150000) * {'Bronze':1,'Silver':2,'Gold':4,'Platinum':8}[tier]
    if age >= 50:
        base_ltv *= 1.15
    if location == 'Nakuru CBD':
        base_ltv *= 1.2
    risk_profile = random.choices(['Low','Medium','High'], weights=[0.3,0.5,0.2])[0]

    return {
        'clientid': next_client_id,
        'Name': name,
        'DOB': dob,
        'Age': int(age),
        'Gender': gender,
        'Location': location,
        'JoinDate': join_date,
        'Tier': tier,
        'LifetimeValue': round(base_ltv, 2),
        'RiskProfile': risk_profile
    }

def generate_policy(next_policy_id, client_id, agent_id):
    policy_type = random.choice(POLICY_TYPES)
    start = datetime.now().date()
    end = start + relativedelta(years=1)
    base_premiums = {'Motor': 20000, 'Health': 35000, 'Life': 80000, 'Property': 200000}
    premium = base_premiums[policy_type] * random.uniform(0.8, 1.3)

    coverage_type = None
    vehicle_age = None
    usage_type = None
    if policy_type == 'Motor':
        coverage_type = 'TPO' if random.random() < 0.7 else 'Comprehensive'
        vehicle_age = random.randint(1, 12)
        usage_type = random.choices(['Private', 'Commercial'], weights=[0.7, 0.3])[0]
        if coverage_type == 'TPO':
            premium *= 0.35
        if usage_type == 'Commercial':
            premium *= 1.4
        if vehicle_age > 10:
            premium *= 0.8

    tier_mult = random.choices([0.8, 1.0, 1.3, 1.8], weights=[0.4, 0.35, 0.2, 0.05])[0]
    premium *= tier_mult

    return {
        'PolicyID': next_policy_id,
        'clientid': client_id,
        'AgentID': agent_id,
        'PolicyType': policy_type,
        'StartDate': start,
        'EndDate': end,
        'PremiumAmount': round(premium, 2),
        'Status': 'Active',
        'Channel': random.choice(CHANNELS),
        'PaymentStatus': random.choice(['On-time', 'Late']),
        'RiskScore': round(random.uniform(0.05, 0.4), 3),
        'OriginalPolicyID': None,
        'RenewalNumber': 0,
        'BusinessType': 'Individual',
        'TransactionType': 'Individual',
        'CoverageType': coverage_type,
        'VehicleAge': vehicle_age,
        'UsageType': usage_type
    }

def generate_sale(next_sale_id, policy):
    base_commission_rates = {'Motor': 0.15, 'Health': 0.12, 'Life': 0.20, 'Property': 0.10}
    commission_rate = base_commission_rates[policy['PolicyType']] * (0.7 if policy['TransactionType'] == 'Renewal' else 1.0)
    commission = round(policy['PremiumAmount'] * commission_rate, 2)
    return {
        'SaleID': next_sale_id,
        'PolicyID': policy['PolicyID'],
        'AgentID': policy['AgentID'],
        'CommissionAmount': commission,
        'SaleDate': policy['StartDate'],
        'CommissionPaidFlag': random.choices([1, 0], weights=[0.92, 0.08])[0],
        'PolicyType': policy['PolicyType'],
        'TransactionType': policy['TransactionType'],
        'BusinessType': policy['BusinessType'],
        'CommissionRate': round(commission_rate, 4)
    }

# ---------- Main run ----------
def run():
    print(f"[{datetime.now().isoformat()}] Starting data generation. DAILY_NEW_CLIENTS={DAILY_NEW_CLIENTS}")
    with engine.begin() as conn:
        max_ids = get_max_ids(conn)
        agent_ids = get_agent_ids(conn)
        if not agent_ids:
            agent_ids = ensure_at_least_one_agent(conn)

        next_client = max_ids['clients'] + 1
        next_policy = max_ids['policies'] + 1
        next_sale = max_ids['sales'] + 1

        clients = []
        policies = []
        sales = []

        for _ in range(DAILY_NEW_CLIENTS):
            c = generate_client(next_client)
            clients.append(c)

            num_pols = random.choices([1, 2], weights=[0.8, 0.2])[0]
            for _ in range(num_pols):
                a_id = random.choice(agent_ids)
                p = generate_policy(next_policy, next_client, a_id)
                policies.append(p)
                s = generate_sale(next_sale, p)
                sales.append(s)
                next_policy += 1
                next_sale += 1

            next_client += 1

        # Convert to dataframes

        df_clients = pd.DataFrame(clients)
        df_policies = pd.DataFrame(policies)
        df_sales = pd.DataFrame(sales)

        df_clients.columns = df_clients.columns.str.lower()
        df_policies.columns = df_policies.columns.str.lower()
        df_sales.columns = df_sales.columns.str.lower()
        
        # Write to DB (append)
        if not df_clients.empty:
            df_clients.to_sql('clients', conn.engine, if_exists='append', index=False, method='multi')
        if not df_policies.empty:
            df_policies.to_sql('policies', conn.engine, if_exists='append', index=False, method='multi')
        if not df_sales.empty:
            df_sales.to_sql('sales', conn.engine, if_exists='append', index=False, method='multi')

        print(f"Wrote {len(df_clients)} clients, {len(df_policies)} policies, {len(df_sales)} sales")

if __name__ == "__main__":
    run()
