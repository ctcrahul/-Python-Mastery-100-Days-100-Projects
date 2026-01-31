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

    for _, row in df.iterrows():
        report += f"{row['Metric']}: {row['Value']}\n"

    report += "\nRegards,\nAutomated Reporting System"
    return report

# -----------------------------
# SEND EMAIL
# -----------------------------
def send_email(subject, body):
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SENDER_EMAIL, APP_PASSWORD)
    server.send_message(msg)
    server.quit()

# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    print("📧 Sending Automated Email Report...")

    report_text = generate_report(df)
    subject = "Daily Automated Report"

    send_email(subject, report_text)

    print("✅ Email sent successfully")
