# prompts/email_prompt.py
EMAIL_TEMPLATE_PROMPT = """You are drafting a professional email.

Recipient: {recipient_name}
Purpose: {purpose}

Generate a concise, professional email that:
1. Opens with a clear, personalized greeting
2. States the purpose in the first sentence
3. Includes 1-2 specific details or value proposition
4. Closes with a clear call to action
5. Maintains a professional but warm tone

Subject line should be compelling and specific (max 50 chars).
Body should be 150-250 words.

Generate the email in this format:
To: [email address]
Subject: [subject line]
Body:
[email body]
"""
