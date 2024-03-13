import pandas as pd
from pymongo.mongo_client import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from typing import Dict
from typing import Any


class database:
    def __init__(self, database_name: str, client: MongoClient):
        """
        Initializes a database object with a specified name and client connection.

        :param database_name: The name of the database.
        :type database_name: str
        :param client: The MongoClient object used to establish a connection to the MongoDB server.
        :type client: MongoClient
        """
        self.name = database_name
        self.database: Database = client[database_name]
        self.collections: Dict[str, Any] = {}

    def create_collections(self, collection_name: str):
        """
        Creates a new collection in the database with the specified name.

        :param collection_name: The name of the collection to be created.
        :type collection_name: str
        """
        coll: Collection = self.database[collection_name]
        self.collections[collection_name] = coll


class mongo_db_operation:
    def __init__(self, client_url: str):
        """
        Initializes a MongoDB client with the provided client URL and creates an empty dictionary to store databases.

        :param client_url: The URL used to connect to the MongoDB client.
        :type client_url: str
        """
        self.client_url = client_url
        self.client: MongoClient = MongoClient(self.client_url)
        self.databases: Dict[str, database] = {}

    def create_database(self, database_name: str):
        """
        Creates a new database object and adds it to the dictionary of databases.

        :param database_name: The name of the database to be created.
        :type database_name: str
        """
        new_base = database(database_name, self.client)
        self.databases[database_name] = new_base

    def insert_record(self, records: dict, collection_name: str, database_name: str):
        """
        Inserts one or multiple records into a specified collection within a database, creating the database and collection 
if they do not already exist.

        :param records: The record(s) to be inserted into the collection.
        :type records: dict or list of dicts
        :param collection_name: The name of the collection where the records will be inserted.
        :type collection_name: str
        :param database_name: The name of the database where the records will be inserted.
        :type database_name: str
        """
        if database_name not in self.databases.keys():
            self.create_database(database_name)
        if collection_name not in self.databases[database_name].collections.keys():
            self.databases[database_name].create_collections(collection_name)

        if isinstance(records, list):
            for record in records:
                if not isinstance(record, dict):
                    raise TypeError("Records must be either a dict or a list of dict")
            self.databases[database_name].collections[collection_name].insert_many(records)
        else:
            if not isinstance(records, dict):
                raise TypeError("Records must be either a dict or a list of dict")
            else:
                self.databases[database_name].collections[collection_name].insert_one(records)

    def bulk_insert(self, file_path: str, collection_name: str, database_name: str):
        """
        Reads data from a CSV or Excel file, converts it to JSON format, and inserts it into a 
specified collection in a database.

        :param file_path: The path to the CSV or Excel file containing the data to be inserted.
        :type file_path: str
        :param collection_name: The name of the collection where the data will be inserted.
        :type collection_name: str
        :param database_name: The name of the database where the data will be inserted.
        :type database_name: str
        """
        if file_path.endswith('.csv'):
            data = pd.read_csv(file_path, encoding='utf-8')
        elif file_path.endswith('.xlsx'):
            data = pd.read_excel(file_path, encoding='utf-8')
        json_data = data.to_json(orient='records')
        self.insert_record(json_data, collection_name, database_name)
