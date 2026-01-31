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
