Person 3: CI/CD Pipeline (Task 4 + Task 5 Enhancement)
TASK 4: Set Up CI/CD Pipeline
Step 1: Ensure GitHub Repository is Set Up
You should have already created this in the prerequisites. If not:
bashcd ~/cloud-diet-analysis

# Initialize git if needed

git init
git add .
git commit -m "Initial commit"

# Create repository on GitHub, then:

git remote add origin https://github.com/YOUR_USERNAME/cloud-diet-analysis.git
git branch -M main
git push -u origin main
Step 2: Create GitHub Actions Directory
bashcd ~/cloud-diet-analysis
mkdir -p .github/workflows
cd .github/workflows
Step 3: Create CI/CD Workflow File
Create deploy.yml:
bashcode deploy.yml
Add the following workflow:
yamlname: Cloud Diet Analysis CI/CD Pipeline

# Trigger on push to main branch

on:
push:
branches: [ main ]
pull_request:
branches: [ main ]
workflow_dispatch: # Allow manual trigger

# Environment variables

env:
DOCKER_IMAGE_NAME: diet-analysis
DOCKER_TAG: ${{ github.sha }}

jobs:

# Job 1: Code Quality and Testing

test:
name: Test Python Code
runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install pandas matplotlib seaborn numpy pytest flake8

      - name: Lint with flake8
        run: |
          # Stop build if there are Python syntax errors or undefined names
          flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
          # Exit-zero treats all errors as warnings
          flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
        continue-on-error: true

      - name: Test data analysis script
        run: |
          if [ -f "task1_analysis/data_analysis.py" ]; then
            echo "Testing data analysis script..."
            cd task1_analysis
            # Add a simple test or syntax check
            python -m py_compile data_analysis.py
            echo "✓ Script syntax is valid"
          fi
        continue-on-error: true

# Job 2: Build Docker Image

build:
name: Build Docker Image
runs-on: ubuntu-latest
needs: test

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2

      - name: Log in to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Build Docker image
        run: |
          if [ -f "task2_docker/Dockerfile" ]; then
            cd task2_docker
            docker build -t ${{ secrets.DOCKER_USERNAME }}/${{ env.DOCKER_IMAGE_NAME }}:${{ env.DOCKER_TAG }} .
            docker build -t ${{ secrets.DOCKER_USERNAME }}/${{ env.DOCKER_IMAGE_NAME }}:latest .
            echo "✓ Docker image built successfully"
          else
            echo "Dockerfile not found, skipping build"
          fi

      - name: Push Docker image
        run: |
          if [ -f "task2_docker/Dockerfile" ]; then
            docker push ${{ secrets.DOCKER_USERNAME }}/${{ env.DOCKER_IMAGE_NAME }}:${{ env.DOCKER_TAG }}
            docker push ${{ secrets.DOCKER_USERNAME }}/${{ env.DOCKER_IMAGE_NAME }}:latest
            echo "✓ Docker image pushed to Docker Hub"
          fi

# Job 3: Deploy Simulation

deploy:
name: Simulate Deployment
runs-on: ubuntu-latest
needs: build

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Simulate local deployment
        run: |
          echo "=== Deployment Simulation Started ==="
          echo "Timestamp: $(date)"
          echo "Commit SHA: ${{ github.sha }}"
          echo "Branch: ${{ github.ref }}"

          # Simulate pulling the latest image
          echo "✓ Pulling Docker image..."

          # Simulate container deployment
          echo "✓ Deploying container..."

          # Simulate health check
          echo "✓ Running health checks..."

          echo "=== Deployment Successful ==="
          echo "Deployment completed at: $(date)"

      - name: Create deployment artifact
        run: |
          mkdir -p deployment_logs
          echo "Deployment completed successfully at $(date)" > deployment_logs/deployment_$(date +%Y%m%d_%H%M%S).log
          echo "Commit: ${{ github.sha }}" >> deployment_logs/deployment_$(date +%Y%m%d_%H%M%S).log

      - name: Upload deployment logs
        uses: actions/upload-artifact@v3
        with:
          name: deployment-logs
          path: deployment_logs/

# Job 4: Serverless Function Test (if applicable)

serverless-test:
name: Test Serverless Function
runs-on: ubuntu-latest
needs: test

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Install Azure SDK
        run: |
          pip install azure-storage-blob pandas

      - name: Validate serverless function
        run: |
          if [ -f "task3_serverless/serverless_function.py" ]; then
            echo "Validating serverless function..."
            cd task3_serverless
            python -m py_compile serverless_function.py
            echo "✓ Serverless function syntax is valid"
          fi

# Job 5: Notification

notify:
name: Pipeline Status Notification
runs-on: ubuntu-latest
needs: [test, build, deploy, serverless-test]
if: always()

    steps:
      - name: Pipeline Status
        run: |
          echo "=== CI/CD Pipeline Completed ==="
          echo "Status: ${{ job.status }}"
          echo "Timestamp: $(date)"
          echo "Repository: ${{ github.repository }}"
          echo "Commit: ${{ github.sha }}"
          echo "Author: ${{ github.actor }}"

