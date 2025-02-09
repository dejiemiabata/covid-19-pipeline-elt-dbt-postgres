FROM python:3.12-slim 


# Install system level dependencies

RUN apt-get update && apt-get install -y \
  curl \
  build-essential \
  libpq-dev \
  && rm -rf /var/lib/apt/lists/*


# creare non-root user with user id
RUN useradd -u 8877 appuser

ENV PROJECT_DIR=/Project

# set the working directory to the project root
WORKDIR $PROJECT_DIR

# set Poetry version and disable virtual envs create
ENV POETRY_VIRTUALENVS_CREATE=false \
  POETRY_VERSION=1.8.3 \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local'

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

# Copy Poetry files; Also for caching purposes
COPY pyproject.toml poetry.lock $PROJECT_DIR/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --without dev

# Copy Project
COPY . $PROJECT_DIR

# Change the ownership of the working directory to the non-root user "user"
RUN chown -R appuser:appuser $PROJECT_DIR

# Switch to non-root user "appuser"
USER appuser