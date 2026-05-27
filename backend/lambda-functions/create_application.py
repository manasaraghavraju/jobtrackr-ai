import json
import uuid
from datetime import datetime

def lambda_handler(event, context):
    try:
        body = json.loads(event["body"])

        required_fields = ["userId", "company", "role", "status"]

        for field in required_fields:
            if field not in body or not body[field]:
                return {
                    "statusCode": 400,
                    "body": json.dumps({
                        "error": f"{field} is required"
                    })
                }

        application = {
            "applicationId": str(uuid.uuid4()),
            "userId": body["userId"],
            "company": body["company"],
            "role": body["role"],
            "status": body["status"],
            "appliedDate": body.get("appliedDate"),
            "jobLink": body.get("jobLink"),
            "notes": body.get("notes"),
            "createdAt": datetime.utcnow().isoformat()
        }

        return {
            "statusCode": 201,
            "body": json.dumps({
                "message": "Application added successfully",
                "application": application
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(e)
            })
        }