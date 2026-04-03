# ACEest Fitness & Gym DevOps Recovery Plan

## Purpose
This document is the working plan for completing and evaluating the ACEest Fitness & Gym DevOps assignment.

It is written from two perspectives at the same time:
- `Developer view`: what we need to build or fix
- `Instructor/Evaluator view`: what will be checked during assessment

The goal is not just to "have files present". The goal is to make sure the workflow actually matches the assignment in:
- Flask application behavior
- Pytest validation
- Docker containerization
- Jenkins build validation
- GitHub Actions CI/CD
- documentation and repository quality

---

## 1. Assignment Requirements We Must Satisfy

Based on [Introduction_to_DevOps_Assignment_md.md](./Introduction_to_DevOps_Assignment_md.md), the required workflow is:

1. Build a modular Flask application.
2. Maintain the project in Git/GitHub using meaningful commits and branches.
3. Add Pytest-based unit tests.
4. Containerize the application using Docker.
5. Use Jenkins as a BUILD and quality gate environment.
6. Use GitHub Actions to automate CI/CD on every `push` and `pull_request`.
7. In GitHub Actions, the pipeline must include:
   - Build and lint
   - Docker image build
   - Automated testing
   - testing inside the containerized environment

Required deliverables:
- application source code
- tests
- Dockerfile
- GitHub Actions workflow
- README with setup, test, and CI/CD explanation

---

## 2. Current Project Status

### What is already present
- `app.py`
- `tests/test_app.py`
- `Dockerfile`
- `Jenkinsfile`
- `.github/workflows/main.yml`
- `README.md`
- `requirements.txt`

### What already works
- The Flask app has the expected endpoints:
  - `/`
  - `/members`
  - `/workouts`
  - `/metrics`
- Pytest runs successfully and coverage is above 80%.
- The repository has a reasonable commit history with structured commit messages.

### What is not yet correct
- Linting currently fails.
- Jenkins is not configured to publish test results correctly.
- GitHub Actions does not fully match the assignment wording.
- The Docker/testing approach does not yet support running tests inside the container.
- The repository contains tracked generated files and artifacts that reduce professionalism.

---

## 3. Error Breakdown and How to Fix Each One

This section is the most important part of the plan.

For each issue:
- `Problem`: what is wrong now
- `Why it matters`: why the evaluator will care
- `How to fix`: exact implementation direction
- `How to verify`: what command or outcome proves it is solved

---

## 3.1 Error 1: Flake8 Lint Stage Fails

### Problem
The CI workflow runs `flake8 .`, but `app.py` currently violates flake8 rules.

Observed issues include:
- missing blank lines between top-level functions
- one line longer than the configured max line length

### Why it matters
The assignment explicitly requires a build/lint stage in GitHub Actions.

If lint fails:
- the GitHub Actions workflow fails early
- the project cannot be considered pipeline-reliable
- the README claim that CI is working becomes inaccurate

### How to fix
Update `app.py` to follow flake8/PEP 8:
- add blank lines between route functions
- split long dictionary lines into multiple lines
- keep formatting clean and stable

Optional improvement:
- run `flake8 app.py tests` instead of `flake8 .`

Reason:
- `flake8 .` may inspect unintended files if the repo contains generated content
- a more targeted lint scope is cleaner and more predictable

### How to verify
Run:

```powershell
.\.venv\Scripts\flake8 app.py tests
```

Expected result:
- no output
- exit code 0

Also verify GitHub Actions passes the lint stage.

---

## 3.2 Error 2: Jenkins JUnit Publishing Is Misconfigured

### Problem
The Jenkins pipeline includes:

```groovy
junit '**/test-results.xml'
```

But the test stage only runs:

```groovy
pytest --cov=app --cov-fail-under=80
```

No JUnit XML report is generated.

### Why it matters
From an evaluator perspective, Jenkins should be a real build environment, not a placeholder.

If Jenkins tries to publish a report that does not exist:
- the pipeline may fail in `post`
- or it may show misleading results
- test evidence is not properly surfaced in Jenkins

### How to fix
Choose one of these valid options:

#### Option A: Generate a JUnit report
Update the Jenkins test command to:

```groovy
pytest --cov=app --cov-fail-under=80 --junitxml=test-results.xml
```

Keep the `junit '**/test-results.xml'` publisher.

This is the best option because it gives Jenkins a real test report.

#### Option B: Remove the JUnit publisher
If test report publication is not required for the assignment, remove the `junit` line.

This is simpler, but weaker from a professional pipeline perspective.

### Recommended decision
Use Option A.

