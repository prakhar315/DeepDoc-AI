from app.services.utils import process_and_index_text
import uuid

seed_documents = [
    {
        "text": """Annual Leave Policy:
Full-time employees are entitled to 25 vacation days annually.
Requests should be submitted at least 2 weeks in advance via the HR portal.
Leave approval is subject to manager discretion and team availability.""",
        "metadata": {
            "department": "HR",
            "title": "Annual Leave Policy",
            "doc_id": str(uuid.uuid4())
        }
    },
    {
        "text": """Employee Onboarding Checklist:
- Submit tax and identification documents
- Set up your company email and workstation
- Complete orientation training
- Meet your assigned mentor""",
        "metadata": {
            "department": "HR",
            "title": "Onboarding Checklist",
            "doc_id": str(uuid.uuid4())
        }
    },
    {
        "text": """Password Reset Guide:
If you forget your password:
1. Visit the internal login page.
2. Click 'Forgot Password'.
3. Enter your company email.
4. Follow the reset link sent to your inbox.""",
        "metadata": {
            "department": "IT",
            "title": "Password Reset Instructions",
            "doc_id": str(uuid.uuid4())
        }
    },
    {
        "text": """VPN Setup Instructions:
To access company resources remotely:
1. Install the GlobalProtect VPN client.
2. Login using your SSO credentials.
3. Contact IT support if connection fails or errors occur.""",
        "metadata": {
            "department": "IT",
            "title": "VPN Setup Guide",
            "doc_id": str(uuid.uuid4())
        }
    },
    {
        "text": """Support Ticket Escalation Process:
- Tier 1 handles initial inquiries.
- If unresolved within 24 hours, escalate to Tier 2.
- Urgent issues should be flagged and sent to Incident Management.""",
        "metadata": {
            "department": "Support",
            "title": "Ticket Escalation Policy",
            "doc_id": str(uuid.uuid4())
        }
    },
    {
        "text": """Live Chat Agent Guidelines:
- Respond to initial customer messages within 2 minutes.
- Use a friendly and professional tone.
- Avoid technical jargon unless necessary.
- Escalate issues you cannot resolve within 5 minutes.""",
        "metadata": {
            "department": "Support",
            "title": "Live Chat Best Practices",
            "doc_id": str(uuid.uuid4())
        }
    }
]

def insert_seed_data():
    for doc in seed_documents:
        print(f"Seeding: {doc['metadata']['doc_id']}")
        process_and_index_text(
            text=doc["text"],
            base_metadata=doc["metadata"]
        )
