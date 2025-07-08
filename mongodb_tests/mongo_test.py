from pymongo import MongoClient, ReadPreference
from pymongo.errors import ServerSelectionTimeoutError

# client = MongoClient("mongodb://192.168.50.249:27017, 192.168.50.240:27017/?replicaSet=rs0", serverSelectionTimeoutMS=3000)
client = MongoClient("mongodb://192.168.50.249:27017", serverSelectionTimeoutMS=3000)
# client = MongoClient(
#     "mongodb://192.168.50.249:27017,192.168.50.240:27017/?replicaSet=rs0",
#     read_preference=ReadPreference.SECONDARY
# )

try:
    # print(client.server_info())
    # Get or create a database
    db = client["my_new_database"]

    # Get or create a collection
    collection = db["my_collection"]

    # # # Insert a sample document (this actually creates the db/collection)
    # # collection.insert_one({"name": "Meta Partner Engineer", "level": "onsite", "version":"1"})
    # # collection.insert_one({"name": "Meta Partner Engineer", "level": "onsite", "version":"2"})
    # # collection.insert_one({"name": "Meta Partner Engineer", "level": "onsite", "version":"3"})
    # # collection.insert_one({"name": "Meta Partner Engineer", "level": "onsite", "version":"4"})
    # # collection.insert_one({"name": "Meta Partner Engineer", "level": "onsite", "version":"5"})
    # # collection.insert_one({"name": "Meta Partner Engineer", "level": "onsite", "version":"6"})
    # # collection.insert_one({"name": "Meta Partner Engineer", "level": "onsite", "version":"7"})
    # # collection.delete_one({"version":"2"})
    # # collection.create_index([("name", 1), ("version", 1)])

    # # # Find all matching documents
    for doc in collection.find({}):
        print(doc)

    # # List all indexes on the collection
    # # for index in collection.list_indexes():
    # #     print(index)
    
    # Step 1: Aggregate duplicate emails
    # pipeline = [
    #     {
    #         "$group": {
    #             "_id": "$version",
    #             "ids": {"$addToSet": "$_id"},
    #             "count": {"$sum": 1}
    #         }
    #     },
    #     {
    #         "$match": {
    #             "count": {"$gt": 1}
    #         }
    #     }
    # ]

    # duplicates = list(collection.aggregate(pipeline))
    # # print(duplicates)

    # total_deleted = 0

    # for group in duplicates:
    #     ids_to_keep = group["ids"][0]        # keep the first document
    #     ids_to_delete = group["ids"][1:]     # delete the rest
        
    #     if ids_to_delete:
    #         result = collection.delete_many({"_id": {"$in": ids_to_delete}})
    #         total_deleted += result.deleted_count

    # print(f"Deleted {total_deleted} duplicate documents.")

except ServerSelectionTimeoutError as e:
    print("Cannot reach MongoDB server:", e)



