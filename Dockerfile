# Base image
FROM python:3.10.9

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python -

# Install tmux (if not already installed)
RUN apt-get update && apt-get install -y tmux

# Set the working directory in the container
WORKDIR /app

# Copy only the pyproject.toml and poetry.lock files to leverage Poetry caching
COPY pyproject.toml poetry.lock /app/

# Install project dependencies with Poetry
RUN poetry install

# Copy the rest of the project files to the working directory
COPY . /app

# Set the environment variables for Celery
ENV C_FORCE_ROOT=1

# Add a shell script for running multiple commands using tmux
RUN echo '#!/bin/bash\n\
    redis-server &\n\
    tmux new-session -d -s celery_worker "celery -A main worker --loglevel=info --include tasks"\n\
    tmux new-session -d -s celery_beat "celery -A celery_base beat -l info"\n\
    python3 main.py' > run.sh
RUN chmod +x run.sh

# Run the shell script as the CMD
CMD ["/bin/bash", "-c", "./run.sh"]