### How to verify
In Jenkins:
- trigger a build
- confirm the test stage passes
- confirm Jenkins shows published test results
- confirm the post stage no longer fails due to missing report file

---

## 3.3 Error 3: GitHub Actions Trigger Is Too Narrow

### Problem
The assignment says the workflow must be triggered on every `push` and `pull_request`.

The current workflow is limited to:

```yaml
on:
  push:
    branches: [main, dev]
  pull_request:
    branches: [main, dev]
```

### Why it matters
This is a mismatch with the problem statement.

If someone pushes to:
- `feature/login`
- `feature/docker-fix`
- `hotfix/metrics`

the workflow may not run.

That means code can bypass validation before merging.

### How to fix
Adjust the workflow trigger to validate all pushes and pull requests.

Recommended:

```yaml
on:
  push:
  pull_request:
```

If branch filtering is truly required later, document the reason carefully. For this assignment, broad validation is better aligned.

### How to verify
Create a test branch and push a small change.

Expected:
- GitHub Actions starts automatically on that branch push

Also open a PR and confirm the workflow runs there too.

---

## 3.4 Error 4: Tests Are Not Running Inside the Container

### Problem
The assignment explicitly says:

`Automated Testing: Execute the Pytest suite inside the containerized environment to confirm stability.`

Current behavior:
- GitHub Actions runs pytest on the GitHub runner
- Docker is built afterward
- the container is only smoke-tested with `curl /`

Current Docker image contents:
- `app.py`
- installed dependencies

Not included:
- `tests/`
- `pytest.ini`

So the current image cannot run the full test suite inside the container.

### Why it matters
This is one of the most important assignment mismatches.

The evaluator can reasonably say:
- Docker was built, yes
- but test execution did not happen inside the containerized environment

That means the workflow only partially satisfies the CI/CD requirement.

### How to fix
There are two clean approaches.

#### Option A: Build a dedicated test image
Use a multi-stage Docker strategy:
- one stage for dependencies
- one `test` stage that includes:
  - `app.py`
  - `tests/`
  - `pytest.ini`
- one runtime stage for production execution

Then in GitHub Actions:
- build the test stage
- run pytest inside that container
- build the runtime image
- run smoke validation

This is the best design.

#### Option B: Build the image and mount tests at runtime
Run containerized pytest by mounting the repo into the container:

```bash
docker run --rm -v $PWD:/app aceest-gym:latest pytest
```

This works, but it is less clean and less portable in CI, especially across shells and platforms.

### Recommended decision
Use Option A with explicit test and runtime stages.

### How to verify
Run a containerized test command in CI and locally.

Expected:
- pytest executes from inside a Docker container
- all tests pass
- coverage threshold is still met

---

## 3.5 Error 5: Repository Hygiene Is Weak

### Problem
The repository currently tracks files that should usually not be committed:
- `.coverage`
- `__pycache__/`
- `tests/__pycache__/`
- Office temp file starting with `~$`
- large zip/archive artifacts

### Why it matters
This may not directly fail the assignment, but it hurts the professional quality score:
- unnecessary build context
- noisy repository
- confusing artifacts for evaluators
- harder CI maintenance

### How to fix
Add or improve `.gitignore` so it excludes:

```gitignore
__pycache__/
*.pyc
.coverage
.pytest_cache/
.venv/
venv/
~$*.docx
*.zip
```

Then remove already-tracked generated files from git using non-destructive cleanup.

### How to verify
Run:

```powershell
git status
git ls-files
```

Expected:
- generated files no longer appear as tracked artifacts
- repo content looks intentional and clean

---

## 3.6 Error 6: README Overstates Pipeline Reliability

### Problem
The README currently describes the CI/CD pipeline as if it is fully reliable.

But at the moment:
- flake8 is failing
- Jenkins reporting is incomplete
- containerized pytest is not implemented

### Why it matters
Documentation is part of the assignment deliverables.

If the README promises more than the repo actually does, an evaluator may mark down:
- documentation clarity
- engineering honesty
- reproducibility

### How to fix
Update `README.md` so it reflects the true final behavior after fixes are made:
- local setup
- test commands
- lint commands
- Docker build and run commands
- how Jenkins validates builds
- how GitHub Actions validates pushes and PRs
- whether tests run in container stage, and how

### How to verify
A new engineer should be able to:
1. clone the repo
2. create a venv
3. install dependencies
4. run lint
5. run tests
6. build Docker
7. understand CI/CD flow from README alone

---

## 4. Implementation Plan for GPT-4.1 Machine

Use this as the execution order on your other machine.

