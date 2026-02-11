TASK 3: Cloud-Native Data Processing with Serverless Functions
Step 1: Install Azurite
bashcd ~/cloud-diet-analysis
mkdir task3_serverless
cd task3_serverless

# Install Azurite via npm

sudo npm install -g azurite

# OR run via Docker

docker pull mcr.microsoft.com/azure-storage/azurite
Step 2: Start Azurite
Option A: Direct npm installation:
bash# Start Azurite in the background
azurite --silent --location ~/azurite-data --debug ~/azurite-debug.log &

# Verify it's running

ps aux | grep azurite
Option B: Docker:
bashdocker run -d -p 10000:10000 -p 10001:10001 -p 10002:10002 \
 --name azurite \
 mcr.microsoft.com/azure-storage/azurite

# Verify it's running

docker ps | grep azurite
Take screenshot showing Azurite running
Step 3: Install Azure Storage SDK
bashpip3 install azure-storage-blob --break-system-packages
Step 4: Upload CSV to Azurite
Create upload_to_azurite.py:
pythonfrom azure.storage.blob import BlobServiceClient
import os
from datetime import datetime

print(f"Upload started at: {datetime.now()}")

# Connection string for Azurite (default)

connect_str = (
"DefaultEndpointsProtocol=http;"
"AccountName=devstoreaccount1;"
"AccountKey=Eby8vdM02xNOcqFlErLqDJcm0b9K2zZYPIoOz6rGg3Ew4HqhkVcj3MBo7u8zB5FbLhkLxK4Y8A==;"
"BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
)

# Create BlobServiceClient

blob_service_client = BlobServiceClient.from_connection_string(connect_str)

# Create container

container_name = "datasets"
try:
container_client = blob_service_client.create_container(container_name)
print(f"Container '{container_name}' created successfully")
except Exception as e:
print(f"Container already exists or error: {e}")
container_client = blob_service_client.get_container_client(container_name)

# Upload CSV file

blob_name = "All_Diets.csv"
csv_path = "../task1_analysis/All_Diets.csv"

print(f"\nUploading {blob_name}...")
with open(csv_path, "rb") as data:
blob_client = container_client.upload_blob(
name=blob_name,
data=data,
overwrite=True
)

print(f"✓ Successfully uploaded {blob_name} to Azurite Blob Storage")

# List blobs to verify

print(f"\nBlobs in container '{container_name}':")
blob_list = container_client.list_blobs()
for blob in blob_list:
print(f" - {blob.name} (Size: {blob.size} bytes)")

print(f"\nUpload completed at: {datetime.now()}")
Run the upload:
bashpython3 upload_to_azurite.py
Take screenshot of successful upload
Step 5: Create Serverless Function
Create serverless_function.py:
pythonfrom azure.storage.blob import BlobServiceClient
import pandas as pd
import io
import json
import os
from datetime import datetime

def process_nutritional_data_from_azurite():
"""
Serverless function to process nutritional data from Azurite Blob Storage
"""
print(f"Function started at: {datetime.now()}")
print("="\*60)

    # Connection string for Azurite
    connect_str = (
        "DefaultEndpointsProtocol=http;"
        "AccountName=devstoreaccount1;"
        "AccountKey=Eby8vdM02xNOcqFlErLqDJcm0b9K2zZYPIoOz6rGg3Ew4HqhkVcj3MBo7u8zB5FbLhkLxK4Y8A==;"
        "BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
    )

    try:
        # Step 1: Connect to Blob Storage
        print("\n[1/5] Connecting to Azurite Blob Storage...")
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)

        container_name = 'datasets'
        blob_name = 'All_Diets.csv'

        # Step 2: Download blob
        print(f"[2/5] Downloading blob: {blob_name}...")
        container_client = blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)

        # Download blob content
        stream = blob_client.download_blob().readall()
        print(f"✓ Downloaded {len(stream)} bytes")

        # Step 3: Load into DataFrame
        print("[3/5] Processing CSV data...")
        df = pd.read_csv(io.BytesIO(stream))
        print(f"✓ Loaded {len(df)} recipes")

        # Step 4: Calculate nutritional insights
        print("[4/5] Calculating nutritional insights...")

        # Average macronutrients per diet type
        avg_macros = df.groupby('Diet_type')[['Protein(g)', 'Carbs(g)', 'Fat(g)']].mean()

        # Top 5 protein recipes per diet
        top_protein = df.sort_values('Protein(g)', ascending=False).groupby('Diet_type').head(5)

        # Diet with highest protein
        highest_protein_diet = avg_macros['Protein(g)'].idxmax()
        highest_protein_value = avg_macros['Protein(g)'].max()

        # Most common cuisines per diet
        most_common_cuisines = df.groupby('Diet_type')['Cuisine_type'].agg(
            lambda x: x.mode()[0] if len(x.mode()) > 0 else 'N/A'
        )

        # Prepare results
        results = {
            'timestamp': datetime.now().isoformat(),
            'total_recipes': len(df),
            'average_macronutrients_by_diet': avg_macros.to_dict(),
            'highest_protein_diet': {
                'diet_type': highest_protein_diet,
                'avg_protein_g': float(highest_protein_value)
            },
            'most_common_cuisines': most_common_cuisines.to_dict(),
            'top_protein_recipes': top_protein[['Diet_type', 'Recipe_name', 'Protein(g)']].to_dict('records')[:20]  # First 20
        }

        print(f"✓ Calculated insights for {len(avg_macros)} diet types")

        # Step 5: Save to simulated NoSQL storage
        print("[5/5] Saving to simulated NoSQL database...")

        # Create directory for NoSQL simulation
        os.makedirs('simulated_nosql', exist_ok=True)

        # Save as JSON (simulating NoSQL document database)
        output_path = 'simulated_nosql/nutrition_results.json'
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)

        print(f"✓ Results saved to {output_path}")

        # Print summary
        print("\n" + "="*60)
        print("PROCESSING SUMMARY")
        print("="*60)
        print(f"Total Recipes Analyzed: {results['total_recipes']}")
        print(f"Diet Types: {len(avg_macros)}")
        print(f"Highest Protein Diet: {highest_protein_diet} ({highest_protein_value:.2f}g)")
        print(f"\nResults Location: {output_path}")
        print("="*60)

        print(f"\nFunction completed at: {datetime.now()}")
        return "✓ Data processed and stored successfully"

    except Exception as e:
        error_msg = f"✗ Error processing data: {str(e)}"
        print(error_msg)
        return error_msg

