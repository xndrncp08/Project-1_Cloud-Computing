# Use official Python image
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy script and dataset
COPY data_analysis.py .
COPY All_Diets.csv .

# Output folder
RUN mkdir -p /app/output

# Headless matplotlib
ENV MPLBACKEND=Agg

# Run the analysis
CMD ["python", "data_analysis.py"]
