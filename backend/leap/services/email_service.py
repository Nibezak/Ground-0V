import os
import logging
from typing import Optional
import subprocess
# import tempfile # No longer needed for Resend API call

# Removed SendGrid imports:
# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        # Reverted to RESEND_API_KEY
        self.api_key = os.environ.get("RESEND_API_KEY")
        # Consistent 'from' email for Resend, ensure this is verified in your Resend account.
        # The name part "Ground-0 by packman" will be part of the 'from' field in the JSON payload.
        self.from_email_address = "info@payflow.dev" 

        if not self.api_key:
            logger.warning("RESEND_API_KEY not found. Email notifications disabled.")
        else:
            logger.info("Resend API key found. Email notifications enabled.")

    def send_animation_ready_notification(self, email: str, job_id: str, video_url: str) -> bool:
        """Send notification when animation is ready using Resend API with curl."""
        if not self.api_key:
            logger.error("RESEND_API_KEY is not set. Cannot send email.")
            return False
        if not email:
            logger.warning("Recipient email missing. Cannot send email.")
            return False

        subject = "Your Ground-0 by packman Animation is Ready!"
        # Using f-string for cleaner HTML content generation
        html_content = f"""
            <h1>Your animation is ready!</h1>
            <p>Your requested animation has been generated and is ready to view.</p>
            <p><a href="{video_url}">Click here to view your animation</a></p>
            <p>Job ID: {job_id}</p>
            <p>Thank you for using Ground-0 by packman!</p>
        """

        # Constructing the JSON payload string manually to ensure proper escaping for the -d argument
        # Double quotes inside the JSON string need to be escaped for the shell.
        # Python's json.dumps can help, but for direct curl -d, manual construction is also common.
        # Let's ensure html_content is properly escaped for JSON.
        # A simple way is to replace " with \\" and newlines with \\\\n if putting directly in shell string,
        # but subprocess handles arguments, so we just need a valid JSON string.
        
        # Python's json.dumps will handle escaping for us if we build a dict first
        import json
        payload_dict = {
            "from": f"Ground-0 by packman <{self.from_email_address}>",
            "to": [email], # Resend API expects 'to' to be an array
            "subject": subject,
            "html": html_content
        }
        json_payload = json.dumps(payload_dict)

        curl_command = [
            "curl", 
            "-o", "NUL", # For Windows, discards output. Use "/dev/null" for Linux/macOS
            "-s",         # Silent mode
            "-w", "%{http_code}", # Output only the HTTP status code
            "-X", "POST", "https://api.resend.com/emails",
            "-H", f"Authorization: Bearer {self.api_key}",
            "-H", "Content-Type: application/json",
            "-d", json_payload
        ]

        try:
            process = subprocess.run(curl_command, capture_output=True, text=True, check=False)
            status_code = process.stdout.strip() # http_code from -w
            
            if status_code == "200":
                logger.info(f"Email notification sent to {email} via Resend. Status code: {status_code}")
                return True
            else:
                # Resend might return more detailed errors in the response body (which we are discarding with -o NUL)
                # For debugging, you might want to capture stderr or remove -o NUL and -s temporarily
                logger.error(f"Failed to send email notification via Resend. HTTP Status code: {status_code}. Stderr: {process.stderr}. Curl stdout (should be empty if -o NUL used): {process.stdout}")
                return False
        except FileNotFoundError:
            logger.error("curl command not found. Please ensure curl is installed and in your PATH.")
            return False
        except Exception as e:
            logger.error(f"Failed to send email notification using Resend curl: {str(e)}")
            return False
