from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv("MONGO_URI")
print("URI:", uri)   # 👈 DEBUG LINE

client = MongoClient(uri, serverSelectionTimeoutMS=5000)

try:
    client.server_info()
    print("MongoDB Connected ✅")
except Exception as e:
    print("Connection Failed ❌", e)

db = client["blood_bank_system"]

blood_inventory = db["blood_inventory"]
blood_banks = db["blood_banks"]
donors = db["donors"]
requests = db["requests"]