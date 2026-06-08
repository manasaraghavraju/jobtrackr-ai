# JobTrackr AI DynamoDB Table Design

## Goal

Design DynamoDB tables for the main JobTrackr AI backend resources:

- Users
- Applications
- Tasks

The design focuses on simple access patterns needed by the frontend pages.

---

# 1. Users Table

## Table Name

Users

## Primary Key

Partition Key:

```text
userId
```

## Example Item

```json
{
  "userId": "user_123",
  "name": "Manasa",
  "email": "manasa@email.com",
  "createdAt": "2026-05-20T10:30:00Z"
}
```

## Access Patterns

### Create user

Used when a new user signs up.

```text
PUT item by userId
```

### Get user profile

Used when user opens dashboard.

```text
GET item by userId
```

### Update user profile

Used when user edits name/email.

```text
UPDATE item by userId
```

---

# 2. Applications Table

## Table Name

Applications

## Primary Key

Partition Key:

```text
userId
```

Sort Key:

```text
applicationId
```

## Example Item

```json
{
  "userId": "user_123",
  "applicationId": "app_001",
  "company": "Amazon",
  "role": "Software Development Engineer",
  "status": "Applied",
  "appliedDate": "2026-05-20",
  "jobLink": "https://example.com/job",
  "notes": "Applied through company website",
  "createdAt": "2026-05-20T10:30:00Z",
  "updatedAt": "2026-05-20T10:30:00Z"
}
```

## Why this key design?

One user can have many applications.

So:

```text
userId → groups all applications for one user
applicationId → uniquely identifies each application
```

## Access Patterns

### Create application

Used when user adds a job application.

```text
PUT item with userId + applicationId
```

### Get all applications for a user

Used on Applications page.

```text
QUERY by userId
```

### Get one application

Used when user opens application details.

```text
GET item by userId + applicationId
```

### Update application status

Used when status changes from Applied to Interview, Rejected, Offer, etc.

```text
UPDATE item by userId + applicationId
```

### Delete application

Used when user removes an application.

```text
DELETE item by userId + applicationId
```

## Possible Status Values

```text
Saved
Applied
Online Assessment
Interview
Rejected
Offer
Accepted
```

---

# 3. Tasks Table

## Table Name

Tasks

## Primary Key

Partition Key:

```text
userId
```

Sort Key:

```text
taskId
```

## Example Item

```json
{
  "userId": "user_123",
  "taskId": "task_001",
  "title": "Solve Two Sum",
  "category": "LeetCode",
  "status": "Pending",
  "priority": "High",
  "dueDate": "2026-05-25",
  "createdAt": "2026-05-20T10:30:00Z",
  "updatedAt": "2026-05-20T10:30:00Z"
}
```

## Why this key design?

One user can have many tasks.

So:

```text
userId → groups all tasks for one user
taskId → uniquely identifies each task
```

## Access Patterns

### Create task

Used when user creates a new task.

```text
PUT item with userId + taskId
```

### Get all tasks for a user

Used on Dashboard and LeetCode page.

```text
QUERY by userId
```

### Get one task

Used when user opens task details.

```text
GET item by userId + taskId
```

### Update task status

Used when task changes from Pending to Completed.

```text
UPDATE item by userId + taskId
```

### Delete task

Used when user removes a task.

```text
DELETE item by userId + taskId
```

## Possible Categories

```text
LeetCode
Application
Networking
Resume
Interview Prep
Project
```

## Possible Status Values

```text
Pending
In Progress
Completed
Skipped
```

---

# Summary of Tables

| Table | Partition Key | Sort Key | Purpose |
|---|---|---|---|
| Users | userId | None | Store user profile |
| Applications | userId | applicationId | Store job applications |
| Tasks | userId | taskId | Store preparation tasks |

---

# Main Access Patterns

## Dashboard Page

Needs:

```text
Get user profile
Get user's applications
Get user's tasks
```

## Applications Page

Needs:

```text
Create application
Get all applications
Update application
Delete application
```

## LeetCode Page

Needs:

```text
Create task
Get LeetCode tasks
Update task status
```

## Contacts Page

Contacts table will be designed separately later.

---

# Notes

For the first version, we will keep the design simple using three separate DynamoDB tables.

Later, this can be optimized into a single-table design if needed.