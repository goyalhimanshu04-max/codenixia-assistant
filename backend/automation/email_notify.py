import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

def send_lead_notification(lead_data: dict):
    """
    Automation Workflow:
    Lead Form Submission → Email Notification to Admin
    """
    sender = os.getenv("EMAIL_SENDER")
    password = os.getenv("EMAIL_PASSWORD")
    receiver = os.getenv("EMAIL_RECEIVER")

    if not all([sender, password, receiver]):
        print("⚠️  Email credentials not set. Skipping email notification.")
        return False

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"🔔 New Lead: {lead_data.get('name', 'Unknown')}"
        msg["From"] = sender
        msg["To"] = receiver

        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; padding: 20px;">
            <h2 style="color: #4f46e5;">🚀 New Lead Captured — Codenixia Assistant</h2>
            <table style="border-collapse: collapse; width: 100%;">
                <tr><td style="padding: 8px; font-weight:bold;">Name:</td>
                    <td style="padding: 8px;">{lead_data.get('name', '-')}</td></tr>
                <tr style="background:#f3f4f6;"><td style="padding: 8px; font-weight:bold;">Email:</td>
                    <td style="padding: 8px;">{lead_data.get('email', '-')}</td></tr>
                <tr><td style="padding: 8px; font-weight:bold;">Phone:</td>
                    <td style="padding: 8px;">{lead_data.get('phone', '-')}</td></tr>
                <tr style="background:#f3f4f6;"><td style="padding: 8px; font-weight:bold;">Company:</td>
                    <td style="padding: 8px;">{lead_data.get('company', '-')}</td></tr>
                <tr><td style="padding: 8px; font-weight:bold;">Interest:</td>
                    <td style="padding: 8px;">{lead_data.get('interest', '-')}</td></tr>
                <tr style="background:#f3f4f6;"><td style="padding: 8px; font-weight:bold;">Message:</td>
                    <td style="padding: 8px;">{lead_data.get('message', '-')}</td></tr>
            </table>
            <p style="color: #6b7280; margin-top: 20px;">This lead was captured from the AI Business Assistant system.</p>
        </body>
        </html>
        """

        msg.attach(MIMEText(html_body, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.sendmail(sender, receiver, msg.as_string())

        print(f"✅ Email notification sent for lead: {lead_data.get('name')}")
        return True

    except Exception as e:
        print(f"❌ Email failed: {e}")
        return False