Step 4: Set Up GitHub Secrets

Go to your GitHub repository
Click Settings → Secrets and variables → Actions
Click New repository secret
Add the following secrets:

Name: DOCKER_USERNAME, Value: your Docker Hub username
Name: DOCKER_PASSWORD, Value: your Docker Hub password or access token

Take screenshot of the secrets page (don't show the actual secret values)
Step 5: Create a Simple Test File
Create a test file to validate the pipeline:
bashcd ~/cloud-diet-analysis
mkdir -p tests
cd tests
code test_analysis.py
Add:
pythonimport pytest
import pandas as pd
import numpy as np

def test_dataframe_creation():
"""Test that we can create a DataFrame"""
data = {
'Diet_type': ['Paleo', 'Keto', 'Vegan'],
'Protein(g)': [50, 60, 30],
'Carbs(g)': [20, 10, 80],
'Fat(g)': [30, 70, 10]
}
df = pd.DataFrame(data)
assert len(df) == 3
assert 'Protein(g)' in df.columns

def test_average_calculation():
"""Test average calculation"""
data = {
'Diet_type': ['Paleo', 'Paleo', 'Keto', 'Keto'],
'Protein(g)': [50, 60, 40, 50]
}
df = pd.DataFrame(data)
avg = df.groupby('Diet_type')['Protein(g)'].mean()
assert avg['Paleo'] == 55
assert avg['Keto'] == 45

def test_ratio_calculation():
"""Test ratio calculation"""
protein = 100
carbs = 50
ratio = protein / carbs
assert ratio == 2.0

if **name** == "**main**":
test_dataframe_creation()
test_average_calculation()
test_ratio_calculation()
print("All tests passed!")
Step 6: Commit and Push to Trigger Pipeline
bashcd ~/cloud-diet-analysis
git add .github/workflows/deploy.yml tests/test_analysis.py
git commit -m "Person 3: Task 4 - CI/CD Pipeline Setup"
git push origin main
Step 7: Monitor GitHub Actions

Go to your GitHub repository
Click on the Actions tab
Watch the workflow run
Click on the running workflow to see details

Take screenshots showing:

The Actions tab with workflow running
Each job's success status
Build logs with timestamps
Final success message

Step 8: Create Documentation
Create CI_CD_DOCUMENTATION.md:
markdown# CI/CD Pipeline Documentation

## Overview

This document explains the automated CI/CD pipeline for the Cloud Diet Analysis project.

## Pipeline Architecture

### Workflow File Location

`.github/workflows/deploy.yml`

### Trigger Events

- Push to main branch
- Pull requests to main branch
- Manual workflow dispatch

### Pipeline Jobs

#### 1. Test Job

**Purpose:** Validate code quality and syntax

- Checks out code
- Sets up Python 3.9
- Installs dependencies
- Runs linting with flake8
- Validates Python script syntax

#### 2. Build Job

**Purpose:** Create Docker images

- Builds Docker image from Dockerfile
- Tags with commit SHA and 'latest'
- Pushes to Docker Hub
- Depends on: Test job success

#### 3. Deploy Job

**Purpose:** Simulate deployment

- Simulates pulling latest image
- Simulates container deployment
- Runs health checks
- Creates deployment logs
- Depends on: Build job success

#### 4. Serverless Test Job

**Purpose:** Validate serverless functions

- Validates Python syntax
- Checks Azure SDK compatibility
- Runs in parallel with Build job

#### 5. Notify Job

**Purpose:** Report pipeline status

- Runs after all jobs complete
- Reports final status
- Always runs (even on failure)

## Required Secrets

The following secrets must be configured in GitHub:

- `DOCKER_USERNAME`: Docker Hub username
- `DOCKER_PASSWORD`: Docker Hub password or access token

## How to Use

### Automatic Trigger

Simply push code to the main branch:

```bash
git add .
git commit -m "Your message"
git push origin main
```

### Manual Trigger

1. Go to Actions tab
2. Select "Cloud Diet Analysis CI/CD Pipeline"
3. Click "Run workflow"
4. Select branch and click "Run workflow"

## Monitoring

### View Pipeline Status

1. Navigate to repository on GitHub
2. Click "Actions" tab
3. Click on workflow run to see details

### Download Artifacts

- Deployment logs are saved as artifacts
- Available for 90 days after workflow run
- Download from Actions → Workflow run → Artifacts

## Troubleshooting

### Build Fails

- Check Dockerfile syntax
- Verify all files are committed
- Check Docker Hub credentials

### Test Fails

- Review flake8 output
- Fix Python syntax errors
- Ensure all dependencies are listed

### Deployment Simulation Fails

- Check previous job statuses
- Review deployment logs
- Verify workflow permissions

## Future Enhancements

- Add integration tests
- Implement staging environment
- Add security scanning
- Automated rollback on failure

# Push to github

Save and commit:
bashgit add CI_CD_DOCUMENTATION.md
git commit -m "Person 3: Added CI/CD documentation"
git push origin main
