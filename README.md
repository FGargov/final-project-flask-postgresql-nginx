# Athena Web Quiz – DevOps Project

This project is a fully functional Flask web application for creating and taking quizzes, with a strong emphasis on demonstrating modern DevOps practices. Inspired by Athena's theme of wisdom and knowledge, the project features containerization with Docker, orchestration with Docker Compose, automated deployment with Ansible, and CI/CD pipelines using GitHub Actions.

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
    -   `docker-compose.yml` for orchestrating the entire stack (Flask, PostgreSQL, NGINX), including health checks for reliable startup order.
-   **Infrastructure as Code (IaC) with Ansible:**
    -   Fully automated deployment playbook that handles everything from dependency installation to application startup.
    -   **Role-based structure** for clean separation of concerns:
        -   `common`: Installs base dependencies like `git`.
        -   `docker`: Ensures Docker and Docker Compose are installed and running.
        -   `deploy`: Clones the project, generates secure configurations from templates, and starts the application stack.
    -   **Security:** Uses **Ansible Vault** to encrypt all sensitive data (API keys, database credentials), ensuring no secrets are ever exposed in the repository.
-   **CI/CD with GitHub Actions:**
    -   Automated workflows for testing, building, and releasing the application.
-   **Testing:**
    -   Integration tests with Pytest, executed in an isolated Docker environment defined in `docker-compose-test.yml`.
-   **Security:**
    -   NGINX configured for TLS termination (requires providing an SSL certificate and key).
    -   Use of GitHub Secrets for managing sensitive data in CI/CD pipelines.

## Getting Started

### Prerequisites

-   Git
-   Docker
-   Docker Compose (usually included with Docker)
-   Ansible

### Local Setup and Running (with Ansible)

This project uses Ansible to automate the entire setup process, ensuring a consistent and reliable deployment every time.

**1. Clone the repository:**
```
git clone https://github.com/<your_username>/<your_repository_name>.git
cd <your_repository_name>
```

**2. Configure Ansible Secrets:**
The entire application configuration is managed securely through Ansible Vault. You will create your own encrypted secrets file.

*   Navigate to the Ansible directory:
    ```
    cd ansible
    ```
*   Create a new file named `secrets.yml`. **Do not** name it `.env`.
*   Fill the file with the necessary secrets. The `DATABASE_URL` is generated automatically by Ansible and should **not** be included here.
    ```
    # ansible/secrets.yml
    FLASK_APP: "app.py"
    FLASK_ENV: "development"
    
    # Generate a NEW, RANDOM key for production
    SECRET_KEY: "your-very-secret-flask-key" 
    
    # PostgreSQL Settings
    POSTGRES_USER: "postgres"
    POSTGRES_PASSWORD: "a-strong-password-here"
    POSTGRES_DB: "athenadb"
    ```
*   Encrypt your new `secrets.yml` file using Ansible Vault. You will be prompted to create a new password for the vault. **Remember this password!**
    ```
    ansible-vault encrypt secrets.yml
    ```

**3. Run the Ansible Playbook:**
This single command will set up and start the entire application stack.
```
ansible-playbook -i inventory playbook.yml --ask-vault-pass -K
```
*   Ansible will prompt you for two passwords:
    1.  `BECOME password:` This is your computer's **sudo (administrator) password**.
    2.  `Vault password:` This is the password you created in the previous step for `secrets.yml`.

**4. Access the application:**
*   Open a web browser and go to `http://localhost`.
*   If using HTTPS, go to `https://localhost`.

**5. Stop the application:**
To stop and remove all containers managed by the Ansible deployment, run the following command. It targets the project directory created by the `root` user.
```
sudo docker-compose -f /root/final-project/docker-compose.yml down
```
*   The `-f` (`--file`) flag is crucial because it points to the correct `docker-compose.yml` file.

### Running Tests Locally (with Docker Compose)

1.  **Configure `.env.test` file (if needed):**
    *   If your tests require a different configuration (e.g., a separate test database), create an `.env.test` file.
    *   In `docker-compose-test.yml`, the `flask_app` and `db` services should be configured to use this `env_file`.

