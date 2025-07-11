import boto3
import json
import os
from dotenv import load_dotenv

# Load AWS credentials from .env
load_dotenv()

# Initialize Bedrock client
bedrock = boto3.client(
    "bedrock-runtime",
    region_name=os.getenv("AWS_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)

# Claude 3 Sonnet Model ID
MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"

def analyze_user_input(user_input: str) -> dict:
    """
    Uses Claude 3 Sonnet to:
    - Detect user intent
    - Extract entities (patient_name, dob, preferred_date)
    Returns:
        {
            "intent": "schedule",
            "entities": {
                "patient_name": "John Doe",
                "dob": "YYYY-MM-DD",
                "preferred_date": "July 10 at 10am"
            }
        }
    """
    # Messages API payload
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "messages": [
            {
                "role": "user",
                "content": f"""
Classify the intent and extract entities from this text:
\"{user_input}\"

- intent: One of ["schedule", "onboard", "operator"]
- patient_name: Full name of patient if available
- dob: Date of birth in YYYY-MM-DD format if mentioned
- preferred_date: Appointment date and time if mentioned

Return JSON like:
{{
  "intent": "schedule",
  "entities": {{
    "patient_name": "John Doe",
    "dob": "YYYY-MM-DD",
    "preferred_date": "July 10 at 10am"
  }}
}}

If any field is missing, set it to null.
"""
            }
        ],
        "max_tokens": 800,
        "temperature": 0.2,
        "top_p": 1.0
    }

    response = bedrock.invoke_model(
        modelId=MODEL_ID,
        body=json.dumps(body),
        contentType="application/json",
        accept="application/json"
    )

    # Parse Claude 3 response
    response_body = json.loads(response["body"].read())
    content_blocks = response_body.get("content", [])
    text_response = ""
    for block in content_blocks:
        if block.get("type") == "text":
            text_response += block.get("text", "")

    try:
        result = json.loads(text_response)
    except json.JSONDecodeError:
        print("❌ Failed to parse Bedrock response as JSON")
        result = {
            "intent": None,
            "entities": {}
        }

    return result
