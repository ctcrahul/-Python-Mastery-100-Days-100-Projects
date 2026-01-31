# Automated Email Reports (Single File)
# Generates a report and emails it automatically

import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# -----------------------------
# EMAIL CONFIG
# -----------------------------
SENDER_EMAIL = "your_email@gmail.com"
APP_PASSWORD = "your_app_password"
RECEIVER_EMAIL = "receiver_email@gmail.com"

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587



# -----------------------------
# SAMPLE DATA (REPLACE WITH REAL)
# -----------------------------
data = {
    "Metric": ["Total Users", "Active Users", "Revenue", "Errors"],
    "Value": [1200, 860, "$5,430", 3]
}

df = pd.DataFrame(data)

# -----------------------------
# GENERATE REPORT
# -----------------------------
def generate_report(df):
    date = datetime.now().strftime("%Y-%m-%d")

    report = f"""
📊 DAILY AUTOMATED REPORT
Date: {date}

------------------------
"""
