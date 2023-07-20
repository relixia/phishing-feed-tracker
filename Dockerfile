# Base image
FROM python:3.10.9

# Set the working directory in the container
WORKDIR /app

# Copy the project files to the working directory
COPY . /app

# Install project dependencies
RUN pip install -r requirements.txt
# pip install poetry, sonraki starıda run install poetry gibi gibi

# Add a shell script for running multiple commands
RUN echo '#!/bin/bash\n\
    redis-server &\n\
    celery -A tasks worker --loglevel=info --concurrency=4 &\n\
    python3 main.py' > run.sh
RUN chmod +x run.sh

# Run the shell script as the CMD
CMD ["/bin/bash", "-c", "./run.sh"]
