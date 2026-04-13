import os
from pymongo import MongoClient

# MongoDB से कनेक्ट करने का फंक्शन
def get_db():
    mongo_uri = os.environ.get("MONGO_URI")
    client = MongoClient(mongo_uri)
    return client.telegram_bot_db

# स्क्रिप्ट को सेव करने का फंक्शन
def save_script(user_name, user_id, username, choices, script_text):
    db = get_db()
    collection = db.scripts
    data = {
        "user_name": user_name,
        "user_id": user_id,
        "username": username,
        "category": choices.get('category'),
        "tone": choices.get('tone'),
        "language": choices.get('language'),
        "format": choices.get('format'),
        "audience": choices.get('audience'),
        "duration": choices.get('duration'),
        "topic": choices.get('topic'),
        "script": script_text
    }
    collection.insert_one(data)

# डैशबोर्ड के लिए सारी स्क्रिप्ट्स लाने का फंक्शन
def get_all_scripts(category_filter=None):
    db = get_db()
    collection = db.scripts
    query = {}
    if category_filter:
        query['category'] = category_filter
    # नई स्क्रिप्ट्स पहले दिखें इसलिए -1
    return list(collection.find(query).sort("_id", -1))

# स्क्रिप्ट डिलीट करने का फंक्शन
def delete_script_by_id(script_id):
    db = get_db()
    collection = db.scripts
    from bson.objectid import ObjectId
    collection.delete_one({"_id": ObjectId(script_id)})
