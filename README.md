# ACEest Fitness & Gym DevOps Assignment

[![CI-CD Pipeline](https://github.com/2025ht66006-cyber/ACEest_fitness_and_gym/actions/workflows/main.yml/badge.svg)](https://github.com/2025ht66006-cyber/ACEest_fitness_and_gym/actions/workflows/main.yml)

## Overview
This project demonstrates a complete DevOps pipeline for a Flask-based fitness and gym management application. It covers modern best practices in version control, automated testing, containerization, and CI/CD using GitHub Actions and Jenkins.

---

## Project Structure
- `app.py` — Main Flask application
- `requirements.txt` — Python dependencies
- `tests/` — Pytest test suite
- `Dockerfile` — Multi-stage Docker build
- `.github/workflows/main.yml` — GitHub Actions pipeline
- `Jenkinsfile` — Jenkins pipeline (for build/quality gate)
- `README.md` — Project documentation

---

## Local Setup & Execution

1. **Clone the repository**
   ```bash
   git clone https://github.com/2025ht66006-cyber/ACEest_fitness_and_gym.git
   cd ACEest_fitness_and_gym
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```
   Visit [http://localhost:5000](http://localhost:5000) in your browser.

---

## Running Tests

- Run all tests:
  ```bash
  pytest
  ```
- Run tests with coverage (required: 80%+):
  ```bash
  pytest --cov=app --cov-fail-under=80
  ```

---

## Docker Usage

- **Build the Docker image:**
  ```bash
  docker build -t aceest-gym:latest .
  ```
- **Run the container:**
  ```bash
  docker run -p 5000:5000 aceest-gym:latest
  ```

---

## CI/CD Pipelines

### GitHub Actions
- Triggers on every push and pull request to `main` and `dev`
- Stages:
  - Lint (flake8)
  - Test (pytest with coverage)
  - Docker build and validation

### Jenkins
- Pulls latest code from GitHub
- Stages:
  - Checkout
  - Install dependencies
  - Lint
  - Test (with coverage)
  - Docker build

---

## Branching & Version Control

- `main`: Production-ready code
- `dev`: Integration branch
- `feature/*`: Feature branches
- `hotfix/*`: Hotfixes

Commits use conventional prefixes: `feat:`, `fix:`, `docs:`, `refactor:`, `chore:`

---

## Evaluation Criteria Mapping

- **Application Integrity:** Flask app with all required endpoints and logic
- **VCS Maturity:** Structured commits, clear branching
- **Testing Coverage:** Pytest suite, coverage enforced in CI
- **Docker Efficiency:** Multi-stage build, minimal image
- **Pipeline Reliability:** Jenkins and GitHub Actions, automated build/test
- **Documentation Clarity:** This README covers all requirements

---

## Notes

- Legacy scripts (Aceestver-*.py) are archived and not part of the main pipeline.
- Only `app.py` and files in the root are used for CI/CD and deployment.
