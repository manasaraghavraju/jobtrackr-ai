import boto3
import uuid
from datetime import datetime

dynamodb = boto3.resource("dynamodb")

applications_table = dynamodb.Table("Applications")
tasks_table = dynamodb.Table("Tasks")


def create_application(user_id, company, role, status):
    application = {
        "userId": user_id,
        "applicationId": str(uuid.uuid4()),
        "company": company,
        "role": role,
        "status": status,
        "createdAt": datetime.utcnow().isoformat(),
        "updatedAt": datetime.utcnow().isoformat()
    }

    applications_table.put_item(Item=application)

    return application


def get_user_applications(user_id):
    response = applications_table.query(
        KeyConditionExpression="userId = :userId",
        ExpressionAttributeValues={
            ":userId": user_id
        }
    )

    return response["Items"]


def create_task(user_id, title, category, status):
    task = {
        "userId": user_id,
        "taskId": str(uuid.uuid4()),
        "title": title,
        "category": category,
        "status": status,
        "createdAt": datetime.utcnow().isoformat(),
        "updatedAt": datetime.utcnow().isoformat()
    }

    tasks_table.put_item(Item=task)

    return task