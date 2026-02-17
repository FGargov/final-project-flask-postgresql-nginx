# Athena Web Quiz – DevOps Project

Athena Web Quiz is a fully functional Flask web application for creating and taking quizzes, built to demonstrate modern DevOps practices.

The project showcases:

- Containerization with Docker
- Orchestration with Docker Compose
- Infrastructure as Code (IaC) with Ansible
- CI/CD pipelines using GitHub Actions
- Secure secret management with Ansible Vault

---

# 1. Application Features

-   **Quiz Creation:** Users can create new quizzes with multiple questions and answers.
-   **Quiz Taking:** Users can take available quizzes.
-   **View Results:** Ability to view the results of completed quizzes.
-   **Database:** PostgreSQL for storing data related to quizzes, questions, answers, and results.
-   **Sample Data:** Automatic population of the database with sample data on initial startup if it's empty.
-   **Health Check:** `/health` endpoint for checking the application's status.

---

# 2. DevOps Architecture & Technologies

## 2.1 Containerization

- `Dockerfile` builds the Flask application image
- `docker-compose.yml` orchestrates:
  - Flask
  - PostgreSQL
  - NGINX
- Health checks ensure correct startup order

## 2.2 Infrastructure as Code (Ansible)

Fully automated deployment using a role-based structure:

- `common`  
  Installs base dependencies (e.g., git)

- `docker`  
  Ensures Docker and Docker Compose are installed and running

- `deploy`  
  - Clones repository
  - Generates secure `.env` from template
  - Starts Docker Compose stack

### Security

- All secrets are encrypted using **Ansible Vault**
- No credentials are stored in plaintext in the repository

## 2.3 CI/CD (GitHub Actions)

- Automated linting and testing (CI)
- Automated image build & release (CD)
- Docker Hub publishing
- GitHub Releases automation

## 2.4 Testing

- Pytest integration tests
- Isolated Docker test environment (`docker-compose-test.yml`)

## 2.5 Security

- TLS termination via NGINX
- GitHub Secrets for CI/CD credentials

---

# 3. Prerequisites

Make sure you have:

- Git
- Docker
- Docker Compose
- Ansible

---

# 4. Local Setup and Deployment (with Ansible)

## 4.1 Clone the Repository

```bash
git clone https://github.com/<your_username>/<your_repository_name>.git
cd <your_repository_name>
```

---

## 4.2 Configure Ansible Secrets

Navigate to the Ansible directory:

```bash
cd ansible
```

Create a file named:

```
secrets.yml
```

Do NOT name it `.env`.

Example content:

```yaml
FLASK_APP: "app.py"
FLASK_ENV: "development"

SECRET_KEY: "your-very-secret-flask-key"

POSTGRES_USER: "postgres"
POSTGRES_PASSWORD: "strong-password"
POSTGRES_DB: "athenadb"
```

Encrypt the file:

```bash
ansible-vault encrypt secrets.yml
```

You will be prompted to create a vault password.

---

## 4.3 Run the Ansible Playbook

```bash
ansible-playbook -i inventory playbook.yml --ask-vault-pass -K
```

You will be prompted for:

1. **BECOME password** – your local sudo password  
2. **Vault password** – the password used to encrypt `secrets.yml`

After execution, the application stack will be deployed under:

```
/root/final-project/
```

---

# 5. Access the Application

- HTTP:  
  http://localhost

- HTTPS (if configured):  
  https://localhost

---

# 6. Application Lifecycle Management

All commands target:

```
/root/final-project/docker-compose.yml
```

## 6.1 Stop (Keep Containers)

```bash
sudo docker compose -f /root/final-project/docker-compose.yml stop
```

Stops containers without removing them.

---

## 6.2 Start (Previously Stopped Containers)

```bash
sudo docker compose -f /root/final-project/docker-compose.yml start
```

---

## 6.3 Restart the Stack

```bash
sudo docker compose -f /root/final-project/docker-compose.yml restart
```

---

## 6.4 Remove Containers (Keep Database)

```bash
sudo docker compose -f /root/final-project/docker-compose.yml down
```

Removes:
- Containers
- Network

Keeps:
- Volumes (database data preserved)

---

## 6.5 Full Cleanup (Including Database)

```bash
sudo docker compose -f /root/final-project/docker-compose.yml down -v
```

⚠ This removes PostgreSQL data permanently.

---

# 7. Running Tests Locally

## 7.1 Optional: Create `.env.test`

If needed, create:

```
.env.test
```

Ensure `docker-compose-test.yml` references it:

```yaml
env_file:
  - .env.test
```

---

## 7.2 Run Tests

```bash
docker compose -f docker-compose-test.yml \
  --env-file .env.test \
  up --build \
  --abort-on-container-exit \
  --exit-code-from flask_app
```

Options explained:

- `--build` → rebuild images
- `--abort-on-container-exit` → stop all containers when tests finish
- `--exit-code-from flask_app` → return pytest exit code

---

# 8. CI/CD Pipeline

## 8.1 Continuous Integration (CI)

Triggered on:
- Push to `feature/*`
- Push to `dev`
- Pull Requests to `dev` or `main`

Workflow:
- Run `flake8`
- Run `pytest` in Docker test environment

---

## 8.2 Continuous Deployment (CD)

Triggered on:

```
v*.*.*
```

Examples:
- v1.0.0
- v1.4.0-beta.0

Pipeline actions:
- Build Docker image
- Tag with version
- Tag `latest` (stable only)
- Push to Docker Hub
- Create GitHub Release

Pull image:

```bash
docker pull <your_dockerhub_username>/athena-web-quiz:<tag>
```

---

## 8.3 Creating a New Release

```bash
git checkout main
git pull origin main
git tag -a vX.Y.Z -m "Release description"
git push origin vX.Y.Z
```

---

# 9. Project Structure

```
app/                    Flask application
nginx/                  NGINX configuration
tests/                  Pytest tests
ansible/                Infrastructure automation
.github/workflows/      CI/CD pipelines

Dockerfile
docker-compose.yml
docker-compose-test.yml
requirements.txt
```

Inside `ansible/`:

```
playbook.yml
inventory
roles/
secrets.yml (encrypted)
```

---

# 10. Summary

This project demonstrates:

- Full containerized architecture
- Infrastructure as Code
- Secure secret management
- CI/CD automation
- Production-ready deployment structure


