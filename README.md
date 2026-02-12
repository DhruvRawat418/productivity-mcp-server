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