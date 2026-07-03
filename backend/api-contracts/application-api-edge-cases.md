# Application API Test Cases and Edge Cases

## Endpoint Tested

POST /applications  
GET /applications

## Test Cases Covered

| Test Case | Expected Result |
|---|---|
| Create application with valid data | 201 Created |
| Missing role field | 400 Bad Request |
| Invalid status value | 400 Bad Request |
| Get applications with valid userId | 200 OK |
| Get applications without userId | 400 Bad Request |
| Unsupported method DELETE | 405 Method Not Allowed |

## Validation Rules

Required fields for creating an application:

- userId
- company
- role
- status

Allowed status values:

- Saved
- Applied
- Online Assessment
- Interview
- Rejected
- Offer
- Accepted

## Error Handling

The Lambda returns clear error responses for:

- Missing required fields
- Invalid status values
- Missing query parameters
- Unsupported HTTP methods
- Unexpected server errors

## Notes

DynamoDB calls are mocked in unit tests to avoid calling real AWS resources during local testing.