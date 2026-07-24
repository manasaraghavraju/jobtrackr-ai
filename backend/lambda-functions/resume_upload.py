import json
import logging
import os
import re
import uuid
from pathlib import Path
from typing import Any

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3_client = boto3.client("s3")

BUCKET_NAME = os.environ.get("RESUME_BUCKET_NAME", "")
PRESIGNED_URL_EXPIRATION = 300
MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024

ALLOWED_CONTENT_TYPES = {
    "application/pdf": ".pdf",
    "application/msword": ".doc",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
}


def response(status_code: int, body: dict[str, Any]) -> dict[str, Any]:
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "http://localhost:5173",
            "Access-Control-Allow-Headers": "Content-Type,Authorization",
            "Access-Control-Allow-Methods": "POST,OPTIONS",
        },
        "body": json.dumps(body),
    }


def parse_body(event: dict[str, Any]) -> dict[str, Any]:
    body = event.get("body")

    if not body:
        return {}

    if isinstance(body, dict):
        return body

    return json.loads(body)


def sanitize_filename(filename: str) -> str:
    """
    Remove folder paths and replace unsafe filename characters.
    """

    base_name = Path(filename).name
    sanitized = re.sub(r"[^A-Za-z0-9._-]", "_", base_name)

    return sanitized[:150]


def get_authenticated_user_id(event: dict[str, Any]) -> str | None:
    """
    Read the Cognito subject from the API Gateway JWT authorizer.
    """

    claims = (
        event.get("requestContext", {})
        .get("authorizer", {})
        .get("jwt", {})
        .get("claims", {})
    )

    return claims.get("sub")


def lambda_handler(
    event: dict[str, Any],
    context: Any,
) -> dict[str, Any]:
    try:
        method = (
            event.get("requestContext", {})
            .get("http", {})
            .get("method")
        )

        if method == "OPTIONS":
            return response(
                200,
                {"message": "CORS preflight successful"},
            )

        if method != "POST":
            return response(
                405,
                {"error": "Method not allowed"},
            )

        if not BUCKET_NAME:
            logger.error("RESUME_BUCKET_NAME is not configured")

            return response(
                500,
                {"error": "Resume storage is not configured"},
            )

        body = parse_body(event)

        filename = str(body.get("filename", "")).strip()
        content_type = str(body.get("contentType", "")).strip()
        file_size = body.get("fileSize")

        if not filename:
            return response(
                400,
                {"error": "filename is required"},
            )

        if content_type not in ALLOWED_CONTENT_TYPES:
            return response(
                400,
                {
                    "error": (
                        "Unsupported file type. "
                        "Only PDF, DOC, and DOCX are allowed"
                    )
                },
            )

        try:
            file_size = int(file_size)
        except (TypeError, ValueError):
            return response(
                400,
                {"error": "fileSize must be an integer"},
            )

        if file_size < 1:
            return response(
                400,
                {"error": "File cannot be empty"},
            )

        if file_size > MAX_FILE_SIZE_BYTES:
            return response(
                400,
                {"error": "File size must not exceed 5 MB"},
            )

        expected_extension = ALLOWED_CONTENT_TYPES[content_type]
        safe_filename = sanitize_filename(filename)

        if not safe_filename.lower().endswith(expected_extension):
            return response(
                400,
                {
                    "error": (
                        f"Filename must end with "
                        f"{expected_extension}"
                    )
                },
            )

        user_id = get_authenticated_user_id(event)

        # Temporary fallback for your current development setup.
        if not user_id:
            user_id = str(body.get("userId", "")).strip()

        if not user_id:
            return response(
                400,
                {"error": "Unable to determine user identity"},
            )

        file_id = str(uuid.uuid4())

        object_key = (
            f"users/{user_id}/resumes/"
            f"{file_id}-{safe_filename}"
        )

        upload_url = s3_client.generate_presigned_url(
            ClientMethod="put_object",
            Params={
                "Bucket": BUCKET_NAME,
                "Key": object_key,
                "ContentType": content_type,
            },
            ExpiresIn=PRESIGNED_URL_EXPIRATION,
        )

        logger.info({
            "message": "Generated resume upload URL",
            "userId": user_id,
            "objectKey": object_key,
            "contentType": content_type,
            "declaredFileSize": file_size,
        })

        return response(
            200,
            {
                "message": "Upload URL generated successfully",
                "uploadUrl": upload_url,
                "objectKey": object_key,
                "expiresIn": PRESIGNED_URL_EXPIRATION,
                "requiredHeaders": {
                    "Content-Type": content_type
                },
            },
        )

    except json.JSONDecodeError:
        return response(
            400,
            {"error": "Invalid JSON body"},
        )

    except ClientError:
        logger.exception("Unable to generate S3 upload URL")

        return response(
            500,
            {"error": "Unable to prepare resume upload"},
        )

    except Exception:
        logger.exception("Unexpected resume upload error")

        return response(
            500,
            {"error": "Internal server error"},
        )