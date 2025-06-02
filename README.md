# Athena Web Quiz – DevOps Project

This project is a fully functional Flask web application for creating and taking quizzes, with a strong emphasis on demonstrating modern DevOps practices. Inspired by Athena's theme of wisdom and knowledge, the project features containerization with Docker, orchestration with Docker Compose, and automated CI/CD pipelines using GitHub Actions for testing, building Docker images, publishing to Docker Hub, and creating GitHub Releases.

## Application Features

-   **Quiz Creation:** Users can create new quizzes with multiple questions and answers.
-   **Quiz Taking:** Users can take available quizzes.
-   **View Results:** Ability to view the results of completed quizzes.
-   **Database:** PostgreSQL for storing data related to quizzes, questions, answers, and results.
-   **Sample Data:** Automatic population of the database with sample data on initial startup if it's empty.
-   **Health Check:** `/health` endpoint for checking the application's status.

## DevOps Practices and Technologies

-   **Containerization:**
    -   `Dockerfile` for building the Docker image for the Flask application.
    -   `docker-compose.yml` for orchestrating the entire stack:
        -   Flask application (`flask_app`)
        -   PostgreSQL database (`db`)
        -   NGINX reverse proxy (`nginx`)
-   **CI/CD with GitHub Actions:**
    -   **Test Workflow (`.github/workflows/ci-test.yml`):**
        -   Triggered on push to `feature/*`, `dev`, and on Pull Requests to `dev` or `main`.
        -   Performs linting (flake8) and runs Pytest tests (using a Docker Compose environment with a test database).
        -   Uses GitHub Secrets for sensitive data (e.g., test database credentials).
    -   **Release Workflow (`.github/workflows/cd-release.yml`):**
        -   Triggered on push of Git tags formatted as `v*.*.*` (e.g., `v1.0.0`).
        -   Logs into Docker Hub (using `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` from GitHub Secrets).
        -   Builds the Docker image of the Flask application.
        -   Tags the image with the specific version (e.g., `1.0.0`) and `latest` (for stable versions).
        -   Publishes the tagged images to Docker Hub (`<your_dockerhub_username>/athena-web-quiz`).
        -   Creates a GitHub Release for stable Major/Minor versions (e.g., `v1.0.0`, `v1.1.0`), with auto-generated release notes. Pre-release tags (e.g., `v1.0.0-alpha`) also create a GitHub Release, marked as "pre-release".
-   **Testing:**
    -   Integration tests with Pytest.
    -   Tests are executed in an isolated Docker environment defined in `docker-compose-test.yml`.
-   **Security:**
    -   NGINX is configured for TLS termination (requires providing an SSL certificate and key).
    -   Use of GitHub Secrets for managing sensitive data in CI/CD.
-   **Configuration:**
    -   Uses an `.env` file for local application configuration.

## Getting Started

### Prerequisites

-   Git
-   Docker
-   Docker Compose (usually comes with Docker Desktop)

### Local Setup and Running (with Docker Compose)

1.  **Clone the repository:**
    ```
    git clone https://github.com/<your_username>/<your_repository_name>.git
    cd <your_repository_name>
    ```

2.  **Configure Environment Variables:**
    *   Copy `example.env` (if you have one) or create a new file named `.env` in the project's root directory.
    *   Fill in the required values. Example content for `.env`:
        ```
        FLASK_APP=app.py
        FLASK_ENV=development # Or production if for "deploy"
        SECRET_KEY=your_very_secret_flask_key # Generate a strong key
        
        # PostgreSQL Settings for docker-compose.yml
        POSTGRES_USER=athena_user
        POSTGRES_PASSWORD=<your password>
        POSTGRES_DB=athena_db
        
        # Full DATABASE_URL to be used by the Flask application INSIDE the Docker network
        DATABASE_URL=postgresql://athena_user:<your password>@db:5432/athena_db 
        ```
    *   **Note:** `db` in `DATABASE_URL` is the name of the PostgreSQL service defined in `docker-compose.yml`.

3.  **Start the application with Docker Compose:**
    ```
    docker-compose up --build -d
    ```
    *   `--build` will build the Docker images on the first run or if there are changes to the `Dockerfile`.
    *   `-d` will start the containers in detached mode (background).

4.  **Access the application:**
    *   Open a web browser and go to `http://localhost` (or `http://localhost:80` if NGINX is on port 80).
    *   If using HTTPS, it will be `https://localhost` (and you might need to accept a self-signed certificate if you haven't configured a valid one).

5.  **Stop the application:**
    ```
    docker-compose down
    ```

### Running Tests Locally (with Docker Compose)

1.  **Configure `.env.test` file (if needed):**
    *   If your tests require a different configuration (e.g., a separate test database), create an `.env.test` file, similar to `.env`, but with values for the test environment.
    *   In `docker-compose-test.yml`, the `flask_app` and `db` services should be configured to use this `env_file`.

2.  **Run the tests:**
    ```
    docker-compose -f docker-compose-test.yml --env-file .env.test up --build --abort-on-container-exit --exit-code-from flask_app
    ```
    *   `flask_app` here is the name of the service in `docker-compose-test.yml` that executes `pytest`.

## CI/CD Pipeline

-   **CI (Testing):** On every push to `feature/*`, `dev`, or PR to `dev`/`main`, the workflow in `.github/workflows/ci-test.yml` automatically:
    1.  Runs `flake8` for linting.
    2.  Executes `pytest` tests in a Docker Compose environment to ensure code quality.
-   **CD (Release and Publish):** On push of a Git tag formatted as `v*.*.*` (e.g., `v1.0.0`, `v1.1.0-alpha.0`), the workflow in `.github/workflows/cd-release.yml` automatically:
    1.  Builds the Docker image for the Flask application.
    2.  Tags the image with the specific version (e.g., `1.0.0`) and `latest` (only for stable, non-prerelease versions).
    3.  Publishes the image to Docker Hub: `docker pull <your_dockerhub_username>/athena-web-quiz:tag`.
    4.  Creates a GitHub Release associated with the Git tag, with auto-generated notes for changes. Pre-release tags are marked as "pre-release". GitHub Releases are created for Major/Minor stable versions and all pre-release versions.

### Creating a New Release (to trigger CD)

1.  Ensure your local `main` (or other release branch) is up-to-date:
    ```
    git checkout main
    git pull origin main
    ```
2.  (If needed) Update the `VERSION` file or other version metadata and commit the changes.
3.  Create a new Git tag:
    ```
    git tag -a vX.Y.Z -m "Release version X.Y.Z - description of changes"
    # Example: git tag -a v1.3.0 -m "Release v1.3.0: Added user profiles and quiz history"
    # For pre-release: git tag -a v1.4.0-beta.0 -m "Beta for upcoming v1.4.0 features"
    ```
4.  Push the tag to GitHub:
    ```
    git push origin vX.Y.Z
    ```
    This will trigger the CD workflow.

## Project Structure

-   `app/`: Contains the Flask application (Python code, templates, static files).
-   `nginx/`: Configuration files for NGINX (including for TLS).
-   `tests/`: Pytest tests.
-   `.github/workflows/`: GitHub Actions workflow files (`ci-test.yml`, `cd-release.yml`).
-   `Dockerfile`: Instructions for building the Docker image for the Flask application.
-   `docker-compose.yml`: Defines the services (app, db, nginx) for the main Docker Compose environment.
-   `docker-compose-test.yml`: Defines the services for the test Docker Compose environment.
-   `.env` (created manually): Local environment variables.
-   `example.env` (optional): Template for the `.env` file.
-   `requirements.txt` (in `app/`): Python dependencies.




---
