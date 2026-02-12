import os
import csv
import json
from datetime import datetime
from azure.storage.blob import BlobServiceClient

print(f"Process started at: {datetime.now()}")

# Azurite connection string
connect_str = "UseDevelopmentStorage=true"
blob_service_client = BlobServiceClient.from_connection_string(connect_str)

container_name = "datasets"
blob_name = "All_Diets.csv"
csv_path = os.path.join(os.getcwd(), blob_name)

# ---------------- Upload CSV to Azurite ----------------
try:
    container_client = blob_service_client.create_container(container_name)
    print(f"Container '{container_name}' created successfully")
except Exception:
    container_client = blob_service_client.get_container_client(container_name)
    print(f"Container '{container_name}' already exists")

if not os.path.isfile(csv_path):
    print(f"Error: CSV file not found at {csv_path}")
    exit(1)

print(f"Uploading {blob_name} from {csv_path}...")
with open(csv_path, "rb") as data:
    container_client.upload_blob(name=blob_name, data=data, overwrite=True)
print(f"✓ Successfully uploaded {blob_name} to Azurite")

print(f"\nBlobs in container '{container_name}':")
for blob in container_client.list_blobs():
    print(f" - {blob.name} (Size: {blob.size} bytes)")

# ---------------- Process CSV and save to JSON ----------------
local_csv = "temp_All_Diets.csv"
blob_client = container_client.get_blob_client(blob_name)
with open(local_csv, "wb") as f:
    f.write(blob_client.download_blob().readall())
print(f"Downloaded '{blob_name}' for processing.")

diets = []
with open(local_csv, newline='', encoding='utf-8', errors='replace') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        row["_uploaded_at"] = datetime.now().isoformat()
        diets.append(row)


json_file = "diet_analysis_nosql.json"
if os.path.exists(json_file):
    with open(json_file, "r") as f:
        existing_data = json.load(f)
    diets = existing_data + diets

with open(json_file, "w") as f:
    json.dump(diets, f, indent=4)

print(f"CSV data processed and saved to '{json_file}' successfully!")

print("\nFirst 5 entries:")
for diet in diets[:5]:
    print(diet)

print(f"\nProcess completed at: {datetime.now()}")
