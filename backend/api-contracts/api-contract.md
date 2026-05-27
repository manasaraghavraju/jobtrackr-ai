# JobTrackr AI Backend API Contract

## Base URL

Local/Development:
http://localhost:5000

Production:
https://api.jobtrackr-ai.com

---

# 1. Users API

## Create User

POST /users

### Request Body

```json
{
  "name": "Manasa",
  "email": "manasa@email.com"
}
```

### Response

```json
{
  "message": "User created successfully",
  "userId": "user_123"
}
```

### DynamoDB Fields

- userId
- name
- email
- createdAt

---

# 2. Tasks API

## Create Task

POST /tasks

### Request Body

```json
{
  "userId": "user_123",
  "title": "Solve Two Sum",
  "category": "LeetCode",
  "status": "Pending",
  "dueDate": "2026-05-25"
}
```

### Response

```json
{
  "message": "Task created successfully",
  "taskId": "task_123"
}
```

## Get Tasks

GET /tasks/{userId}

### Response

```json
[
  {
    "taskId": "task_123",
    "title": "Solve Two Sum",
    "category": "LeetCode",
    "status": "Pending",
    "dueDate": "2026-05-25"
  }
]
```

### DynamoDB Fields

- taskId
- userId
- title
- category
- status
- dueDate
- createdAt

---

# 3. Applications API

## Create Application

POST /applications

### Request Body

```json
{
  "userId": "user_123",
  "company": "Amazon",
  "role": "Software Development Engineer",
  "status": "Applied",
  "appliedDate": "2026-05-20",
  "jobLink": "https://example.com/job",
  "notes": "Applied through company website"
}
```

### Response

```json
{
  "message": "Application added successfully",
  "applicationId": "app_123"
}
```

## Get Applications

GET /applications/{userId}

### Response

```json
[
  {
    "applicationId": "app_123",
    "company": "Amazon",
    "role": "Software Development Engineer",
    "status": "Applied",
    "appliedDate": "2026-05-20"
  }
]
```

### DynamoDB Fields

- applicationId
- userId
- company
- role
- status
- appliedDate
- jobLink
- notes
- createdAt

---

# 4. Contacts API

## Create Contact

POST /contacts

### Request Body

```json
{
  "userId": "user_123",
  "name": "John Smith",
  "company": "Google",
  "email": "john@email.com",
  "linkedinUrl": "https://linkedin.com/in/example",
  "lastContacted": "2026-05-20",
  "notes": "Recruiter for backend roles"
}
```

### Response

```json
{
  "message": "Contact added successfully",
  "contactId": "contact_123"
}
```

## Get Contacts

GET /contacts/{userId}

### Response

```json
[
  {
    "contactId": "contact_123",
    "name": "John Smith",
    "company": "Google",
    "email": "john@email.com",
    "lastContacted": "2026-05-20"
  }
]
```

### DynamoDB Fields

- contactId
- userId
- name
- company
- email
- linkedinUrl
- lastContacted
- notes
- createdAt

---

# 5. Notes API

## Create Note

POST /notes

### Request Body

```json
{
  "userId": "user_123",
  "title": "AWS Lambda Deep Dive",
  "content": "Lambda receives API Gateway events and writes to DynamoDB.",
  "category": "Interview Prep"
}
```

### Response

```json
{
  "message": "Note created successfully",
  "noteId": "note_123"
}
```

## Get Notes

GET /notes/{userId}

### Response

```json
[
  {
    "noteId": "note_123",
    "title": "AWS Lambda Deep Dive",
    "category": "Interview Prep",
    "createdAt": "2026-05-20T10:30:00"
  }
]
```

### DynamoDB Fields

- noteId
- userId
- title
- content
- category
- createdAt