# JobTrackr AI SES Email Notification Design

## Goal

Use Amazon SES to send email notifications for job search follow-ups.

Example use cases:

- Follow-up reminder after applying to a job
- Interview reminder
- Recruiter follow-up reminder
- Daily preparation summary

---

# Notification Flow

```text
User creates application
        ↓
Application has followUpDate
        ↓
Backend checks due follow-ups
        ↓
Lambda triggers SES
        ↓
Email reminder is sent to user