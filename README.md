# Multi-Service App

This project consists of a Node.js front-end, Python FastAPI back-end, and Postgres database, all containerized with Docker.

## Development Setup

1. Ensure you have Docker and Docker Compose installed.
2. Clone the repository.
3. Open the project in VS Code.
4. When prompted, reopen the folder in the dev container.
5. The dev container will set up the environment and install dependencies.

## Running the Application

From within the dev container:

```bash
docker-compose up
```

This will start all services:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- Database: localhost:5432

## Project Structure

- `frontend/`: Node.js React app
- `backend/`: Python FastAPI app
- `db/`: Database initialization scripts
- `.devcontainer/`: Dev container configuration
- `docker-compose.yml`: Docker Compose configuration

## Deployment

For deployment to Digital Ocean Droplet, use the docker-compose.yml and build the images.
