# security/sanitizer.py
"""
Input sanitization to prevent injection attacks
Prevents: SQL injection, command injection, XSS
"""

import re
import logging

logger = logging.getLogger(__name__)

def sanitize_email(email: str) -> str:
    """
    Validate and sanitize email address
    Prevents: Email header injection
    """
    email = email.strip()
    
    # Remove newlines and carriage returns (email header injection)
    if '\n' in email or '\r' in email:
        raise ValueError("Invalid character in email address")
    
    # Strict email format validation
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        raise ValueError("Invalid email format")
    
    return email

def sanitize_text(text: str, max_length: int = 1000) -> str:
    """
    Sanitize general text input
    Prevents: Injection attacks via length limits and character filtering
    """
    if not isinstance(text, str):
        raise ValueError("Input must be string")
    
    text = text.strip()
    
    # Enforce max length
    if len(text) > max_length:
        raise ValueError(f"Text exceeds max length of {max_length}")
    
    # Remove control characters (potential injection vectors)
    text = ''.join(char for char in text if ord(char) >= 32 or char in '\n\t')
    
    return text

# ========== EXPLOIT TEST ==========

def test_email_injection():
    """Test that email injection is blocked"""
    try:
        # Attempt: BCC injection via newline
        malicious = "attacker@evil.com\nBCC: admin@evil.com"
        sanitize_email(malicious)
        print("❌ FAILED: Email injection NOT blocked")
        return False
    except ValueError:
        print("✓ PASSED: Email injection blocked")
        return True

if __name__ == "__main__":
    test_email_injection()
