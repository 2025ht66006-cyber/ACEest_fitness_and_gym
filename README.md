# ACEest Fitness & Gym DevOps Assignment

## Project Overview
This project implements a Flask-based fitness center API with a CI/CD workflow using GitHub Actions and Jenkins. It is built to satisfy the assignment criteria for:
- Application Integrity
- Version Control
- Testing Coverage
- Docker Efficiency
- Pipeline Reliability
- Documentation Clarity

## Project Structure
- `app.py` - Flask application entry point
- `requirements.txt` - project dependencies
- `tests/test_app.py` - pytest test suite
- `pytest.ini` - pytest configuration with coverage checks
- `Dockerfile` - multi-stage builder containerization
- `.dockerignore` - files excluded from image context
- `.github/workflows/main.yml` - CI/CD workflow
- `Jenkinsfile` - Jenkins pipeline script
- `README.md` - this documentation

## Local setup
1. Clone
   ```bash
git clone https://github.com/2025ht66006-cyber/ACEest_fitness_and_gym.git
cd ACEest_fitness_and_gym
```
2. Create venv
   ```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
3. Run app
   ```bash
python app.py
```
4. Access
   - `http://localhost:5000/`
   - `http://localhost:5000/members`

## Test commands
- `pytest`
- `pytest --cov=app --cov-fail-under=80`

## Docker commands
- `docker build -t aceest-gym:latest .`
- `docker run -p 5000:5000 aceest-gym:latest`

## Git workflow
- `main`, `dev`, `feature/*`, `hotfix/*`
- commit prefix: `feat:`, `fix:`, `docs:`, `refactor:`, `chore:`

## CI/CD
- GitHub Actions in `.github/workflows/main.yml`
- Jenkins pipeline to trigger builds from GitHub webhooks

## Evaluation alignment
- Application integrity: endpoint tests + sanity checks
- VCS maturity: branch strategy + commit style
- Testing coverage: `pytest --cov-fail-under=80`
- Docker efficiency: multi-stage image + .dockerignore
- Pipeline: lint + test + build in Actions
- Documentation: this README + plan doc
