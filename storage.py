import boto3
import uuid
from datetime import datetime

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Appointments")  # Make sure the table exists in AWS Console

def save_appointment(patient_name, dob, preferred_date):
    appointment_id = str(uuid.uuid4())
    item = {
        "appointment_id": appointment_id,
        "patient_name": patient_name,
        "dob": dob,
        "preferred_date": preferred_date,
        "created_at": datetime.utcnow().isoformat()
    }
    table.put_item(Item=item)
    return appointment_id
