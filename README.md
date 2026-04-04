# ACEest Fitness & Gym DevOps Assignment

[![CI-CD Pipeline](https://github.com/2025ht66006-cyber/ACEest_fitness_and_gym/actions/workflows/main.yml/badge.svg)](https://github.com/2025ht66006-cyber/ACEest_fitness_and_gym/actions/workflows/main.yml)

## Overview
This project demonstrates a DevOps workflow for a Flask-based fitness and gym management application. It covers version control, unit testing, Docker containerization, GitHub Actions CI, and Jenkins-based build validation.

## Project Structure
- `app.py` - main Flask application
- `app_static.py` - serves both the Flask API backend and static frontend files
- `requirements.txt` - Python dependencies
- `tests/` - Pytest suite
- `Dockerfile` - multi-stage Docker build for test and runtime images
- `.github/workflows/main.yml` - GitHub Actions pipeline
- `Jenkinsfile` - Jenkins build pipeline
- `README.md` - project documentation

## Local Setup & Execution
1. Clone the repository:

```bash
git clone https://github.com/2025ht66006-cyber/ACEest_fitness_and_gym.git
cd ACEest_fitness_and_gym
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the application:

```bash
python app.py
```

The API starts on `http://localhost:5000`.

Note: app_static.py serves both the Flask API backend and static frontend files (HTML, CSS, JS) from a single application, combining backend and frontend into one integrated app.

## Running Tests
- Run lint:

```bash
python -m flake8 app.py tests
```

- Run unit tests with coverage:

```bash
python -m pytest --cov=app --cov-fail-under=80
```

## Docker Usage
- Build and run the test image:

```bash
docker build --target test -t aceest-gym:test .
docker run --rm aceest-gym:test
```

- Build and run the runtime image:

```bash
docker build --target runtime -t aceest-gym:latest .
docker run --rm -p 5000:5000 aceest-gym:latest
```

## CI/CD Pipelines
### GitHub Actions
- Triggers on every `push` and `pull_request`
- `lint-test`: installs dependencies, runs flake8, then runs pytest with coverage
- `docker-test`: builds the Docker test stage and runs pytest inside the container
- `docker-runtime-smoke`: builds the runtime image and checks the health endpoint

### Jenkins
- Pulls the latest code from GitHub
- Runs `Checkout`, `Install`, `Lint`, `Test`, `Docker Test`, `Docker Runtime Build`, and `Docker Run Smoke Test`
- Publishes JUnit test results from `test-results.xml`

## Branching & Version Control
- `main`: production-ready code
- `dev`: integration branch
- `feature/*`: feature branches
- `hotfix/*`: urgent fixes

Commits use conventional prefixes such as `feat:`, `fix:`, `docs:`, `refactor:`, and `chore:`.

## Evaluation Criteria Mapping
- **Application Integrity:** Flask app with the required endpoints and logic
- **VCS Maturity:** structured commit history and branch strategy
- **Testing Coverage:** Pytest suite with coverage gate of 80% or higher
- **Docker Efficiency:** multi-stage Dockerfile with separate test and runtime stages
- **Pipeline Reliability:** Jenkins and GitHub Actions both validate lint, tests, and Docker flow
- **Documentation Clarity:** this README documents setup, validation, and CI/CD behavior

## Notes
- Legacy scripts in `legacy/` are archived and not part of the primary CI path.
- The Docker `test` stage is for containerized validation, while the `runtime` stage is the deployment image.
