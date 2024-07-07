import pandas as pd
from app.mongo_models import Keyword
import datetime

async def save_keywords_to_mongo(mongo_db, keywords_df):
    try:
        # Add created at and updated at columns
        now = datetime.datetime.now()
        keywords_df["created_at"] = now.isoformat()
        keywords_df["updated_at"] = now.isoformat()
        # Convert the dataframe to dictionary
        data = keywords_df.to_dict(orient="records")

        # Validate and save items to MongoDB
        keywords_objs = []
        for keyword in data:
            try:
                item_obj = Keyword(**keyword)
                keywords_objs.append(item_obj.model_dump(exclude=["id"]))
            except Exception as e:
                raise ValueError(f"Failed to validate keyword: {e}")        
        # Insert the data into the MongoDB collection
        await mongo_db.keywords.insert_many(keywords_objs)
        print("Keywords saved to MongoDB")
        return True
    except Exception as e:
        raise ValueError(f"Failed to save keywords to MongoDB: {e}")
    
async def keywords_by_landscape(mongo_db, landscape_id):
    try:
        query = {"landscape_id": landscape_id}
        projection = {"_id": 1}
        documents = await mongo_db.keywords.find(query, projection).to_list(None)
        # Remove the _ids and convert the documents to a list of strings
        keywords = [str(doc["_id"]) for doc in documents]
        return keywords
    except Exception as e:
        raise ValueError(f"Failed to fetch keywords from MongoDB: {e}")