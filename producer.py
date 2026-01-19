import time
import json
import requests
from google.cloud import storage
from datetime import datetime

BUCKET_NAME = "trinhducan-spark-483410"
FOLDER_NAME = "raw_data"

# Initialize GCS Client
storage_client = storage.Client()
bucket = storage_client.bucket(BUCKET_NAME)

# API COINGECKO
# Get price of the 5: Bitcoin, Ethereum, Tether, BNB, Solana
API_URL = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,tether,binancecoin,solana&vs_currencies=usd&include_last_updated_at=true"

print(f"Start uploading data to: gs://{BUCKET_NAME}/{FOLDER_NAME}/")

while True:
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            data = response.json()
            records = []
            for coin, info in data.items():
                # Check if 'info' is a dictionary containing prices.
                # If API returns an error (info is string), we ignore it.
                if not isinstance(info, dict) or 'usd' not in info:
                    print(f"⚠️ Unusual data (ignore): {coin} -> {info}")
                    continue

                record = {
                    "symbol": coin.upper(),
                    "priceUsd": float(info['usd']),
                    "timestamp": datetime.now().isoformat()
                }
                records.append(record)
            if records: # Only upload if a valid record exists
                file_name = f"coins_{int(time.time())}.json"
                blob_path = f"{FOLDER_NAME}/{file_name}"
                
                blob = bucket.blob(blob_path)
                # Convert to NDJSON (one object per line)
                data_str = "\n".join([json.dumps(r) for r in records])
                
                blob.upload_from_string(data_str, content_type='application/json')
                print(f"✅ Upload finished: {blob_path} ({len(records)} coins)")
            else:
                print("⚠️ No valid coin prices were obtained..")
        else:
            print(f"❌ Error API: {response.status_code}")
                    
        time.sleep(60)
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(30)