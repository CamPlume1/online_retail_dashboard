# Importing libraries
import pandas as pd
import matplotlib.pyplot as plt
from pymongo import MongoClient

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

    # Remove any country with negative amount for each month
    for month in month_data:
        month_data[month] = {country: amount for country, amount in month_data[month].items() if amount >= 0}

    return month_data

# Given the selected countires, vizualizes their spending by month
def visualize_spending(selected_countries):

    # Extracts data via mongo and returns a dictionary where each month lists the total spending by country
    month_data = spending_by_month_and_country()

    # Sort month_data by month 
    sorted_month_data = dict(sorted(month_data.items()))

    # Create the bar plot
    fig, ax = plt.subplots(figsize=(16, 8)) 
    width = 0.8 / len(sorted_month_data) 

    # Iterate over the months and plot bars for each selected country
    for i, (month, country_data) in enumerate(sorted_month_data.items()):
        selected_country_data = {country: amount for country, amount in country_data.items() if country in selected_countries}
        x = [j + i * width for j in range(len(selected_country_data))]
        ax.bar(x, selected_country_data.values(), width, label=f'Month {month}')

    ax.set_xlabel('Country')
    ax.set_ylabel('Total Amount Spent (USD)')
    ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
    ax.set_title('Online Retail Spending by Month and Country')
    ax.set_xticks([i + 0.4 for i in range(len(selected_countries))]) 
    ax.set_xticklabels(selected_countries)
    ax.legend()

    plt.show()

