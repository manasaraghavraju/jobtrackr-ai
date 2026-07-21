import json
import uuid
import boto3
import logging
import base64
from typing import Any
from datetime import datetime
from boto3.dynamodb.conditions import Attr, Key
from botocore.exceptions import ClientError
from cache_service import delete_cached_value

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Applications")

ALLOWED_STATUSES = [
    "Saved",
    "Applied",
    "Online Assessment",
    "Interview",
    "Rejected",
    "Offer",
    "Accepted"
]


def response(status_code, body):
    logger.info({
        "statusCode": status_code,
        "responseBody": body
    })

    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type,Authorization",
            "Access-Control-Allow-Methods": "OPTIONS,GET,POST,PATCH"
        },
        "body": json.dumps(body)
    }


def parse_body(event):
    if "body" not in event or not event["body"]:
        return {}

    if isinstance(event["body"], dict):
        return event["body"]

    return json.loads(event["body"])

def encode_next_token(last_evaluated_key: dict[str, Any] | None) -> str | None:
    """
    Convert DynamoDB LastEvaluatedKey into a URL-safe token.
    """

    if not last_evaluated_key:
        return None

    token_json = json.dumps(last_evaluated_key)

    return base64.urlsafe_b64encode(
        token_json.encode("utf-8")
    ).decode("utf-8")


def decode_next_token(next_token: str | None) -> dict[str, Any] | None:
    """
    Convert the API nextToken back into DynamoDB ExclusiveStartKey.
    """

    if not next_token:
        return None

    try:
        decoded_bytes = base64.urlsafe_b64decode(
            next_token.encode("utf-8")
        )

        decoded_value = json.loads(
            decoded_bytes.decode("utf-8")
        )

        if not isinstance(decoded_value, dict):
            raise ValueError("Decoded token is not an object")

        return decoded_value

    except (ValueError, json.JSONDecodeError, UnicodeDecodeError) as error:
        raise ValueError("Invalid nextToken") from error


def validate_iso_date(date_value: str, field_name: str) -> str | None:
    """
    Validate dates in YYYY-MM-DD format.
    Returns an error message when invalid, otherwise None.
    """

    try:
        datetime.strptime(date_value, "%Y-%m-%d")
        return None
    except ValueError:
        return f"{field_name} must use YYYY-MM-DD format"

def build_application_filter(
    company: str | None,
    status: str | None,
    role: str | None,
    search: str | None,
    date_from: str | None,
    date_to: str | None,
):
    """
    Build one DynamoDB FilterExpression from optional filters.
    """

    filter_expression = None

    def add_condition(condition):
        nonlocal filter_expression

        if filter_expression is None:
            filter_expression = condition
        else:
            filter_expression = filter_expression & condition

    if company:
        add_condition(
            Attr("companyLower").contains(company.strip().lower())
        )

    if role:
        add_condition(
            Attr("roleLower").contains(role.strip().lower())
        )

    if status:
        add_condition(
            Attr("status").eq(status)
        )

    if search:
        normalized_search = search.strip().lower()

        search_condition = (
            Attr("companyLower").contains(normalized_search)
            | Attr("roleLower").contains(normalized_search)
        )

        add_condition(search_condition)

    if date_from:
        add_condition(
            Attr("appliedDate").gte(date_from)
        )

    if date_to:
        add_condition(
            Attr("appliedDate").lte(date_to)
        )

    return filter_expression

def validate_create_application(body):
    required_fields = ["userId", "company", "role", "status"]

    for field in required_fields:
        if field not in body or not body[field]:
            return f"{field} is required"

    if body["status"] not in ALLOWED_STATUSES:
        return "Invalid status value"

    return None


def create_application(event):
    body = parse_body(event)

    validation_error = validate_create_application(body)

    if validation_error:
        return response(400, {"error": validation_error})

    now = datetime.utcnow().isoformat()

    application = {
        "userId": body["userId"],
        "applicationId": str(uuid.uuid4()),
        "company": body["company"].strip(),
        "companyLower": body["company"].strip().lower(),
        "role": body["role"].strip(),
        "roleLower": body["role"].strip().lower(),
        "status": body["status"],
        "appliedDate": body.get("appliedDate"),
        "jobLink": body.get("jobLink"),
        "notes": body.get("notes"),
        "createdAt": now,
        "updatedAt": now,
    }

    logger.info({
        "message": "Creating application",
        "userId": application["userId"],
        "applicationId": application["applicationId"],
        "company": application["company"]
    })

    table.put_item(Item=application)

    delete_cached_value(
        f"dashboard:metrics:{application['userId']}"
    )

    return response(201, {
        "message": "Application created successfully",
        "application": application
    })


