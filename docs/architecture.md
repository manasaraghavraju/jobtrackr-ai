# Target Architecture

## System Overview

The application will use a React frontend connected to a serverless AWS backend.

## Architecture Flow

User → React Frontend → API Gateway → AWS Lambda → DynamoDB

Authentication will be handled using AWS Cognito.

## Main Components

### Frontend
- Login and signup pages
- Dashboard page
- Job application tracker
- Recruiter tracker
- Interview tracker
- Analytics dashboard

### Backend
- REST APIs using AWS Lambda
- API Gateway for routing requests
- DynamoDB for storing user data
- Cognito for user authentication

### Database Tables

#### Users
- userId
- name
- email
- createdAt

#### Applications
- applicationId
- userId
- company
- role
- status
- appliedDate
- followUpDate
- notes

#### Recruiters
- recruiterId
- userId
- name
- company
- email
- linkedinUrl
- lastContacted
- notes

#### InterviewPrep
- prepId
- userId
- topic
- problemName
- difficulty
- status
- notes

## Future Enhancements

- Resume upload
- AI-based resume matching
- Email reminder integration
- Calendar integration
- Application analytics