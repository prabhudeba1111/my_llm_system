# ---- Base image ----
FROM python:3.11-slim

# ---- Environment ----
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ---- Working directory ----
WORKDIR /app

# ---- Install runtime dependencies ----
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- Copy source code ----
COPY src ./src
COPY pyproject.toml .
COPY README.md .

# ---- Default command ----
CMD ["python", "-m", "src.main"]