2.  **Run the tests:**
    ```
    docker-compose -f docker-compose-test.yml --env-file .env.test up --build --abort-on-container-exit --exit-code-from flask_app
    ```
    *   `flask_app` here is the name of the service in `docker-compose-test.yml` that executes `pytest`.

### CI/CD Pipeline

#### CI (Testing)
On every `push` event to `feature/*`, `dev`, or on `Pull Request` creation to `dev`/`main`, the workflow in `.github/workflows/ci-test.yml` automatically:
*   Executes `flake8` for code style checks (linting).
*   Runs `pytest` tests in an isolated Docker Compose environment to ensure code quality.

#### CD (Release and Publish)
On `push` of a Git tag formatted as `v*.*.*` (e.g., `v1.0.0`, `v1.1.0-alpha.0`), the workflow in `.github/workflows/cd-release.yml` automatically:
*   Builds the Docker image for the Flask application.
*   Tags the image with the specific version (e.g., `1.0.0`) and with `latest` (only for stable, non-prerelease versions).
*   Publishes the image to Docker Hub. It can then be pulled using: `docker pull <your_dockerhub_username>/athena-web-quiz:tag`.
*   Creates a GitHub Release, associated with the Git tag, with auto-generated release notes. Pre-release tags are marked as "pre-release".

#### Creating a New Release (to trigger CD)
1.  Ensure your `main` branch (or other release branch) is up-to-date:
    ```
    git checkout main
    git pull origin main
    ```
2.  Create a new Git tag with a descriptive message:
    ```
    git tag -a vX.Y.Z -m "Release version X.Y.Z - description of changes"
    # Example (stable release): git tag -a v1.3.0 -m "Release v1.3.0: Added user profiles"
    # Example (pre-release):   git tag -a v1.4.0-beta.0 -m "Beta for upcoming v1.4.0 features"
    ```
3.  Push the tag to GitHub, which will trigger the CD workflow:
    ```
    git push origin vX.Y.Z
    ```

#### Important Note for Forks
GitHub Secrets and Variables are **not** transferred when a repository is forked. This is a critical security feature. If you fork this project, you must configure your own secrets and variables in your repository's settings for the CI/CD workflows to function correctly.

Go to `Settings > Secrets and variables > Actions` and create the following entries:

##### **Repository Secrets**
*(For sensitive data that should be encrypted)*
-   `DOCKERHUB_TOKEN`: Your access token for Docker Hub.
-   `DOCKERHUB_USERNAME`: Your username for Docker Hub.
-   `POSTGRES_PASSWORD`: The password for the test database (e.g., `testpassword`).
-   `SECRET_KEY`: A secret key for Flask sessions (e.g., `a-random-string-for-ci`).

##### **Repository Variables**
*(For non-sensitive configuration data)*
-   `FLASK_APP`: `app.py`
-   `FLASK_ENV`: `development`
-   `POSTGRES_DB`: The name for the test database (e.g., `athenadb_test`).
-   `POSTGRES_USER`: The username for the test database (e.g., `postgres`).


## Project Structure
-   `app/`: Contains the Flask application (Python code, templates, static files).
-   `nginx/`: Configuration files for NGINX.
-   `tests/`: Pytest tests.
-   `.github/workflows/`: GitHub Actions workflow files.
-   **`ansible/`**: Contains the Ansible automation logic.
    -   `playbook.yml`: The main playbook that orchestrates the deployment.
    -   `secrets.yml`: Your local, encrypted file with all secrets.
    -   `inventory`: Defines the hosts for deployment (e.g., `localhost`).
    -   `roles/`: Contains the separated logic for `common`, `docker`, and `deploy`.
-   `Dockerfile`: Instructions for building the Flask application image.
-   `docker-compose.yml`: Defines the services for the main Docker environment.
-   `docker-compose-test.yml`: Defines the services for the test environment.
-   `requirements.txt`: Python dependencies.