def get_applications(event):
    query_params = event.get("queryStringParameters") or {}

    user_id = query_params.get("userId")
    limit_value = query_params.get("limit", "10")
    sort_order = query_params.get("sortOrder", "desc").lower()
    next_token = query_params.get("nextToken")

    company = query_params.get("company")
    status = query_params.get("status")
    role = query_params.get("role")
    search = query_params.get("search")
    date_from = query_params.get("dateFrom")
    date_to = query_params.get("dateTo")

    # -----------------------------
    # Validate userId
    # -----------------------------

    if not user_id:
        return response(400, {
            "error": "userId query parameter is required"
        })

    # -----------------------------
    # Validate limit
    # -----------------------------

    try:
        limit = int(limit_value)
    except ValueError:
        return response(400, {
            "error": "limit must be an integer"
        })

    if limit < 1 or limit > 50:
        return response(400, {
            "error": "limit must be between 1 and 50"
        })

    # -----------------------------
    # Validate sorting
    # -----------------------------

    if sort_order not in {"asc", "desc"}:
        return response(400, {
            "error": "sortOrder must be asc or desc"
        })

    # -----------------------------
    # Validate status
    # -----------------------------

    if status and status not in ALLOWED_STATUSES:
        return response(400, {
            "error": "Invalid status value"
        })

    # -----------------------------
    # Validate dates
    # -----------------------------

    if date_from:
        date_error = validate_iso_date(date_from, "dateFrom")

        if date_error:
            return response(400, {
                "error": date_error
            })

    if date_to:
        date_error = validate_iso_date(date_to, "dateTo")

        if date_error:
            return response(400, {
                "error": date_error
            })

    if date_from and date_to and date_from > date_to:
        return response(400, {
            "error": "dateFrom cannot be later than dateTo"
        })

    # -----------------------------
    # Decode pagination token
    # -----------------------------

    try:
        exclusive_start_key = decode_next_token(next_token)
    except ValueError:
        return response(400, {
            "error": "Invalid nextToken"
        })

    # -----------------------------
    # Build DynamoDB filters
    # -----------------------------

    filter_expression = build_application_filter(
        company=company,
        status=status,
        role=role,
        search=search,
        date_from=date_from,
        date_to=date_to,
    )

    query_arguments = {
        "KeyConditionExpression": Key("userId").eq(user_id),
        "Limit": limit,
        "ScanIndexForward": sort_order == "asc",
    }

    if exclusive_start_key:
        query_arguments["ExclusiveStartKey"] = exclusive_start_key

    if filter_expression is not None:
        query_arguments["FilterExpression"] = filter_expression

    logger.info({
        "message": "Searching and filtering applications",
        "userId": user_id,
        "limit": limit,
        "sortOrder": sort_order,
        "company": company,
        "status": status,
        "role": role,
        "search": search,
        "dateFrom": date_from,
        "dateTo": date_to,
        "hasNextToken": next_token is not None,
    })

    result = table.query(**query_arguments)

    applications = result.get("Items", [])

    encoded_next_token = encode_next_token(
        result.get("LastEvaluatedKey")
    )

    active_filters = {
        "company": company,
        "status": status,
        "role": role,
        "search": search,
        "dateFrom": date_from,
        "dateTo": date_to,
    }

    active_filters = {
        key: value
        for key, value in active_filters.items()
        if value is not None and value != ""
    }

    return response(200, {
        "applications": applications,
        "pagination": {
            "limit": limit,
            "returnedCount": len(applications),
            "nextToken": encoded_next_token,
            "hasMore": encoded_next_token is not None,
        },
        "sorting": {
            "sortBy": "applicationId",
            "sortOrder": sort_order,
        },
        "filters": active_filters,
    })


def update_application(event):
    body = parse_body(event)

    user_id = body.get("userId")
    application_id = body.get("applicationId")

    if not user_id or not application_id:
        return response(400, {
            "error": "userId and applicationId are required"
        })

    allowed_update_fields = [
        "company",
        "role",
        "status",
        "appliedDate",
        "jobLink",
        "notes"
    ]

    update_fields = {}

    for field in allowed_update_fields:
        if field in body:
            update_fields[field] = body[field]

    if "company" in update_fields:
        company = update_fields["company"].strip()

        if not company:
            return response(400, {
                "error": "company cannot be empty"
            })

        update_fields["company"] = company
        update_fields["companyLower"] = company.lower()

    if "role" in update_fields:
        role = update_fields["role"].strip()

        if not role:
            return response(400, {
                "error": "role cannot be empty"
            })

        update_fields["role"] = role
        update_fields["roleLower"] = role.lower()

    if not update_fields:
        return response(400, {
            "error": "At least one field is required to update"
        })

    if "status" in update_fields and update_fields["status"] not in ALLOWED_STATUSES:
        return response(400, {
            "error": "Invalid status value"
        })

    update_fields["updatedAt"] = datetime.utcnow().isoformat()

    update_expression_parts = []
    expression_attribute_names = {}
    expression_attribute_values = {}

    for field, value in update_fields.items():
        update_expression_parts.append(f"#{field} = :{field}")
        expression_attribute_names[f"#{field}"] = field
        expression_attribute_values[f":{field}"] = value

    update_expression = "SET " + ", ".join(update_expression_parts)

    try:
        result = table.update_item(
            Key={
                "userId": user_id,
                "applicationId": application_id
            },
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="ALL_NEW",
            ConditionExpression="attribute_exists(applicationId)"
        )

        delete_cached_value(
            f"dashboard:metrics:{user_id}"
        )

        return response(200, {
            "message": "Application updated successfully",
            "application": result["Attributes"]
        })

    except ClientError as e:
        logger.error({
            "message": "DynamoDB update failed",
            "errorCode": e.response["Error"]["Code"],
            "errorMessage": e.response["Error"]["Message"]
        })

        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            return response(404, {
                "error": "Application not found"
            })

        return response(500, {
            "error": "Could not update application"
        })


def lambda_handler(event, context):

    logger.info({
        "message": "Received request",
        "method": event.get("requestContext", {}).get("http", {}).get("method"),
        "path": event.get("rawPath"),
        "queryParams": event.get("queryStringParameters")
    })
    try:
        method = event.get("requestContext", {}).get("http", {}).get("method")

        if method == "OPTIONS":
            return response(200, {"message": "CORS preflight success"})

        if method == "POST":
            return create_application(event)

        if method == "GET":
            return get_applications(event)

        if method == "PATCH":
            return update_application(event)

        return response(405, {"error": "Method not allowed"})

    except json.JSONDecodeError:
        return response(400, {"error": "Invalid JSON body"})

    except Exception as e:
        logger.exception("Unexpected server error")
        return response(500, {
            "error": "Internal server error",
            "message": "Something went wrong while processing the request"
        })