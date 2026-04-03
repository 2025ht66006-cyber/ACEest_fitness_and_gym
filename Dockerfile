FROM python:3.11-slim AS base
WORKDIR /app

COPY requirements.txt ./
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

FROM base AS test
COPY app.py pytest.ini ./
COPY tests ./tests
CMD ["python", "-m", "pytest"]

FROM base AS runtime
COPY app.py ./
EXPOSE 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
