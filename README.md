# Athena Web Quiz – DevOps Starter Skeleton

This repository provides a **comprehensive DevOps starter skeleton** for the Athena Web Quiz assignment, inspired by Athena's theme of wisdom and knowledge. It includes a fully functional Flask web application with backend and frontend components, allowing users to create and take quizzes. The focus of this project is on DevOps practices such as containerization, service orchestration, and CI/CD, rather than complex application logic. The core technologies include a Python/Flask backend, a PostgreSQL database for storing quiz data, and an NGINX reverse proxy that terminates TLS and forwards requests to the Flask app.

## What You Get

- **Backend**: A complete Flask application with:
  - Models and routes for creating quizzes, adding questions, taking quizzes, and viewing results.
  - Endpoints like `/health` for monitoring, `/create_quiz` for quiz creation, and more.
- **Frontend**: A user-friendly interface with:
  - HTML templates for all user interactions (create quiz, add questions, take quiz, view results).
  - CSS styling for a clean, modern look.
  - JavaScript for basic interactivity and form validation.
- **Database**: SQLAlchemy models for quizzes, questions, answers, and results, ready to connect with PostgreSQL within a Docker Compose setup.
- **Sample Data**: Initial quiz data to test the application, automatically populated on first startup if the database is empty.
- **NGINX Config**: Placeholder configuration for a reverse proxy (no TLS by default).
- **Docker Setup**: Empty `Dockerfile` and `docker-compose.yml` for you to implement containerization and orchestration.
- **CI/CD**: Example GitHub Actions workflow as a template.
- **Tests**: Minimal test for the `/health` endpoint.
- **`CONTRIBUTORS.md`**: For tracking team contributions.

## How to Start

1. **Clone this repository.**
2. **Set up your Python environment** (e.g., `python -m venv venv && source venv/bin/activate`).
3. **Install dependencies:**
   ```sh
   pip install -r app/requirements.txt
   ```
4. **Set up the database (for local development):**
   - Configure the database URL in `app/config.py` if needed (default is SQLite for local simplicity).
   - Initialize the database:
     ```sh
     flask db init
     flask db migrate
     flask db upgrade
     ```
   - Note: When using Docker Compose, the database will be part of the orchestrated services (PostgreSQL), and the application is set to initialize the schema automatically on startup.
5. **Run the Flask app locally:**
   ```sh
   python -m app.app
   ```
   - Access the app at `http://localhost:5000` to create quizzes, take them, and view results. Sample data will be populated automatically if the database is empty.
6. **Run tests:**
   ```sh
   pytest
   ```
7. **Focus on DevOps tasks:**
   - **Containerization**: Complete the `Dockerfile` to build a Docker image for the Flask app. Ensure it installs dependencies and can run the application.
   - **Orchestration**: Update `docker-compose.yml` to manage the Flask app, PostgreSQL database, and NGINX reverse proxy as a unified stack. Include environment variables for database configuration. The database will be initialized automatically when the containers start.
   - **CI/CD**: Customize the GitHub Actions workflow in `.github/workflows/` to automate testing, building, and deployment.
   - **Security**: Configure NGINX for TLS termination and ensure secure database connections.
   - **Exposure**: Consider using services like Ngrok to temporarily expose your locally hosted or Dockerized application for presentation or testing purposes. For example, after starting your Docker Compose setup, you can run `ngrok http 80` to share access to your NGINX service.
8. **Customize further (optional):**
   - Extend the frontend by modifying HTML, CSS, and JavaScript in `app/templates` and `app/static` for minor customizations to the user interface.
   - Add more features to the backend in `app/app.py` and `app/models.py` if needed (e.g., user authentication), though the focus should remain on DevOps tasks.

## Project Structure

- `app/` : Contains the Flask application.
  - `app.py` : Main application file with all routes and automatic database initialization.
  - `models.py` : Database models for quizzes, questions, answers, and results.
  - `config.py` : Configuration settings.
  - `sample_data.py` : Script to populate the database with sample quiz data (called automatically on startup if needed).
  - `templates/` : HTML templates for the frontend.
  - `static/` : CSS and JavaScript files for styling and interactivity.
- `nginx/` : Placeholder for NGINX configuration.
- `tests/` : Test files for the application.
- `Dockerfile` : Empty file for Docker image definition with commented guidance.
- `docker-compose.yml` : Empty file for Docker service orchestration with commented examples.
- `.github/workflows/` : Example CI/CD pipeline using GitHub Actions.

## Contributors

- Use `CONTRIBUTORS.md` to record your work. Each team member should add their name, GitHub username, and a brief summary of their contributions. This helps instructors review individual work.

## References

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [Docker Compose Docs](https://docs.docker.com/compose/)
- [NGINX Docs](https://nginx.org/en/docs/)
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Ngrok Documentation](https://ngrok.com/docs) for exposing your application.

---

**Note:** The provided `Dockerfile` and `docker-compose.yml` are intentionally left empty with comments. You are expected to complete them as part of your assignment. The application is fully functional locally and within a Docker Compose setup, with automatic database initialization on startup. Your primary task is to apply DevOps practices to deploy and manage it. Ensure your Docker setup supports running the application as a cohesive stack with PostgreSQL and NGINX.
