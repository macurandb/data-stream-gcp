# Use a base image for Python
FROM python:3.12-slim

# Set author label
LABEL authors="duany"

# Install dependencies for Poetry, curl, and other required tools
RUN pip3 install poetry

# Add Poetry to the PATH for all future commands
ENV POETRY_HOME="/root/.local"
ENV PATH="$POETRY_HOME/bin:$PATH"

# Set the working directory
WORKDIR /app

# Copy Poetry configuration files first to leverage Docker cache
COPY pyproject.toml poetry.lock /app/

# Install project dependencies without creating a virtual environment (for Docker)
RUN poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction --no-ansi

# Copy the application source code
COPY cloud-function/src/ /app

# Expose port 8080 (if using Flask or similar)
EXPOSE 8080

# Set the entry point to run the Python application
CMD ["poetry", "run" ,"python", "deib/api/app.py"]
