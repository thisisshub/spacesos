# Generative AI Task Manager (Reward: $X)

## Goal
Create a task prioritization system that generates and rotates tasks based on client data.

## Requirements
- Analyze user interactions to:
  - Generate daily priority tasks
  - Schedule client reminders (e.g., birthdays, follow-ups)
  - Suggest queries financial advisors might find useful
- Auto-update tasks in real time.

## APIs & Tools
- OpenAI API
- Supabase
- Google Cloud Functions

## Prerequisites
- Experience with task scheduling algorithms

#
- Has structlog as middleware so you get prettified logs for debugging in console or file
`2025-02-14T07:02:26.119911Z [info     ] request_started                [django_structlog.middlewares.request] ip=127.0.0.1 request='POST /api/token/' request_id=217869e5-fe7c-4956-8c46-ba3bba8f515b user_agent=curl/8.7.1 user_id=None`

- Creates a superuser whenever a new db instance is started from scratch from env variables

- Has jwt authentication for users along with predefined permissions as per devised django auth groups

- Uses marvin ai to generate summaries