# tools/email_tool.py
"""
Email drafting tool with input sanitization
Prevents command injection and validates email addresses
"""

import re
import logging
from typing import Dict, Any
from security.sanitizer import sanitize_email, sanitize_text

logger = logging.getLogger(__name__)

async def draft_email(
    recipient: str,
    subject: str,
    body: str,
    send: bool = False
) -> str:
    """
    Draft or send an email with Gmail API
    
    Args:
        recipient: Email address (validated)
        subject: Email subject
        body: Email body
        send: If True, send email; if False, draft only
    
    Returns:
        Confirmation message
    """
    try:
        # SECURITY: Input sanitization
        recipient = sanitize_email(recipient)
        subject = sanitize_text(subject, max_length=200)
        body = sanitize_text(body, max_length=5000)
        
        # Validate recipient format
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, recipient):
            return f"Error: Invalid email address format"
        
        # Mock Gmail API (replace with real API call)
        email_data = {
            "to": recipient,
            "subject": subject,
            "body": body,
            "status": "sent" if send else "drafted"
        }
        
        action = "sent to" if send else "drafted for"
        logger.info(f"Email {action} {recipient}: {subject[:50]}...")
        
        return f"✓ Email {action} {recipient}\nSubject: {subject}\nBody preview: {body[:100]}..."
    
    except ValueError as e:
        logger.warning(f"Input validation error: {str(e)}")
        return f"Error: {str(e)}"
    except Exception as e:
        logger.error(f"Unexpected error in draft_email: {str(e)}")
        return "Error: Failed to draft email"