### Phase 1: Fix code quality first
1. Update `app.py` formatting so flake8 passes.
2. Run:

```powershell
python -m pytest
python -m flake8 app.py tests
```

3. Confirm:
- tests pass
- lint passes

### Phase 2: Improve Docker for test execution
1. Refactor `Dockerfile` to support:
- dependency install stage
- test stage
- runtime stage

2. Ensure test-related files are available in the test stage.
3. Keep runtime image minimal.

### Phase 3: Correct GitHub Actions
1. Update `.github/workflows/main.yml` so it:
- runs on every push
- runs on every pull request
- installs dependencies
- runs flake8
- runs pytest
- builds Docker
- runs pytest inside the containerized environment
- optionally performs a smoke test on the runtime container

### Phase 4: Correct Jenkins
1. Update `Jenkinsfile` so it:
- checks out code
- installs dependencies
- runs lint
- runs pytest with coverage
- generates `test-results.xml`
- publishes JUnit results
- builds Docker
- optionally runs a smoke test

### Phase 5: Clean repository hygiene
1. Create or update `.gitignore`.
2. Remove tracked generated files.
3. Keep only source, tests, docs, and assignment-relevant artifacts.

### Phase 6: Refresh documentation
1. Update `README.md`.
2. Make sure the CI/CD explanation matches the real implementation.
3. Add exact commands for:
- local setup
- tests
- lint
- docker build
- docker run

---

## 5. Suggested Final GitHub Actions Design

This is the intended behavior, not necessarily the exact YAML yet.

### Job 1: `lint-and-unit-test`
- checkout code
- setup Python 3.11
- install requirements
- run flake8
- run pytest with coverage

### Job 2: `docker-test`
- build Docker test image/stage
- run pytest inside container

### Job 3: `docker-runtime-smoke`
- build runtime image
- run container
- curl health endpoint

Benefits:
- direct alignment with assignment wording
- clearer troubleshooting
- cleaner separation of concerns

---

## 6. Suggested Final Jenkins Design

### Jenkins stages
1. `Checkout`
2. `Install`
3. `Lint`
4. `Test`
5. `Publish Test Report`
6. `Docker Build`
7. `Smoke Test`

### Recommended pytest command

```bash
pytest --cov=app --cov-fail-under=80 --junitxml=test-results.xml
```

### Recommended smoke validation
- start the container on a temporary port
- wait a few seconds
- call `/`
- stop and remove the container

---

## 7. Exact Success Criteria

The assignment should be considered complete only when all of the following are true:

- `app.py` works locally
- `pytest` passes locally
- coverage is at least 80%
- `flake8` passes locally
- Docker image builds successfully
- tests run successfully inside a container
- Jenkins pipeline completes successfully
- GitHub Actions runs on push and pull request
- GitHub Actions passes lint, test, Docker build, and containerized test stages
- README clearly explains the workflow

---

## 8. Practical Command Checklist

Use these commands during implementation and validation.

### Local Python validation

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python -m pytest
python -m flake8 app.py tests
```

### Docker validation

```powershell
docker build -t aceest-gym:latest .
docker run --rm -p 5000:5000 aceest-gym:latest
```

### Optional containerized pytest pattern

```powershell
docker build --target test -t aceest-gym:test .
docker run --rm aceest-gym:test
```

### Git validation

```powershell
git status
git log --oneline --decorate -n 10
```

---

## 9. Evaluator Notes

If I were grading this assignment, I would score it like this right now:

### Strong areas
- application exists and is functional
- tests exist
- coverage is above threshold
- Docker, Jenkins, and Actions files are present
- commit history is reasonably structured

### Weak areas
- pipeline does not fully pass yet
- GitHub Actions does not fully satisfy "test inside container"
- Jenkins report publishing is incomplete
- repo cleanliness can be improved

### Final evaluator judgment
The submission is close to acceptable, but not fully correct until the pipeline defects are fixed.

---

## 10. Immediate Next Actions

These should be done first, in order:

1. Fix `app.py` so flake8 passes.
2. Update `Jenkinsfile` to generate and publish JUnit results correctly.
3. Redesign `Dockerfile` so tests can run inside a container.
4. Update GitHub Actions to run on every push and PR.
5. Add a containerized pytest step in CI.
6. Clean the repository using `.gitignore`.
7. Update README to match the final system.

---

## 11. Working Principle for Development

When developing further on the GPT-4.1 machine, follow this rule:

`Do not treat "file exists" as success. Treat "workflow executes and passes" as success.`

That mindset matches both DevOps practice and the evaluator's expectations.
