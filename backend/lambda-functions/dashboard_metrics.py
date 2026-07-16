import json
import logging
from datetime import date
from typing import Any

import boto3
from boto3.dynamodb.conditions import Key

from cache_service import get_cached_json, set_cached_json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource("dynamodb")

applications_table = dynamodb.Table("Applications")
tasks_table = dynamodb.Table("Tasks")

TERMINAL_APPLICATION_STATUSES = {
    "Rejected",
    "Accepted",
}


def build_response(status_code: int, body: dict[str, Any]) -> dict[str, Any]:
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "http://localhost:5173",
            "Access-Control-Allow-Headers": "Content-Type,Authorization",
            "Access-Control-Allow-Methods": "GET,OPTIONS",
        },
        "body": json.dumps(body),
    }


def get_user_id(event: dict[str, Any]) -> str | None:
    """
    Prefer the authenticated Cognito user ID.
    Fall back to query parameter temporarily for local development.
    """
    claims = (
        event.get("requestContext", {})
        .get("authorizer", {})
        .get("jwt", {})
        .get("claims", {})
    )

    authenticated_user_id = claims.get("sub")

    if authenticated_user_id:
        return authenticated_user_id

    query_params = event.get("queryStringParameters") or {}
    return query_params.get("userId")


def calculate_metrics(user_id: str) -> dict[str, int]:
    applications_response = applications_table.query(
        KeyConditionExpression=Key("userId").eq(user_id)
    )
    applications = applications_response.get("Items", [])

    tasks = []

    today = date.today().isoformat()

    applications_sent = len(applications)

    dsa_done = sum(
        1
        for task in tasks
        if task.get("category") == "LeetCode"
        and task.get("status") == "Completed"
    )

    follow_ups_due = sum(
        1
        for application in applications
        if application.get("followUpDate")
        and application["followUpDate"] <= today
        and application.get("status") not in TERMINAL_APPLICATION_STATUSES
    )

    return {
        "applicationsSent": applications_sent,
        "dsaDone": dsa_done,
        "followUpsDue": follow_ups_due,
    }


def lambda_handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    try:
        method = (
            event.get("requestContext", {})
            .get("http", {})
            .get("method")
        )

        if method == "OPTIONS":
            return build_response(200, {"message": "CORS preflight successful"})

        if method != "GET":
            return build_response(405, {"error": "Method not allowed"})

        user_id = get_user_id(event)

        if not user_id:
            return build_response(400, {"error": "Unable to determine userId"})

        cache_key = f"dashboard:metrics:{user_id}"

        cached_metrics = get_cached_json(cache_key)

        if cached_metrics is not None:
            return build_response(200, {
                "source": "cache",
                "metrics": cached_metrics,
            })

        metrics = calculate_metrics(user_id)

        set_cached_json(
            key=cache_key,
            value=metrics,
            ttl_seconds=300,
        )

        return build_response(200, {
            "source": "database",
            "metrics": metrics,
        })

    except Exception:
        logger.exception("Failed to retrieve dashboard metrics")

        return build_response(500, {
            "error": "Internal server error",
            "message": "Unable to load dashboard metrics",
        })