# Run the function

if **name** == "**main**":
result = process_nutritional_data_from_azurite()
print(f"\nFunction Result: {result}")
Run the serverless function:
bashpython3 serverless_function.py
Take screenshots showing:

Function execution with all steps
Date/time timestamp
Successfully saved JSON file

Step 6: View Results
bash# View the results
cat simulated_nosql/nutrition_results.json

# Or format it nicely

python3 -m json.tool simulated_nosql/nutrition_results.json
Step 7: Optional - Create MongoDB Simulation
Install MongoDB (optional):
bash# Install MongoDB
sudo apt install -y mongodb

# Start MongoDB

sudo systemctl start mongodb
sudo systemctl enable mongodb
Create serverless_mongodb.py:
pythonfrom azure.storage.blob import BlobServiceClient
import pandas as pd
import io
from datetime import datetime
from pymongo import MongoClient

def process_to_mongodb():
"""
Process data and store in MongoDB
"""
print(f"MongoDB processing started at: {datetime.now()}")

    # Connect to Azurite (same as before)
    connect_str = (
        "DefaultEndpointsProtocol=http;"
        "AccountName=devstoreaccount1;"
        "AccountKey=Eby8vdM02xNOcqFlErLqDJcm0b9K2zZYPIoOz6rGg3Ew4HqhkVcj3MBo7u8zB5FbLhkLxK4Y8A==;"
        "BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
    )

    # Download and process data
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    container_client = blob_service_client.get_container_client('datasets')
    blob_client = container_client.get_blob_client('All_Diets.csv')
    stream = blob_client.download_blob().readall()
    df = pd.read_csv(io.BytesIO(stream))

    # Calculate insights
    avg_macros = df.groupby('Diet_type')[['Protein(g)', 'Carbs(g)', 'Fat(g)']].mean()

    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['nutrition_db']
    collection = db['diet_analysis']

    # Prepare documents
    documents = []
    for diet_type in avg_macros.index:
        doc = {
            'diet_type': diet_type,
            'avg_protein_g': float(avg_macros.loc[diet_type, 'Protein(g)']),
            'avg_carbs_g': float(avg_macros.loc[diet_type, 'Carbs(g)']),
            'avg_fat_g': float(avg_macros.loc[diet_type, 'Fat(g)']),
            'timestamp': datetime.now()
        }
        documents.append(doc)

    # Insert into MongoDB
    result = collection.insert_many(documents)
    print(f"✓ Inserted {len(result.inserted_ids)} documents into MongoDB")

    # Query and display
    print("\nStored documents:")
    for doc in collection.find():
        print(f"  {doc['diet_type']}: Protein={doc['avg_protein_g']:.2f}g")

    print(f"\nCompleted at: {datetime.now()}")

if **name** == "**main**": # First install: pip3 install pymongo --break-system-packages
process_to_mongodb()

# Step 8: Commit Everything

bashgit add .
git commit -m "Person 2: Task 3 - Serverless Function with Azurite Complete"
git push origin main
