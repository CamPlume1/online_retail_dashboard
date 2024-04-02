# Importing libratries
import data_load
from pymongo import MongoClient
import mongo_api

# Main script
def main():

    # Connect to MongoDB
    client = MongoClient('localhost', 27017)  
    db = client['OnlineRetail']
    collection = db['OnlineRetail']

    # Inserst OnlineRetail Data
    data_load.insert_online_retail_data()

    # Creates vizualization of the given countries spending by month 
    specified_countries = ["Germany", "France", "Australia", "Japan", "Italy"]
    mongo_api.plot_country_spending(specified_countries)
    
if __name__ == '__main__':
    main()