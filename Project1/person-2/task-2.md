Person 2: Containerization & Serverless (Task 2 + Task 3)
TASK 2: Dockerizing the Data Processing Application
Step 1: Prepare the Application
bashcd ~/cloud-diet-analysis
mkdir task2_docker
cd task2_docker

# Copy the analysis script from Person 1

cp ../task1_analysis/data_analysis.py .
cp ../task1_analysis/All_Diets.csv .
Step 2: Create Requirements File
Create requirements.txt:
bashcode requirements.txt
Add:
pandas
matplotlib
seaborn
numpy
Step 3: Create Dockerfile
Create Dockerfile:
bashcode Dockerfile
Add the following:
dockerfile# Use official Python runtime as base image
FROM python:3.9-slim

# Set working directory in container

WORKDIR /app

# Install system dependencies

RUN apt-get update && apt-get install -y \
 gcc \
 && rm -rf /var/lib/apt/lists/\*

# Copy requirements first (for better layer caching)

COPY requirements.txt .

# Install Python dependencies

RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application

COPY data_analysis.py .
COPY All_Diets.csv .

# Create output directory

RUN mkdir -p /app/output

# Set environment variable for matplotlib (headless mode)

ENV MPLBACKEND=Agg

# Run the analysis script

CMD ["python", "data_analysis.py"]
Step 4: Build the Docker Image
bash# Build the image
docker build -t diet-analysis:v1.0 .

# Verify the image was created

docker images | grep diet-analysis
Take screenshot showing the build process and successful completion
Step 5: Run the Container Locally
bash# Run the container
docker run --name diet-analysis-test diet-analysis:v1.0

# Check logs

docker logs diet-analysis-test

# Copy output files from container

docker cp diet-analysis-test:/app/processed_diets.csv ./output_processed_diets.csv

# Clean up

docker rm diet-analysis-test
Take screenshot showing:

Container running successfully
Output logs with date/time
Extracted files

Step 6: Push to Docker Hub
bash# Login to Docker Hub
docker login

# Enter your username and password

# Tag the image for Docker Hub

docker tag diet-analysis:v1.0 YOUR_DOCKERHUB_USERNAME/diet-analysis:v1.0

# Push to Docker Hub

docker push YOUR_DOCKERHUB_USERNAME/diet-analysis:v1.0
Take screenshot of successful push
Step 7: Create Docker Compose Configuration
Create docker-compose.yml:
bashcode docker-compose.yml
Add:
yamlversion: '3.8'

services:
diet-analysis:
image: diet-analysis:v1.0
container_name: diet-analysis-app
volumes: - ./output:/app/output
environment: - MPLBACKEND=Agg
command: python data_analysis.py

# Optional: Add a simple web server to view results

results-viewer:
image: nginx:alpine
container_name: results-nginx
ports: - "8080:80"
volumes: - ./output:/usr/share/nginx/html
depends_on: - diet-analysis
Step 8: Test Docker Compose
bash# Create output directory
mkdir -p output

# Run with Docker Compose

docker-compose up

# In another terminal, verify

docker-compose ps

# Stop services

docker-compose down
Take screenshot of docker-compose running
Step 9: Commit to GitHub
bashgit add Dockerfile requirements.txt docker-compose.yml

# Push to github

git commit -m "Person 2: Task 2 - Dockerization Complete"
git push origin main
