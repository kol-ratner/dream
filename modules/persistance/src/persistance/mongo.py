from dataclasses import dataclass
from typing import Optional
from pymongo import MongoClient as PyMongoClient
from pymongo.database import Database
from pymongo.collection import Collection

@dataclass
class MongoConfig:
    host: str
    user: str
    password: str
    database: str
    collection: str
    replicaset: str
    authSource: str = "admin"
    authMechanism: str = "SCRAM-SHA-256"
    port: int = 27017

@dataclass 
class MongoClient:
    config: MongoConfig
    client: Optional[PyMongoClient] = None
    db: Optional[Database] = None
    
    def setup_connection(self) -> 'MongoClient':
        self.client = PyMongoClient(
            host=self.config.host,
            port=self.config.port,
            username=self.config.user,
            password=self.config.password,
            authSource=self.config.authSource,
            authMechanism=self.config.authMechanism,
            replicaset=self.config.replicaset   
        )
        self.db = self.client[self.config.database]
        self.collection = self.db[self.config.collection]
        return self
    