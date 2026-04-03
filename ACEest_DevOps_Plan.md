# ACEest Fitness & Gym DevOps Implementation Plan

## Overview
This document provides a step-by-step implementation plan to complete the assignment covering:
- GitHub version control
- Flask app development
- Unit test coverage
- Docker containerization
- Jenkins build integration
- GitHub Actions CI/CD

It is structured to meet the evaluation criteria in the assignment prompt.

---

## 1. Application Integrity (Flask App)

### 1.1 Project structure
Create repository structure:
- `app.py`
- `requirements.txt`
- `Dockerfile`
- `tests/`
- `.github/workflows/main.yml`
- `README.md`
- `Jenkinsfile` (optional)

### 1.2 Flask baseline
`app.py`:
- create `Flask(__name__)`
- endpoints: `/`, `/members`, `/workouts`, `/metrics`
- example logic from ACEest feature set

### 1.3 Python dependency file
`requirements.txt` includes:
- Flask
- pytest
- pytest-cov
- gunicorn (optional)
- requests (for API tests)

---

## 2. VCS Maturity (Git configuration)

### 2.1 Branching strategy
- `main`: production-ready
- `dev`: integration pre-release
- `feature/<name>`: feature branches
- `hotfix/<id>`: urgent bug fixes

### 2.2 Commit message policy
- `feat:` new feature
- `fix:` bug fix
- `docs:` documentation
- `style:` formatting
- `refactor:` code refactor
- `chore:` tooling

### 2.3 PR template
Add file: `.github/PULL_REQUEST_TEMPLATE.md` with checklist:
- [ ] Tests run locally
- [ ] Code lint passes
- [ ] Pipeline passes
- [ ] Docs updated

---

## 3. Testing Coverage (Pytest)

### 3.1 Create tests
- `tests/test_app.py`
- every endpoint status code and behavior
- function-level tests for business logic

### 3.2 Enforce coverage
`pytest.ini`:
```ini
[pytest]
addopts = --maxfail=1 --disable-warnings -q --cov=app --cov-report=term-missing
python_files = tests/test_*.py
```

### 3.3 Local run commands
- `python -m pytest`
- `python -m pytest --cov --cov-fail-under=80`

---

## 4. Docker Efficiency

### 4.1 Dockerfile multi-stage
```Dockerfile
FROM python:3.11-slim AS builder
WORKDIR /workspace
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /workspace/app.py ./
COPY --from=builder /workspace/requirements.txt ./
EXPOSE 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
```

### 4.2 Build/run
- `docker build -t aceest-gym:latest .`
- `docker run -p 5000:5000 aceest-gym:latest`

### 4.3 .dockerignore
```
__pycache__
*.pyc
venv
.git
.github
tests
```

---

## 5. Jenkins BUILD & Quality Gate

### 5.1 Jenkins job config
- SCM: GitHub repository URL
- Build trigger: GitHub hook trigger for GITScm polling
- Build steps:
  1. `docker build --tag aceest-gym:jenkins .`
  2. `docker run --rm aceest-gym:jenkins pytest --maxfail=1 --disable-warnings -q`

### 5.2 Build result quality gates
- Fail on test failure
- Fail on non-zero exit
- Add notification for failed build (email/Slack)

---

## 6. GitHub Actions CI/CD

### 6.1 Workflow file
`.github/workflows/main.yml`:
```yaml
name: CI CD
on:
  push:
    branches: [main, dev]
  pull_request:
    branches: [main, dev]

jobs:
  lint-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: 3.11
      - name: Install dependencies
        run: python -m pip install --upgrade pip && pip install -r requirements.txt
      - name: Lint
        run: pip install flake8 && flake8 .
      - name: Run tests
        run: pytest --cov=app --cov-fail-under=80

  docker-build:
    needs: [lint-test]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build Docker image
        run: docker build -t aceest-gym:latest .
      - name: Optionally push image
        if: github.ref == 'refs/heads/main'
        run: |
          echo "TODO: Docker login + push to registry"
```

---

## 7. Documentation Clarity

### 7.1 README sections
- Project summary
- Setup instructions
- Run commands
- Test commands
- Docker + pipeline commands
- Branching + git policy
- CI/CD badge placeholders

### 7.2 Status badges
- GitHub Actions
- Jenkins
- Coverage (e.g., Codecov)

---

## 8. Evaluation checklist
- [ ] Application integrity verified with endpoint tests
- [ ] Git history meaningful and structured
- [ ] Pytest coverage >= 80% enforced
- [ ] Dockerfile multi-stage and minimal image
- [ ] Jenkins job successful on build trigger
- [ ] GitHub Actions success on push/PR
- [ ] Documentation complete and professional

---

## 9. Suggested execution order
1. Flask app and minimal tests
2. Local pytest + coverage
3. Dockerfile + local container test
4. GitHub repo + branches
5. GitHub Actions config + run
6. Jenkins pipeline integration
7. Final docs + badges
