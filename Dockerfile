# Use an official Python runtime as a parent image
FROM python:latest

# Set the working directory in the container
WORKDIR /code

# Copy the requirements file into the container
COPY ./requirements.txt /code/requirements.txt

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the application code into the container
COPY ./app /code/app

# Expose the port the app runs on
EXPOSE 80

CMD ["fastapi", "run", "app/main.py", "--port", "80"]