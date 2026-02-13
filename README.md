# Productivity MCP Server 🚀

A Model Context Protocol (MCP) server for personal productivity tasks.

## 🎯 Features
- ✅ **send_email_draft**: Create secure email drafts (input sanitized)
- ✅ **add_task**: Add tasks to persistent storage 
- ✅ **professional_email**: Generate professional email templates
- 🔒 **Input Sanitization**: Blocks command injection/CRLF attacks
- 🔒 **Error Disclosure Protection**: Sanitizes error messages

## 🛠️ Quick Start

### 1. Clone & Setup
```bash
git clone <your-repo-url>
cd productivity-mcp-server
uv venv
source .venv/bin/activate  # Mac/Linux
# .venv\Scripts\activate  # Windows
uv pip install -r requirements.txt
cp .env.example .env
### 2. Install Dependencies
\`\`\`bash
uv pip install -r requirements.txt
\`\`\`

### 3. Configure Secrets
Create `.env` file:
\`\`\`
GMAIL_API_KEY=your_key
GOOGLE_CALENDAR_API_KEY=your_key
TASK_DB_PATH=./tasks.json
LOG_LEVEL=INFO
\`\`\`

### 4. Run Server
\`\`\`bash
python server.py
\`\`\`

### 5. Connect to Claude Desktop
Update `~/.config/claude/claude_desktop_config.json` with the server path.

## Tools

### `draft_email`
Draft and send professional emails.

**Inputs**:
- `recipient` (string): Email address
- `subject` (string): Email subject
- `body` (string): Email body
- `send` (boolean, optional): Send vs draft

**Security**: 
- Email header injection prevention
- Input validation and sanitization

**Example**:
\`\`\`
draft_email(
  recipient="hiring@company.com",
  subject="Internship Application",
  body="I'm interested in...",
  send=False
)
\`\`\`

### `create_task`
Create tasks with deadlines (rate limited).

**Inputs**:
- `title` (string): Task name
- `description` (string, optional)
- `deadline` (string, optional): ISO format YYYY-MM-DD
- `priority` (string): low/medium/high

**Security**:
- Rate limited to 10 tasks/minute
- Input length limits

**Example**:
\`\`\`
create_task(
  title="Review resume",
  deadline="2026-02-15",
  priority="high"
)
\`\`\`

## Resources

### `tasks://all`
Lists all tasks from the database.

## Prompts

### `professional_email`
Template for drafting professional emails.
**Arguments**:
- `recipient_name`: Who you're writing to
- `purpose`: What you're requesting
