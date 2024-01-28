from dataclasses import dataclass

@dataclass
class MongoConfig:
    host: str = "mongodb"
    port: int = 27017
    database: str = "images"

DATABASE_CONFIG = MongoConfig()