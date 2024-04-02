# Importing libraries
import pandas as pd
import matplotlib.pyplot as plt
from pymongo import MongoClient
import numpy as np

# Extracts data via mongo and returns a dictionary where each month lists the total spending by country 
def spending_by_month_and_country():

    # Connect to MongoDB
    client = MongoClient('localhost', 27017) 
    db = client['OnlineRetail']
    collection = db['OnlineRetail']

    # Cypher Query 
    pipeline = [
        {"$project": {
            "Month": {"$month": "$InvoiceDate"},
            "Country": 1,
            "TotalAmount": {"$multiply": ["$Quantity", "$UnitPrice"]}
        }},
        {"$group": {
            "_id": {"Month": "$Month", "Country": "$Country"},
            "TotalAmount": {"$sum": "$TotalAmount"}
        }}
    ]

    # Runs cypher query
    results = collection.aggregate(pipeline)

    # Generates Result in dataframe 
    data = pd.DataFrame(results)

    # Extract 'Month', 'Country', and 'TotalAmount' from '_id' field
    data[['Month', 'Country']] = pd.DataFrame(data['_id'].tolist())
    data.drop('_id', axis=1, inplace=True)
    months = data['Month'].tolist()
    countries = data['Country'].tolist()
    data['TotalAmount'] = data['TotalAmount'].round()
    total_amounts = data['TotalAmount'].tolist()

    # Create a dictionary to store total amount spent by country for each month
    month_data = {}
    for month, country, amount in zip(months, countries, total_amounts):
        if month not in month_data:
            month_data[month] = {}
        if country not in month_data[month]:
            month_data[month][country] = amount
        else:
            month_data[month][country] += amount

    # Sort month_data by month 
    month_data = dict(sorted(month_data.items()))

    # Changes month from number to the month's actual name  
    month_sales = {}
    month_sales['January'] = month_data.get(1)
    month_sales['February'] = month_data.get(2)
    month_sales['March'] = month_data.get(3)
    month_sales['April'] = month_data.get(4)
    month_sales['May'] = month_data.get(5)
    month_sales['June'] = month_data.get(6)
    month_sales['July'] = month_data.get(7)
    month_sales['August'] = month_data.get(8)
    month_sales['September'] = month_data.get(9)
    month_sales['October'] = month_data.get(10)
    month_sales['November'] = month_data.get(11)
    month_sales['December'] = month_data.get(12)

    return month_sales

# Given the selected countires, vizualizes their spending by month
def plot_country_spending(specified_countries):

    # Gets cypher queried data as a dictionary and coverst to a data frame
    data = spending_by_month_and_country()
    df = pd.DataFrame(data).T

    # Vizualization
    plt.figure(figsize=(12, 8))

    # Plot data for each country that is apart of the specified list 
    for country in specified_countries:
        if country in df.columns:
            plt.plot(df.index, df[country], label=country)

    # Add labels, title, and legend 
    plt.xlabel('Month')
    plt.ylabel('Amount Spent')
    plt.title('Amount Spent by Country per Month')
    plt.legend()

    # Show plot
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()