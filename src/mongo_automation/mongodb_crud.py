from typing import Any
import pandas as pd
from pymongo.mongo_client import MongoClient
import json
from ensure import ensure_annotations




# The `database` class in Python initializes a database object with a specified name and client
# connection, allowing for the creation of collections within that database.
class database:
    def __init__(self, database_name:str, client: MongoClient):
        """
        This Python function initializes a database object with a specified name and client connection.
        
        :param database_name: The `database_name` parameter is a string that represents the name of the
        database you want to work with in MongoDB
        :type database_name: str
        :param client: The `client` parameter in the `__init__` method is expected to be an instance of
        `MongoClient` class. This parameter is used to establish a connection to the MongoDB server and
        interact with the databases and collections within that server
        :type client: MongoClient
        """
        self.name = database_name
        self.database = client[database_name]
        self.collections = {}
        
    def create_collections(self, collection_name:str):
        """
        The `create_collections` function creates a new collection in a database using the provided
        collection name.
        
        :param collection_name: The `collection_name` parameter is a string that represents the name of the
        collection you want to create in the database
        :type collection_name: str
        """
        self.collections[collection_name] = self.database[collection_name]

# The `mongo_db_operation` class provides methods to interact with MongoDB databases, including
# creating databases, inserting records, and bulk inserting data from CSV or Excel files.
class mongo_db_operation:
    def __init__(self, client_url:str):
        """
        The function initializes a MongoDB client using the provided client URL and creates an empty
        dictionary to store databases.
        
        :param client_url: The `client_url` parameter in the `__init__` method is a string that represents
        the URL used to connect to a MongoDB client. This URL is used to create a MongoClient object to
        interact with the MongoDB database
        :type client_url: str
        """
        self.client_url = client_url
        self.client = MongoClient(self.client_url)
        self.databases = {}
        
    def create_database(self, database_name:str):
        """
        The function `create_database` creates a new database object and adds it to a dictionary of
        databases.
        
        :param database_name: The `create_database` method takes in a `database_name` parameter, which is a
        string representing the name of the database to be created
        :type database_name: str
        """
        new_base = database(database_name, self.client)
        self.databases[database_name] = new_base

        
    def insert_record(self, records:dict, collection_name:str, database_name:str):
        """
        The `insert_record` function inserts one or multiple records into a specified collection within a
        database, creating the database and collection if they do not already exist.
        
        :param records: The `records` parameter in the `insert_record` method is expected to be a dictionary
        or a list of dictionaries. The method checks the type of `records` and then inserts the records into
        the specified collection within the specified database. If `records` is a list, it inserts multiple
        records using
        :type records: dict
        :param collection_name: The `collection_name` parameter in the `insert_record` method refers to the
        name of the collection where you want to insert records. It is a string that specifies the
        collection within a database where the records will be stored
        :type collection_name: str
        :param database_name: The `database_name` parameter in the `insert_record` method refers to the name
        of the database where you want to insert records. It is used to identify the specific database
        within which the records will be stored
        :type database_name: str
        """
        if database_name not in self.databases.keys():
            self.create_database(database_name)
        if collection_name not in self.databases[database_name].collections.keys():
            self.databases[database_name].create_collections(collection_name)
        
        if type(records) == list:
            for record in records:
                if type(record) != dict:
                    raise TypeError("Records must be either a dict or a list of dict")
            self.databases[database_name].collections[collection_name].insert_many(records)
        else:
            if type(records) != dict:
                raise TypeError("Records must be either a dict or a list of dict")
            else:
                self.databases[database_name].collections[collection_name].insert_one(records)


    def bulk_insert(self, file_path:str, collection_name:str, database_name:str):
        """
        The function `bulk_insert` reads data from a CSV or Excel file, converts it to JSON format, and
        inserts it into a specified collection in a database.
        
        :param file_path: The `file_path` parameter is a string that represents the file path of the CSV or
        Excel file from which data will be read for bulk insertion into a database
        :type file_path: str
        :param collection_name: The `collection_name` parameter refers to the name of the collection where
        you want to bulk insert the data. In MongoDB, a collection is a group of documents stored in the
        database. When you perform a bulk insert operation, you are inserting multiple documents into the
        specified collection at once
        :type collection_name: str
        :param database_name: The `database_name` parameter in the `bulk_insert` function refers to the name
        of the database where you want to insert the data. This parameter specifies the target database for
        inserting the records from the provided file
        :type database_name: str
        """
        if file_path.endswith('.csv'):
            data = pd.read_csv(file_path, encoding='utf-8')
        elif file_path.endswith('.xlsx'):
            data = pd.read_excel(file_path, encoding='utf-8')
        json_data = data.to_json(orient='record')
        self.insert_record(json_data, collection_name, database_name)
        


