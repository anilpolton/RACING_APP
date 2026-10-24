import os
import json
import urllib.request
from typing import Optional
from config import config

class EmailAlertService:
    """
    Direct Email Delivery via Resend API (HTTP REST).
    Reliably transmits race predictions and Place Accumulator cards to anilpolton@live.co.za.
    """

    def __init__(self):
        self.recipient = config.TARGET_EMAIL
        self.api_key = config.RESEND_API_KEY
        self.sender = config.EMAIL_FROM

    def send_email(self, subject: str, body_text: str, recipient: Optional[str] = None) -> bool:
        to_email = recipient or self.recipient
        print(f"📧 Transmitting email alert to: {to_email} via Resend API...")

        html_body = f"""
        <div style="font-family: Arial, sans-serif; background-color: #f7f9fa; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 8px; border: 1px solid #e1e8ed; overflow: hidden;">
                <div style="background-color: #0b1f3a; color: #ffffff; padding: 16px 20px;">
                    <h2 style="margin: 0; font-size: 20px;">🏇 Antigravity Racing Predictions</h2>
                </div>
                <div style="padding: 24px; color: #333333; line-height: 1.6;">
                    <pre style="font-family: inherit; font-size: 15px; white-space: pre-wrap; margin: 0;">{body_text}</pre>
                </div>
                <div style="background-color: #f1f5f9; padding: 12px 20px; font-size: 12px; color: #64748b; text-align: center;">
                    ⚡ Powered by Antigravity Quantitative Analytics
                </div>
            </div>
        </div>
        """

        payload = {
            "from": self.sender,
            "to": [to_email],
            "subject": subject,
            "text": body_text,
            "html": html_body
        }

        try:
            req = urllib.request.Request(
                "https://api.resend.com/emails",
                data=json.dumps(payload).encode("utf-8"),
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "User-Agent": "AntigravityRacing/1.0"
                },
                method="POST"
            )

            with urllib.request.urlopen(req, timeout=15) as resp:
                resp_data = json.loads(resp.read().decode("utf-8"))
                email_id = resp_data.get("id")
                print(f"✅ Email successfully delivered to {to_email}! Message ID: {email_id}")

                log_dir = os.path.dirname(__file__)
                log_path = os.path.join(log_dir, "last_email_sent.txt")
                with open(log_path, "w", encoding="utf-8") as f:
                    f.write(f"ID: {email_id}\nTo: {to_email}\nSubject: {subject}\n\n{body_text}")

                return True

        except urllib.error.HTTPError as e:
            err_content = e.read().decode("utf-8")
            print(f"⚠️ Resend HTTP Error {e.code}: {err_content}")
            return False
        except Exception as e:
            print(f"⚠️ Unexpected error sending email: {e}")
            return False
