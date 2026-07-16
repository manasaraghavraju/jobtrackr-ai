# Redis Dashboard Cache Design

## Purpose

Cache dashboard metrics to reduce repeated DynamoDB queries and improve response time.

## Cache Pattern

The application uses the cache-aside pattern.

```text
Request dashboard metrics
        ↓
Check Redis cache
        ↓
Cache hit? ── Yes → Return cached metrics
        │
        No
        ↓
Read DynamoDB
        ↓
Calculate metrics
        ↓
Store result in Redis for 300 seconds
        ↓
Return metrics
```

## Cache Key

```text
dashboard:metrics:{userId}
```

Example:

```text
dashboard:metrics:user_123
```

## Cached Value

```json
{
  "applicationsSent": 5,
  "dsaDone": 12,
  "followUpsDue": 2
}
```

## TTL

```text
300 seconds
```

## Invalidation

The dashboard cache is deleted after:

- Creating an application
- Updating an application
- Creating or completing a DSA task
- Changing a follow-up date

## Failure Behavior

Redis is treated as an optimization, not the source of truth.

If Redis is unavailable:

1. Log the cache error.
2. Continue reading from DynamoDB.
3. Return the API response normally.

## Source of Truth

DynamoDB remains the authoritative data store.

## Production Deployment

The AWS version will use Amazon ElastiCache connected to the Lambda function through a VPC. Redis connection settings will be stored as Lambda environment variables.