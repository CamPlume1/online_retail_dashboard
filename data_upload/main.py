# Importing libratries
from data_upload import data_load
from pymongo import MongoClient
import backend.api_methods.mongo_api as mongo_api

# Main script
def main():

    # Connect to MongoDB
    client = MongoClient('localhost', 27017)  
    db = client['OnlineRetail']
    collection = db['OnlineRetail']

    # Inserst OnlineRetail Data
    data_load.insert_online_retail_data()

    # Creates vizualization of the given countries spending by month 
    selected_countries = ['United Kingdom', 'France', "Japan"]
    mongo_api.visualize_spending(selected_countries)
    

if __name__ == '__main__':
    main()