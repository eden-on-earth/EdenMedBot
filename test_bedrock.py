import boto3
import json
import os
from dotenv import load_dotenv

# Load AWS credentials
load_dotenv()

# Initialize Bedrock client
bedrock = boto3.client(
    "bedrock-runtime",
    region_name=os.getenv("AWS_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)

# Prepare Claude 3 Messages API payload
body = {
    "anthropic_version": "bedrock-2023-05-31",
    "messages": [
        {
            "role": "user",
            "content": """Extract patient_name, dob, and preferred_date from:
"Hi, I’m Sarah Connor born May 14, 1985. I want an appointment on July 15 at 3pm."

Return JSON like:
{
  "patient_name": "John Doe",
  "dob": "YYYY-MM-DD",
  "preferred_date": "July 10 at 10am"
}"""
        }
    ],
    "max_tokens": 500,
    "temperature": 0.2,
    "top_p": 1.0
}

# Call Claude 3 Sonnet
response = bedrock.invoke_model(
    modelId="anthropic.claude-3-sonnet-20240229-v1:0",
    body=json.dumps(body),
    contentType="application/json",
    accept="application/json"
)

# Parse and print response
response_body = json.loads(response["body"].read())
print("Raw response from Claude 3 Sonnet:")
print(response_body)
