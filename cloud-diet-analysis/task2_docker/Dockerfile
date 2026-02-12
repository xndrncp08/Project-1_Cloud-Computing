FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY data_analysis.py .
COPY All_Diets.csv .

RUN mkdir -p /app/output

ENV MPLBACKEND=Agg

CMD ["python", "data_analysis.py"]
