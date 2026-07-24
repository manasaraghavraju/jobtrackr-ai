# Resume Upload API

## Generate Upload URL

```http
POST /resumes/upload-url
```

Authentication:

```http
Authorization: Bearer <access_token>
```

Request:

```json
{
  "filename": "Manasa_Resume.pdf",
  "contentType": "application/pdf",
  "fileSize": 245760
}
```

Response:

```json
{
  "message": "Upload URL generated successfully",
  "uploadUrl": "temporary S3 URL",
  "objectKey": "users/{userId}/resumes/{uuid}-Manasa_Resume.pdf",
  "expiresIn": 300,
  "requiredHeaders": {
    "Content-Type": "application/pdf"
  }
}
```

## Allowed Files

- PDF
- DOC
- DOCX
- Maximum size: 5 MB

## Upload Flow

```text
Client requests upload URL
        ↓
API Gateway validates JWT
        ↓
Lambda validates metadata
        ↓
Lambda creates presigned S3 PUT URL
        ↓
Client uploads directly to S3
```

## Storage

Bucket access is private.

Object-key format:

```text
users/{authenticatedUserId}/resumes/{uuid}-{sanitizedFilename}
```