# JobTrackr AI

JobTrackr AI is a full-stack job search management application that helps users track job applications, coding preparation, recruiter contacts, follow-up activities, and overall job-search progress.

The project uses a React frontend and a serverless AWS backend built with Python, API Gateway, Lambda, DynamoDB, Cognito, and CloudWatch.

---

## Features

- Track job applications and application statuses
- Add application details through a React form
- View dashboard metrics
- Track LeetCode and interview-preparation activities
- Manage recruiter and professional contacts
- Protect backend routes with Cognito JWT authentication
- Validate API requests and return structured errors
- Generate mock follow-up email notifications
- Record backend logs in Amazon CloudWatch
- Test Lambda functions locally using pytest
- Test deployed APIs using Postman

---

## Technology Stack

### Frontend

- React
- Vite
- JavaScript
- React Router
- HTML
- CSS
- Fetch API

### Backend

- Python
- AWS Lambda
- Amazon API Gateway
- Amazon DynamoDB
- Amazon Cognito
- Amazon CloudWatch
- Amazon SES notification design

### Testing and Development Tools

- pytest
- unittest.mock
- Postman
- Git
- GitHub
- Visual Studio Code

---

## Architecture

```text
User
  ↓
React + Vite Frontend
  ↓
Amazon Cognito
  ↓
JWT Access Token
  ↓
Amazon API Gateway
  ↓
JWT Authorizer
  ↓
Python AWS Lambda
  ↓
Amazon DynamoDB
```

Supporting services:

```text
Lambda → CloudWatch Logs
Lambda → Mock Email Notification
Postman → API Testing
GitHub → Source Control and Documentation
```

A detailed architecture explanation is available in:

```text
docs/architecture-walkthrough.md
```

---

## Application Pages

### Dashboard

Displays job-search and preparation metrics, including:

- Applications sent
- DSA problems completed
- Follow-ups due

### Applications

Allows users to:

- Add job applications
- Select an application status
- Store company and role information
- Record application dates
- Save job links and notes
- View loading, success, and error messages

### LeetCode

Provides a dedicated page for tracking coding-practice progress.

### Contacts

Provides a dedicated page for organizing recruiters, referrals, alumni, and other professional contacts.

---

## Backend API

### Base URL

```text
https://y6gq02ijl6.execute-api.us-east-1.amazonaws.com
```

> The deployed API URL may change if the API Gateway configuration is recreated.

---

## Public Endpoints

### Hello Endpoint

```http
GET /hello
```

Purpose:

Tests the API Gateway-to-Lambda connection.

Example response:

```json
{
  "message": "Hello from JobTrackr AI backend!",
  "status": "success"
}
```

### Mock Notification Endpoint

```http
POST /notifications/test
```

Example request:

```json
{
  "email": "user@example.com",
  "company": "Amazon",
  "role": "Software Development Engineer",
  "followUpDate": "2026-05-27"
}
```

Example response:

```json
{
  "message": "Mock notification generated successfully",
  "emailPreview": {
    "to": "user@example.com",
    "subject": "Follow-up Reminder: Amazon Software Development Engineer Application"
  }
}
```

---

## Protected Application Endpoints

The following endpoints require a valid Cognito JWT access token.

### Create Application

```http
POST /applications
```

Example request:

```json
{
  "userId": "user_123",
  "company": "Amazon",
  "role": "Software Development Engineer",
  "status": "Applied",
  "appliedDate": "2026-05-20",
  "jobLink": "https://amazon.jobs/example",
  "notes": "Applied through the company careers page"
}
```

Successful response:

```json
{
  "message": "Application created successfully",
  "application": {
    "userId": "user_123",
    "applicationId": "generated-uuid",
    "company": "Amazon",
    "role": "Software Development Engineer",
    "status": "Applied"
  }
}
```

### Get Applications

```http
GET /applications?userId=user_123
```

Successful response:

```json
{
  "applications": [
    {
      "userId": "user_123",
      "applicationId": "generated-uuid",
      "company": "Amazon",
      "role": "Software Development Engineer",
      "status": "Applied"
    }
  ]
}
```

### Update Application

```http
PATCH /applications
```

Example request:

```json
{
  "userId": "user_123",
  "applicationId": "generated-uuid",
  "status": "Interview",
  "notes": "Recruiter scheduled the first interview"
}
```

Successful response:

```json
{
  "message": "Application updated successfully",
  "application": {
    "userId": "user_123",
    "applicationId": "generated-uuid",
    "status": "Interview"
  }
}
```

---

## Authentication

Amazon Cognito handles user authentication.

After login:

1. Cognito issues a JWT access token.
2. The client sends the token in the `Authorization` header.
3. API Gateway validates the JWT.
4. Valid requests are forwarded to Lambda.
5. Invalid or missing tokens receive `401 Unauthorized`.

Header format:

```http
Authorization: Bearer <ACCESS_TOKEN>
```

Protected routes:

```text
POST /applications
GET /applications
PATCH /applications
```

---

## Application Status Values

The backend accepts the following application statuses:

```text
Saved
Applied
Online Assessment
Interview
Rejected
Offer
Accepted
```

