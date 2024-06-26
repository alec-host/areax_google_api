# FastAPI and Redis Integration

This project is a Python application built using FastAPI and Redis. It provides an API to interact with Gmail, storing OAuth tokens in Redis for secure access.

## Features

- FastAPI for building robust RESTful APIs.
- Redis for storing OAuth tokens securely.
- Integration with Gmail API to read and reply to emails.

## Project Structure

```bash
my_project/
├── redis_client.py # Handles Redis interactions
├── gmail_auth.py # Manages Gmail API authentication
├── main.py # FastAPI application entry point
├── requirements.txt # Python dependencies
├── docker-compose.yml # Docker Compose file for multi-container setup
├── Dockerfile # Dockerfile for building the application image
├── .env
└── .gitignore # Git ignore file
```

## Prerequisites

- Docker
- Docker Compose
- Python 3.11

## Setup Instructions

1. **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd my_project
    ```

2. **Build and run the application using Docker Compose:**

    ```bash
    docker-compose up --build
    ```

3. **Access the application:**

    The FastAPI application will be accessible at `http://localhost:8000`.

## Endpoints

- **POST `/fetch_emails`**: Fetch emails with specified keywords in the subject and body.

    Example request:

    ```json
    {
        "search_words": "internet subscription",
    }
    ```

## Environment Variables

Make sure to set up the following environment variables as needed:

- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET`
- `REDIS_HOST` (default: `redis`)
- `REDIS_PORT` (default: `6379`)

## Notes

- Ensure your `credentials.json` file for Google API is placed in the root directory of the project.
- The `token.json` file will be managed by the application and stored in Redis.

## License

This project is licensed under the MIT License.
