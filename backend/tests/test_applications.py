import json
import sys
import os
from unittest.mock import patch

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "lambda-functions"))

import applications


def make_event(method, body=None, query_params=None):
    return {
        "requestContext": {
            "http": {
                "method": method
            }
        },
        "body": json.dumps(body) if body else None,
        "queryStringParameters": query_params
    }


@patch("applications.table.put_item")
def test_create_application_success(mock_put_item):
    event = make_event("POST", {
        "userId": "user_123",
        "company": "Amazon",
        "role": "Software Engineer",
        "status": "Applied"
    })

    response = applications.lambda_handler(event, None)
    body = json.loads(response["body"])

    assert response["statusCode"] == 201
    assert body["message"] == "Application created successfully"
    assert body["application"]["company"] == "Amazon"


def test_create_application_missing_role():
    event = make_event("POST", {
        "userId": "user_123",
        "company": "Amazon",
        "status": "Applied"
    })

    response = applications.lambda_handler(event, None)
    body = json.loads(response["body"])

    assert response["statusCode"] == 400
    assert body["error"] == "role is required"


def test_create_application_invalid_status():
    event = make_event("POST", {
        "userId": "user_123",
        "company": "Amazon",
        "role": "Software Engineer",
        "status": "Random"
    })

    response = applications.lambda_handler(event, None)
    body = json.loads(response["body"])

    assert response["statusCode"] == 400
    assert body["error"] == "Invalid status value"


@patch("applications.table.query")
def test_get_applications_success(mock_query):
    mock_query.return_value = {
        "Items": [
            {
                "userId": "user_123",
                "applicationId": "app_123",
                "company": "Amazon",
                "role": "Software Engineer",
                "status": "Applied"
            }
        ]
    }

    event = make_event("GET", query_params={"userId": "user_123"})

    response = applications.lambda_handler(event, None)
    body = json.loads(response["body"])

    assert response["statusCode"] == 200
    assert len(body["applications"]) == 1
    assert body["applications"][0]["company"] == "Amazon"


def test_get_applications_missing_user_id():
    event = make_event("GET", query_params={})

    response = applications.lambda_handler(event, None)
    body = json.loads(response["body"])

    assert response["statusCode"] == 400
    assert body["error"] == "userId query parameter is required"


def test_method_not_allowed():
    event = make_event("DELETE")

    response = applications.lambda_handler(event, None)
    body = json.loads(response["body"])

    assert response["statusCode"] == 405
    assert body["error"] == "Method not allowed"