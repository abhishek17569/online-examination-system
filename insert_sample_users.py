from pymongo import MongoClient

MONGODB_URI = "mongodb://localhost:27017/"
DB_NAME = "test_db"
COLLECTION_NAME = "user"

users_data = [
    {
        "name": "John",
        "email": "john.doe@example.com",
        "password": "hashed_password1",
        "role": "admin"
    },
    {
        "name": "Alice",
        "email": "alice.smith@example.com",
        "password": "hashed_password2",
        "role": "student"
    },

]


client = MongoClient(MONGODB_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

result = collection.insert_many(users_data)


print(f"Inserted document IDs: {result.inserted_ids}")

client.close()
