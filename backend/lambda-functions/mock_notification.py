import json
from datetime import datetime


def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type,Authorization",
            "Access-Control-Allow-Methods": "OPTIONS,POST"
        },
        "body": json.dumps(body)
    }


def parse_body(event):
    if "body" not in event or not event["body"]:
        return {}

    if isinstance(event["body"], dict):
        return event["body"]

    return json.loads(event["body"])


def lambda_handler(event, context):
    try:
        method = event.get("requestContext", {}).get("http", {}).get("method")

        if method == "OPTIONS":
            return response(200, {"message": "CORS preflight success"})

        if method != "POST":
            return response(405, {"error": "Method not allowed"})

        body = parse_body(event)

        required_fields = ["email", "company", "role", "followUpDate"]

        for field in required_fields:
            if field not in body or not body[field]:
                return response(400, {"error": f"{field} is required"})

        email = body["email"]
        company = body["company"]
        role = body["role"]
        follow_up_date = body["followUpDate"]

        subject = f"Follow-up Reminder: {company} {role} Application"

        email_body = (
            f"Hi Manasa,\n\n"
            f"This is a reminder to follow up on your {company} {role} application.\n\n"
            f"Follow-up Date: {follow_up_date}\n\n"
            f"Good luck!\n"
            f"JobTrackr AI"
        )

        mock_notification = {
            "to": email,
            "subject": subject,
            "body": email_body,
            "generatedAt": datetime.utcnow().isoformat()
        }

        return response(200, {
            "message": "Mock notification generated successfully",
            "emailPreview": mock_notification
        })

    except json.JSONDecodeError:
        return response(400, {"error": "Invalid JSON body"})

    except Exception as e:
        print("Unexpected error:", str(e))
        return response(500, {"error": "Internal server error"})