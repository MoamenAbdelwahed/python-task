from pymongo import MongoClient
from infrastructure.config import DATABASE_CONFIG

class MongoRepository:
    def __init__(self, config):
        self.client = MongoClient(
            host=config.host,
            port=config.port,
        )
        self.db = self.client[config.database]

    async def create(self, collection_name, data):
        """Inserts a document into a collection."""
        result = self.db[collection_name].insert_one(data)
        return result.inserted_id

    async def read_all_grayscale(self, collection_name, depth_min=None, depth_max=None):
        """Retrieves all documents from a collection, optionally filtering by depth,
       and normalizes image_data values by dividing them by 255."""

        query = {}
        if depth_min is not None:
            query['depth'] = {'$gte': depth_min}
        if depth_max is not None:
            if 'depth' in query:
                if '$gte' in query['depth']:
                    query['depth']['$lte'] = depth_max
                else:
                    query['depth'] = {'$lte': depth_max}
            else:
                query['depth'] = {'$lte': depth_max}

        cursor = self.db[collection_name].find(query)
        results = []
        for document in cursor:
            normalized_image_data = []
            for inner_list in document['image_data']:
                normalized_inner_list = [value / 255 for value in inner_list]
                normalized_image_data.append(normalized_inner_list)

            results.append({
                "depth": document['depth'],
                "image_data": normalized_image_data
            })
        return results

    async def read_one(self, collection_name, query):
        """Retrieves a single document matching a query."""
        result = self.db[collection_name].find_one(query)
        return result

    async def update(self, collection_name, query, data):
        """Updates a document matching a query."""
        result = self.db[collection_name].update_one(query, {"$set": data})
        return result.modified_count

    async def delete(self, collection_name, query):
        """Deletes a document matching a query."""
        result = self.db[collection_name].delete_one(query)
        return result.deleted_count

MONGO_REPO = MongoRepository(DATABASE_CONFIG)