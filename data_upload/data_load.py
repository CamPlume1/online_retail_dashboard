import pandas as pd
from pymongo import MongoClient

# Insterst OnlineRetail data into Mongo DB
def insert_online_retail_data():
    # If data base doesn't exists 
    client = MongoClient('localhost', 27017) 
    if 'OnlineRetail' not in client.list_database_names():

        # Read data 
        excel_file = "../data/Online_Retail.xlsx"
        df = pd.read_excel(excel_file)

        # Convert data to list of dictionaries
        data = df.to_dict(orient='records')

        # Connect to MongoDB and create database and collection
        db = client['OnlineRetail']
        collection = db['OnlineRetail']

        # Insert data into MongoDB
        collection.insert_many(data)

        print("Data inserted successfully into MongoDB.")

        # If data base doesn't exists 
    else:
        print("Database 'OnlineRetail' already exists.")