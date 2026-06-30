# JobTrackr AI Deployment Guide

## Deployment Overview

JobTrackr AI uses a cloud-based serverless backend and a React frontend.

## Architecture

```text
React Frontend
        ↓
API Gateway
        ↓
AWS Lambda
        ↓
DynamoDB

Authentication:
Cognito JWT Authorizer

Mock Notifications:
Lambda mock notification function
```

---

# Backend Deployment

## AWS Region

```text
us-east-1
```

## Backend Services Used

- AWS Lambda
- API Gateway HTTP API
- Amazon DynamoDB
- Amazon Cognito
- Amazon SES mock notification design

---

# Lambda Functions

## 1. Hello Lambda

Function name:

```text
jobtrackr-hello
```

Purpose:

```text
Test basic API Gateway to Lambda connection.
```

Endpoint:

```text
GET /hello
```

---

## 2. Applications Lambda

Function name:

```text
jobtrackr-applications
```

Purpose:

```text
Create, read, and update job applications.
```

Endpoints:

```text
POST /applications
GET /applications
PATCH /applications
```

---

## 3. Mock Notification Lambda

Function name:

```text
jobtrackr-mock-notification
```

Purpose:

```text
Generate mock email notification preview.
```

Endpoint:

```text
POST /notifications/test
```

---

# API Gateway Deployment

API name:

```text
jobtrackr-api
```

Stage:

```text
$default
```

Deployment type:

```text
Auto-deploy enabled
```

Invoke URL:

```text
https://y6gq02ijl6.execute-api.us-east-1.amazonaws.com
```

---

# Protected Routes

The following routes are protected using Cognito JWT authorization:

```text
POST /applications
GET /applications
PATCH /applications
```

Public routes:

```text
GET /hello
POST /notifications/test
```

---

# DynamoDB Deployment

Table name:

```text
Applications
```

Primary key:

```text
userId
```

Sort key:

```text
applicationId
```

Purpose:

```text
Stores job application records for each user.
```

---

# Cognito Deployment

Cognito User Pool is used for authentication.

Token flow:

```text
User logs in
        ↓
Cognito returns JWT token
        ↓
Frontend/Postman sends token in Authorization header
        ↓
API Gateway validates token
        ↓
Lambda is invoked
```

Authorization header format:

```text
Authorization: Bearer <access_token>
```

---

# Frontend Local Deployment

## Install dependencies

```cmd
cd frontend
npm install
```

## Environment variables

Create:

```text
frontend/.env
```

Add:

```env
VITE_API_BASE_URL=https://y6gq02ijl6.execute-api.us-east-1.amazonaws.com
VITE_ACCESS_TOKEN=PASTE_ACCESS_TOKEN_HERE
```

## Run frontend locally

```cmd
npm run dev
```

Frontend URL:

```text
http://localhost:5173
```

---

# Frontend Production Build

To create production build:

```cmd
cd frontend
npm run build
```

Build output folder:

```text
frontend/dist
```

---

# Testing

## Test Hello Endpoint

```text
GET /hello
```

Expected:

```json
{
  "message": "Hello from JobTrackr AI backend!",
  "status": "success"
}
```

## Test Applications Endpoint

```text
GET /applications?userId=user_123
```

Requires:

```text
Authorization: Bearer <access_token>
```

Expected:

```json
{
  "applications": []
}
```

## Test Mock Notification

```text
POST /notifications/test
```

Expected:

```json
{
  "message": "Mock notification generated successfully"
}
```

---

# Screenshots To Add

Add screenshots for:

1. API Gateway routes
2. Lambda functions list
3. DynamoDB Applications table
4. Cognito User Pool
5. Postman successful GET /applications
6. React Applications form success message
7. Dashboard metrics page

---

# Deployment Status

| Component | Status |
|---|---|
| React frontend | Running locally |
| API Gateway | Deployed |
| Lambda functions | Deployed |
| DynamoDB | Deployed |
| Cognito Auth | Implemented |
| SES notification | Mock implemented |