Any unsupported status results in a `400 Bad Request` response.

---

## DynamoDB Design

### Applications Table

```text
Table name: Applications
Partition key: userId
Sort key: applicationId
```

Example record:

```json
{
  "userId": "user_123",
  "applicationId": "generated-uuid",
  "company": "Amazon",
  "role": "Software Development Engineer",
  "status": "Applied",
  "appliedDate": "2026-05-20",
  "jobLink": "https://amazon.jobs/example",
  "notes": "Applied through the careers page",
  "createdAt": "2026-06-12T03:57:11.359281",
  "updatedAt": "2026-06-12T03:57:11.359281"
}
```

This key design allows the backend to efficiently retrieve all applications belonging to one user.

---

## Validation and Error Handling

The Applications API validates required fields:

```text
userId
company
role
status
```

Common API responses:

| Status code | Meaning |
|---|---|
| `200` | Request completed successfully |
| `201` | Resource created successfully |
| `400` | Invalid request or missing fields |
| `401` | Missing, invalid, or expired JWT |
| `404` | Application not found |
| `405` | HTTP method not supported |
| `500` | Unexpected server error |

Detailed server errors are logged in CloudWatch. Clients receive safe, structured error messages without internal stack traces.

---

## Logging and Monitoring

The Python Lambda functions use structured logging.

Logged information includes:

- HTTP method
- Request path
- Query parameters
- User ID
- Application ID
- DynamoDB operations
- Response status
- Unexpected exceptions

Logs can be viewed at:

```text
CloudWatch
→ Log groups
→ /aws/lambda/jobtrackr-applications
```

---

## Testing

Backend unit tests are written using:

```text
pytest
unittest.mock
```

DynamoDB operations are mocked so local tests do not call real AWS resources.

Covered cases include:

- Successful application creation
- Missing required fields
- Invalid application status
- Successful application retrieval
- Missing user ID
- Unsupported HTTP methods

Run tests on Windows CMD:

```cmd
set AWS_DEFAULT_REGION=us-east-1
pytest backend/tests
```

---

## Running the Frontend Locally

### Prerequisites

Install:

- Node.js
- npm
- Git

### Install dependencies

```cmd
cd frontend
npm install
```

### Configure environment variables

Create:

```text
frontend/.env
```

Add:

```env
VITE_API_BASE_URL=https://y6gq02ijl6.execute-api.us-east-1.amazonaws.com
VITE_ACCESS_TOKEN=YOUR_COGNITO_ACCESS_TOKEN
```

Do not commit real access tokens to GitHub.

### Start the development server

```cmd
npm run dev
```

Open:

```text
http://localhost:5173
```

---

## Production Build

Create a production frontend build:

```cmd
cd frontend
npm run build
```

The generated files will be available in:

```text
frontend/dist
```

---

## Project Structure

```text
jobtrackr-ai
├── backend
│   ├── api-contracts
│   │   ├── api-contract.md
│   │   ├── application-api-edge-cases.md
│   │   ├── auth-design.md
│   │   ├── dynamodb-design.md
│   │   └── ses-notification-design.md
│   ├── lambda-functions
│   │   ├── applications.py
│   │   ├── hello.py
│   │   └── mock_notification.py
│   └── tests
│       └── test_applications.py
├── docs
│   ├── architecture.md
│   ├── architecture-walkthrough.md
│   ├── deployment-guide.md
│   └── user-stories.md
├── frontend
│   ├── public
│   ├── src
│   │   ├── components
│   │   ├── pages
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── .gitignore
└── README.md
```

---

## Future Improvements

- Integrate Cognito login directly into the React frontend
- Store tokens securely instead of manually adding them to `.env`
- Read the authenticated user ID from JWT claims
- Prevent users from accessing another user's applications
- Implement delete-application functionality
- Display real application records in the React interface
- Replace hardcoded dashboard metrics with live backend data
- Complete LeetCode task-management APIs
- Complete contacts and networking APIs
- Add filtering and sorting by application status and date
- Add pagination for application results
- Add follow-up dates and automated reminders
- Replace mock notifications with real Amazon SES emails
- Add EventBridge scheduling for due follow-ups
- Add continuous integration using GitHub Actions
- Deploy the React frontend using AWS Amplify or S3 and CloudFront
- Add integration and end-to-end tests
- Add role-based authorization
- Restrict IAM permissions using least-privilege policies
- Manage AWS infrastructure using AWS CDK or Terraform

---

## Key Learning Outcomes

This project demonstrates practical experience with:

- Full-stack application development
- React routing and form handling
- Python REST API development
- Serverless architecture
- JWT authentication
- NoSQL database design
- API validation and error handling
- Cloud logging and monitoring
- Unit testing with mocks
- Frontend-backend integration
- AWS deployment and documentation

---

## Project Status

The current version includes:

- React application shell
- Applications form connected to the backend
- Dashboard metric cards
- Python Lambda application APIs
- DynamoDB persistence
- Cognito JWT authentication
- API Gateway routes
- Structured CloudWatch logging
- Backend unit tests
- Mock email notifications
- Architecture and deployment documentation

The project is actively being improved.