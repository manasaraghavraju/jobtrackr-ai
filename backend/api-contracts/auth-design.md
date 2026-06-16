# JobTrackr AI Authentication Design

## Authentication Provider

Amazon Cognito User Pool

## Token Type

JWT access token

## Authentication Flow

1. User signs up or logs in through Cognito.
2. Cognito returns a JWT token.
3. Frontend sends API requests with the token in the Authorization header.
4. API Gateway validates the token using a JWT authorizer.
5. If token is valid, request is forwarded to Lambda.
6. If token is missing or invalid, API Gateway returns 401 Unauthorized.

## Authorization Header Format

Authorization: Bearer <JWT_TOKEN>

## Public Routes

| Method | Route | Auth Required |
|---|---|---|
| GET | /hello | No |

## Protected Routes

| Method | Route | Auth Required |
|---|---|---|
| POST | /applications | Yes |
| GET | /applications | Yes |
| PATCH | /applications | Yes |

## Notes

For the first version, API Gateway handles JWT validation.
Lambda assumes the request is already authenticated.
Later, Lambda can read user claims from the token and use the authenticated user's userId instead of trusting userId from the request body.