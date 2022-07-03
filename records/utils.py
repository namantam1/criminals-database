import pymongo
from django.core.files.storage import default_storage
from django.conf import settings

client = pymongo.MongoClient(settings.MONGO_URL)
database = settings.MONGO_DATABASE

collection = "Encodings"
threshold = 0.6
k = 10

db = client[database]


def upload_img(img, path="images/"):
    img.seek(0)
    res = default_storage.save(path + str(img), img)
    return default_storage.url(res)

def save_embeddings(ref_no, image_uri, name, embeddings=[]):
    db[collection].insert_many(
        list(
            map(
                lambda embedding: {
                    "ref_no": ref_no,
                    "name": name,
                    "image_uri": image_uri,
                    "embedding": list(embedding),
                },
                embeddings,
            )
        )
    )


def find_data(embedding):
    query = db[collection].aggregate(
        [
            {"$addFields": {"target_embedding": embedding}},
            {"$unwind": {"path": "$embedding", "includeArrayIndex": "embedding_index"}},
            {
                "$unwind": {
                    "path": "$target_embedding",
                    "includeArrayIndex": "target_index",
                }
            },
            {
                "$project": {
                    "ref_no": 1,
                    "image_uri": 1,
                    "name": 1,
                    "embedding": 1,
                    "target_embedding": 1,
                    "compare": {"$cmp": ["$embedding_index", "$target_index"]},
                }
            },
            {"$match": {"compare": 0}},
            {
                "$group": {
                    "_id": {
                        "ref_no": "$ref_no",
                        "image_uri": "$image_uri",
                        "name": "$name",
                    },
                    "distance": {
                        "$sum": {
                            "$pow": [
                                {"$subtract": ["$embedding", "$target_embedding"]},
                                2,
                            ]
                        }
                    },
                }
            },
            {
                "$project": {
                    "_id": 1,
                    "distance": {"$sqrt": "$distance"},
                }
            },
            {
                "$project": {
                    "_id": 1,
                    "distance": 1,
                    "cond": {"$lte": ["$distance", threshold]},
                }
            },
            {"$match": {"cond": True}},
            {"$sort": {"distance": 1}},
            {"$limit": k},
        ]
    )
    return query

def get_imgs(ref_no):
    return list(db[collection].find(dict(ref_no=ref_no)))

def delete_imgs(ref_no):
    return db[collection].delete_many({"ref_no": ref_no}).deleted_count
