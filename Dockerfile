# Stage 1: Build Stage
FROM python:latest AS build

RUN apt update -y && apt upgrade -y
RUN apt install nano net-tools

# Set the working directory in the container
WORKDIR /code

# Copy the requirements file into the container
COPY ./requirements.txt /code/requirements.txt

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the application code into the container
COPY ./app /code/app

# Stage 2: Runtime Stage
FROM python:latest AS runtime
# Set the working directory in the container
WORKDIR /code

# Copy only the installed packages from the build stage
COPY --from=build /usr/local /usr/local

# Copy the application code from the build stage
COPY --from=build /code/app /code/app

# Expose the port the app runs on
EXPOSE 80

# Command to run the application
CMD ["fastapi", "run", "app/main.py", "--port", "80"]
