import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.celery_app import celery_app
from app.core.config import settings

logger = logging.getLogger(__name__)

def generate_verification_html(child_name: str, verification_code: str) -> str:
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #F0F9FF; margin: 0; padding: 20px; }}
        .container {{ max-width: 520px; margin: 0 auto; background: #ffffff; border-radius: 24px; padding: 32px; border: 3px solid #E2E8F0; box-shadow: 0 10px 25px rgba(0,0,0,0.05); text-align: center; }}
        .header-emoji {{ font-size: 54px; margin-bottom: 8px; }}
        .title {{ font-size: 24px; font-weight: 900; color: #1E293B; margin-bottom: 8px; }}
        .subtitle {{ font-size: 15px; color: #64748B; margin-bottom: 24px; line-height: 1.5; }}
        .code-box {{ background: #FFF0EB; border: 3px dashed #FF6B6B; border-radius: 18px; padding: 18px; margin: 24px 0; }}
        .code-label {{ font-size: 13px; font-weight: 800; color: #E11D48; text-transform: uppercase; margin-bottom: 6px; letter-spacing: 1px; }}
        .otp-code {{ font-size: 38px; font-weight: 900; color: #FF6B6B; letter-spacing: 8px; }}
        .info-card {{ background: #F8FAFC; border-radius: 16px; padding: 16px; font-size: 13px; color: #475569; text-align: left; margin-bottom: 24px; border: 1px solid #E2E8F0; }}
        .footer {{ font-size: 12px; color: #94A3B8; margin-top: 24px; }}
      </style>
    </head>
    <body>
      <div class="container">
        <div class="header-emoji">🎈🦁✨</div>
        <div class="title">Welcome to English for Kids!</div>
        <div class="subtitle">
          Hello Parent! We are super excited to welcome <strong>{child_name}</strong> to the fun English learning world!
        </div>

        <div class="code-box">
          <div class="code-label">Your 6-Digit Verification Code</div>
          <div class="otp-code">{verification_code}</div>
        </div>

        <div class="info-card">
          <p style="margin: 0 0 6px 0;"><strong>💡 Quick Instructions:</strong></p>
          <ul style="margin: 0; padding-left: 20px;">
            <li>Enter this code in the app to activate your child's learning profile.</li>
            <li>This code is valid for <strong>{settings.EMAIL_VERIFICATION_EXPIRE_MINUTES} minutes</strong>.</li>
            <li>If you did not request this, please safely ignore this email.</li>
          </ul>
        </div>

        <div class="footer">
          &copy; 2026 English for Kids App. Built with ❤️ for young learners.
        </div>
      </div>
    </body>
    </html>
    """

@celery_app.task(name="send_verification_email_task", bind=True, max_retries=3)
def send_verification_email_task(self, to_email: str, child_name: str, verification_code: str):
    """
    Celery Background Task to send email verification code via SMTP (or log in dev).
    """
    subject = f"✨ Verify your English for Kids account ({verification_code})"
    html_content = generate_verification_html(child_name, verification_code)

    # 1. Check if SMTP credentials are fully provided
    if settings.SMTP_USER and settings.SMTP_PASSWORD and settings.SMTP_HOST:
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"{settings.EMAILS_FROM_NAME} <{settings.EMAILS_FROM_EMAIL}>"
            msg["To"] = to_email

            part = MIMEText(html_content, "html")
            msg.attach(part)

            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                if settings.SMTP_TLS:
                    server.starttls()
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.sendmail(settings.EMAILS_FROM_EMAIL, [to_email], msg.as_string())

            logger.info(f"✅ Verification email sent successfully to {to_email} via SMTP!")
            return {"status": "sent", "email": to_email}
        except Exception as exc:
            logger.error(f"❌ Failed to send verification email to {to_email}: {exc}")
            raise self.retry(exc=exc, countdown=10)
    else:
        # 2. Local / Development fallback logging with high visibility
        print("=" * 60)
        print("📨 [CELERY BACKGROUND EMAIL TASK]")
        print(f"👉 To: {to_email} (Child: {child_name})")
        print(f"🔑 VERIFICATION OTP CODE: >>> {verification_code} <<<")
        print(f"⏱️ Valid for: {settings.EMAIL_VERIFICATION_EXPIRE_MINUTES} minutes")
        print("=" * 60)
        return {"status": "logged_dev", "email": to_email, "code": verification_code}
