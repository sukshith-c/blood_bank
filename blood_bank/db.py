from pymongo import MongoClient

client = MongoClient("mongodb+srv://sukshithc24cs_db_user:Sukshith123@cluster-1.jjhajhp.mongodb.net/")

db = client["blood_bank_system"]

collection = db["blood_inventory"]