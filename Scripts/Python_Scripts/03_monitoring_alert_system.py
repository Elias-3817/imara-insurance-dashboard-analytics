import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy import create_engine, text
import openai
from dotenv import load_dotenv
import sys
import pdb
import traceback

# CONFIG
# Load environment variables from repo root
dotenv_path = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
load_dotenv(dotenv_path=dotenv_path)

print("Loading .env from:", dotenv_path)
print("DB_USER:", os.getenv("DB_USER"))

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST") 
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

GMAIL_USER = os.getenv("SMTP_USER") 
GMAIL_PASSWORD = os.getenv("SMTP_PASS")
TO_EMAIL = os.getenv("CEO_EMAIL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

#Easy to debug if one profile failed to load
required_vars = [
    "DB_USER","DB_PASS","DB_HOST","DB_PORT","DB_NAME",
    "SMTP_USER","SMTP_PASS","CEO_EMAIL","OPENAI_API_KEY"
]

missing = [v for v in required_vars if not os.getenv(v)]
if missing:
    raise RuntimeError(f"Missing required env vars: {', '.join(missing)}")

REVENUE_THRESHOLD = 0.10

def get_revenue_data():
    """
    Get today's revenue and last week's revenue.
    Returns both commission revenue and premium revenue
    """
    engine = create_engine(DATABASE_URL,future= True)    

    with engine.connect() as conn:

        today = datetime.now().date()
        yesterday = today - timedelta(days=1)

        #Query for premium revenue (from policies table)
        premium_query = text("""
                            SELECT DATE(StartDate) as date,
                            SUM(premiumamount) as total_premium,
                            COUNT(*) as policy_count
                            FROM policies
                            WHERE DATE(StartDate) IN (:today, :yesterday)
                            GROUP BY DATE(StartDate)
                            ORDER BY DATE(StartDate)
                            """)
        commission_query = text("""
                                SELECT DATE(saledate) as date,
                                SUM(commissionamount) as total_commission,
                                COUNT(*) as sales_count
                                FROM sales
                                WHERE DATE(saledate) IN (:today, :yesterday)
                                GROUP BY DATE(saledate)
                                ORDER BY DATE(saledate)
                                """)
        
        premium_data = pd.read_sql(premium_query,conn,params={"today":today,"yesterday":yesterday})
        commission_data = pd.read_sql(commission_query,conn,params={"today":today,"yesterday":yesterday})

        return premium_data,commission_data, today,yesterday
    

def calculate_changes(premium_data, commission_data, today, yesterday):
    """
    Calculate % changes and determine if alerts should be sent
    """
    results = {
        'today': today,
        'yesterday': yesterday,
        'premium_today': 0,
        'premium_yesterday': 0,
        'policies_today': 0,
        'policies_yesterday': 0,
        'commission_today': 0,
        'commission_yesterday': 0,
        'sales_today':0,
        'sales_yesterday':0,
        'premium_change_pct': 0,
        'commission_change_pct': 0,
        'should_alert': False,
        'alert_reasons': []
    }

    # Process premium data
    today_premium = premium_data[premium_data['date'] == today]
    yesterday_premium = premium_data[premium_data['date'] == yesterday]

    if not today_premium.empty:
        results['premium_today'] = float(today_premium['total_premium'].iloc[0])
        results['policies_today'] = int(today_premium['policy_count'].iloc[0])

    if not yesterday_premium.empty:
        results['premium_yesterday'] = float(yesterday_premium['total_premium'].iloc[0])
        results['policies_yesterday'] = int(yesterday_premium['policy_count'].iloc[0])

    #Calculate pct change
    if results['premium_yesterday'] > 0:
        results['premium_change_pct'] = ((results['premium_today'] - results['premium_yesterday']) / results['premium_yesterday']) * 100

    #Process commission data
    today_commission = commission_data[commission_data['date'] == today]
    yesterday_commission = commission_data[commission_data['date'] ==yesterday]

    if not today_commission.empty:
        results['commission_today'] = float(today_commission['total_commission'].iloc[0])
        results['sales_today'] = int(today_commission['sales_count'].iloc[0])

    if not yesterday_commission.empty:
        results['commission_yesterday'] = float(yesterday_commission['total_commission'].iloc[0])
        results['sales_yesterday'] = int(yesterday_commission['sales_count'].iloc[0])
    
    #Calculate the percentage change
    if results['commission_yesterday'] > 0:
        results['commission_change_pct'] = ((results['commission_today'] - results['commission_yesterday']) / results['commission_yesterday']) * 100

    threshold_pct = REVENUE_THRESHOLD * 100

    if abs(results['premium_change_pct']) > threshold_pct:
        results['should_alert'] = True
        direction = 'increased' if results['premium_change_pct'] > 0 else "decreased"
        results['alert_reasons'].append(f"Premium revenue {direction} by {abs(results['premium_change_pct']):.1f}%")

    if abs(results['commission_change_pct']) > threshold_pct:
        results['should_alert'] = True
        direction = "increased" if results['commission_change_pct'] > 0 else "decreased"
        results['alert_reasons'].append(f"Commission revenue {direction} by {abs(results['commission_change_pct']):.1f}%")

    return results

def get_ai_summary(results):
    """
    Use CHATGPT to get summary if results['should_alert'] = True
    """

    if not results['should_alert']:
        return "" #do nothing if there is no significant change
    
      # API key check
    if not OPENAI_API_KEY or OPENAI_API_KEY.lower().startswith("your_"):
        return "AI summary unavailable - OpenAI API key not configured."

    try:
        openai.api_key = OPENAI_API_KEY

        prompt = f"""
        today: {results['today']}
        yesterday: {results['yesterday']}

         Premium: ${results['premium_today']:,.2f} vs ${results['premium_yesterday']:,.2f} ({results['policies_today']} vs {results['policies_yesterday']} policies)
        Commission: ${results['commission_today']:,.2f} vs ${results['commission_yesterday']:,.2f} ({results['sales_today']} vs {results['sales_yesterday']} sales)

        premium pct change: {results['premium_change_pct']:+.1f}%
        commission pct change: {results['commission_change_pct']:+.1f}%

        Threshold: {REVENUE_THRESHOLD}
        
        provide a concise 2-3 executive summary with a realistic actionable insight.
        """

        response = openai.ChatCompletion.create(
            model ="gpt-3.5-turbo",
            messages = [{"role":"user","content":prompt}],
            max_tokens = 150,
            temperature = 0.7
        )

        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"AI analysis error: {str(e)}"
        traceback.print_exc()

def print_alert_summary(results, ai_summary):
    """
    Print alert summary to console
    """
    print(f"\n🚨 REVENUE ALERT - {results['today']}")
    print("=" * 50)
    
    for reason in results['alert_reasons']:
        print(f"• {reason}")
    
    print(f"\nToday's Performance:")
    print(f"Premium Revenue: ${results['premium_today']:,.2f} ({results['premium_change_pct']:+.1f}%)")
    print(f"Commission Paid: ${results['commission_today']:,.2f} ({results['commission_change_pct']:+.1f}%)")
    
    print(f"\nYesterday Comparison ({results['yesterday']}):")
    print(f"Premium Revenue: ${results['premium_yesterday']:,.2f}")
    print(f"Commission Paid: ${results['commission_yesterday']:,.2f}")
    
    print(f"\n🤖 AI Insights:")
    print(ai_summary or "N/A")

def send_alert_emails(results, ai_summary):
    """
    Send email alerts with AI summary and insights
    """
    if not GMAIL_USER:
        print("Email not configured ____ will send")
        print_alert_summary(results, ai_summary)
        return

    try:
        # Create email
        msg = MIMEMultipart()
        msg['From'] = GMAIL_USER
        msg['To'] = TO_EMAIL
        msg['Subject'] = f"Insurance Revenue Alert - {results['today']}"

        # Create HTML body
        html_body = f"""
        <html>
        <body>
        <h2>🚨 Revenue Alert - {results['today']}</h2>

        <h3>Alert Reasons:</h3>
        <ul>
        {''.join([f"<li>{reason}</li>" for reason in results['alert_reasons']])}
        </ul>

        <h3>Today's Performance:</h3>
        <table border="1" style="border-collapse: collapse;">
        <tr><th>Metric</th><th>Today</th><th>Yesterday</th><th>Change</th></tr>
        <tr>
          <td>Premium Revenue</td>
          <td>${results['premium_today']:,.2f}</td>
          <td>${results['premium_yesterday']:,.2f}</td>
          <td style="color: {'green' if results['premium_change_pct'] > 0 else 'red'}">
                {results['premium_change_pct']:+.1f}%
          </td>
         </tr>
         <tr>
          <td>Commission Paid</td>
          <td>${results['commission_today']:,.2f}</td>
          <td>${results['commission_yesterday']:,.2f}</td>
          <td style="color: {'green' if results['commission_change_pct'] > 0 else 'red'}">
                {results['commission_change_pct']:+.1f}%
          </td>
         </tr>
         </table>
        
         <h3>🤖 AI Insights:</h3>
         <p><em>{ai_summary}</em></p>

         <hr>
         <small>Automated alert from Imara Insurance Revenue Monitoring System</small>
         </body>
         </html>
         """
        
        msg.attach(MIMEText(html_body, 'html'))

        # Send Email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(GMAIL_USER, GMAIL_PASSWORD)
            server.sendmail(GMAIL_USER, TO_EMAIL, msg.as_string())

        print(f"✅ Alert email sent successfully to {TO_EMAIL}")

    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        print("Alert details:")
        print_alert_summary(results, ai_summary)
        traceback.print_exc()

def main():
    """
    Main function to run the revenue monitoring system
    """
    print(f"🔍 Checking revenue data for {datetime.now().date()}...")
    
    try:
        # Get revenue data
        premium_data, commission_data, today, yesterday = get_revenue_data()
        
        # Calculate changes
        results = calculate_changes(premium_data, commission_data, today, yesterday)
        
        # Get AI summary
        ai_summary = get_ai_summary(results)

        
        # Send alert if needed
        if results['should_alert']:
            send_alert_emails(results, ai_summary)
        else:
            print("✅ No alerts triggered today")
            print(f"Premium change: {results['premium_change_pct']:+.1f}%")
            print(f"Commission change: {results['commission_change_pct']:+.1f}%")
            print(f"Threshold: ±{REVENUE_THRESHOLD * 100}%")

    except Exception as e:
        print(f"❌ Error running revenue monitor: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    try:   
        main()
    except Exception:
        print("\n💥 Crash detected! Dropping into debugger...\n")
        traceback.print_exc()
        pdb.post_mortem()
        sys.exit(1)