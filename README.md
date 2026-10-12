# HYD-PS2

AI-powered lead generation and outreach platform with human-in-the-loop workflows, LLM-assisted decisioning, and voice-enabled communication tools.

This project is built with FastAPI and Python, and includes PostgreSQL, MongoDB, Redis, message/lead workflow orchestration, agent-based automation, and optional integrations for email, SMS, and voice.

## Overview

HYD-PS2 is designed to help teams:

- onboard and manage client or operator workflows
- discover and score leads
- orchestrate outreach campaigns
- manage communication channels such as email and SMS
- run AI-driven decisioning and campaign operations
- monitor system health and readiness in production-like environments

The application exposes a REST API under `/api/v1` and includes health checks at:

- `/health`
- `/ready`
- `/api/v1/system/status`

## Architecture

The application is structured around a FastAPI backend with several service domains:

- `app/api` – API routes for auth, onboarding, leads, campaigns, communications, scheduling, insights, and more
- `app/core` – configuration, DB setup, and shared infrastructure
- `app/models` – SQLAlchemy models and domain entities
- `app/schemas` – request/response validation models
- `app/services` – business logic and provider integrations
- `app/agents` – agent logic for automated processing
- `app/worker.py` – background / long-running task worker logic

## Stack

- Python 3.11
- FastAPI
- Uvicorn
- SQLAlchemy + AsyncPG + Alembic
- PostgreSQL
- MongoDB + Motor
- Redis
- Pydantic + Pydantic Settings
- LangGraph + Postgres checkpointing
- Optional external providers for LLMs, email, SMS, and voice

## Features

- Authentication and authorization
- Lead management APIs
- Campaign orchestration
- Communication pipelines for email/SMS
- Scheduling and workflow automation
- AI provider abstraction for LLMs
- Voice integration support via ElevenLabs
- Health and dependency readiness checks
- Demo-mode configuration for isolated testing
- Background worker execution for asynchronous jobs

## Repository Structure

```text
.
├── app/
│   ├── agents/
│   ├── api/
│   ├── core/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── main.py
│   └── worker.py
├── migrations/
├── scripts/
├── tests/
├── .dockerignore
├── .gitignore
├── alembic.ini
├── Dockerfile
├── requirements.txt
├── requirements-dev.txt
├── README.md
└── ...
```

## Prerequisites

Before running the app locally, make sure you have:

- Python 3.11+
- PostgreSQL running locally or in Docker
- MongoDB running locally or in Docker
- Redis running locally or in Docker
- Optional API keys for your selected LLM/email/SMS/voice providers

## Local Development Setup

1. Clone the repository:

```bash
git clone https://github.com/TusharSingh14x/hyd-02.git
cd hyd-02
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

If you are developing and want dev dependencies:

```bash
pip install -r requirements-dev.txt
```

4. Configure environment variables.

Create a `.env` file in the project root. Example:

```env
APP_NAME=hyd-ps2
APP_ENV=development
DEBUG=true
JWT_SECRET=change_me
DATABASE_URL=postgresql+asyncpg://hydps2:CHANGE_ME@localhost:5432/hydps2
MONGO_URL=mongodb://localhost:27017
MONGO_DB=hydps2_memory
REDIS_URL=redis://localhost:6379/0

# Optional LLM config
LLM_PROVIDER=auto
OPENROUTER_API_KEY=your_key_here
GROQ_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here

# Optional voice/email/sms configs
ELEVENLABS_API_KEY=
ELEVENLABS_AGENT_ID=
ELEVENLABS_OPERATOR_AGENT_ID=

EMAIL_ENABLED=false
EMAIL_PROVIDER=smtp
SMTP_HOST=mailhog
SMTP_PORT=1025
```

5. Run database migrations if needed:

```bash
alembic upgrade head
```

6. Start the API server:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at:

- http://localhost:8000
- health check: http://localhost:8000/health
- readiness: http://localhost:8000/ready

## Docker

A Docker image is included in the repository.

Build the image:

```bash
docker build -t hyd-ps2 .
```

Run the container:

```bash
docker run -p 8000:8000 --env-file .env hyd-ps2
```

The container starts the app with:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Health and Monitoring

The application exposes system health endpoints for operational checks:

- `GET /health` – basic application status
- `GET /ready` – dependency readiness check for DB and memory services
- `GET /api/v1/system/status` – richer status including worker, LLM config, voice config, and email/SMS readiness

## Testing

The repository includes automated tests under `tests/`.

Run the suite with:

```bash
pytest
```

## Notes

- The project is configured for flexible environment-based deployments.
- Several integrations are optional and only become active if corresponding environment variables and services are configured.
- Demo mode is available and requires isolated demo databases and mail-only configuration.

## License

This project does not currently declare a license in the repository root. Please check with the repository owner before using it in a commercial or production setting.

## Contributing

Pull requests and improvements are welcome. For major changes, please open an issue first to discuss the planned update.

## Contact

Repository: https://github.com/TusharSingh14x/hyd-02

