# Base image
FROM python:3.10.9

# Install Redis and other dependencies
RUN apt-get update && apt-get install -y redis-server tmux

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="${PATH}:/root/.local/bin"

# Set the working directory in the container
WORKDIR /app

# Copy only the pyproject.toml and poetry.lock files to leverage Poetry caching
COPY pyproject.toml poetry.lock /app/

# Install project dependencies with Poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-root

# Copy the entire 'src' directory into the container
COPY src/ /app/src/

# Set the environment variables for Celery
ENV C_FORCE_ROOT=1

# Set the working directory to /app/
WORKDIR /app/src/

# Add a shell script for running multiple commands using tmux
RUN echo '#!/bin/bash\n\
    redis-server &\n\
    cd /app/src/\n\
    tmux new-session -d -s celery_worker "celery -A main worker --loglevel=info --include tasks"\n\
    tmux new-session -d -s celery_beat "celery -A celery_base beat -l info"\n\
    python3 main.py' > run.sh
RUN chmod +x run.sh

# Run the shell script as the CMD
CMD ["/bin/bash", "-c", "./run.sh"]

#one container one service celery, beat, 
#iki farklı db oluşturup biri local diğeri proje alanı 
#env diye bir dizin açıp .env diye başka bir dosya bütün secretlar username'ler bunun içerisinde bu dosyayı da github'a atmıyorsun,
#atacaksan da gitsecret gibi şeylerle encrypt edilebilir 

#precommit entegre edilmeli, black, ishort, 
#veriler üzerinde analiz yapıldı mı, hangi domain neyle alakalı, 
#google reklam şeffaflığı, aradığımız urller 