FROM python:3.10-slim

#set environment variables
#prevents python from creating .pyc bytecode files
ENV PYTHONDONTWRITEBYTECODE 1
#prevents output buffering in containers  
ENV PYTHONUNBUFFERED 1

ENV APP_HOME=/app

# set work directory
WORKDIR $APP_HOME

# use system update install system dependencies
# gcc: Installs the GNU Compiler Collection >> needed to build some Python packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

# copy requirements 
COPY requirements.txt .

# install python dependencies from requirements file
RUN pip install --no-cache-dir -r requirements.txt

# copy application code
COPY app app

# Copy pre-populated database
COPY task.db .

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]