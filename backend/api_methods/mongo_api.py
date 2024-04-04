# Importing libraries
from io import BytesIO

import pandas as pd
from pymongo import MongoClient
from sklearn.linear_model import LinearRegression
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
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

    # Remove any country with negative amount for each month
    for month in month_data:
        month_data[month] = {country: amount for country, amount in month_data[month].items() if amount >= 0}

    client.close()

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

    # Save the plot to a BytesIO object
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    plt.close()

    return figfile



def get_unique_countries() -> list[str]:
    '''
    Gets the unique countries
    :return:
    '''
    client = MongoClient('localhost', 27017)
    db = client['OnlineRetail']
    collection = db['OnlineRetail']
    unique_countries = collection.distinct('Country')
    client.close()
    return unique_countries

def get_data(Country):
       # Connect to MongoDB
    client = MongoClient('localhost', 27017)
    db = client['OnlineRetail']
    collection = db['OnlineRetail']
    pipeline = [
        {
            '$match': {
            'Country': Country,
            '$expr': { '$eq': [{ '$year': "$InvoiceDate" }, 2011] }
            }
        },
        {
            '$project': {
            'month': { '$month': "$InvoiceDate" },
            'revenue': { '$multiply': ["$UnitPrice", "$Quantity"] }
            }
        },
        {
            '$group': {
            '_id': "$month" ,
            'totalRevenue': { '$sum': "$revenue" }
            }
        },
        {
            '$sort': { "_id": 1 }
        }
        ]

    # Query the dataset
    result = list(collection.aggregate(pipeline))


    result = pd.DataFrame(result)
    result['Month'] = result['_id'].apply(number_to_month)
    return result



def number_to_month(number):
    months = [
        'January', 'February', 'March', 'April',
        'May', 'June', 'July', 'August',
        'September', 'October', 'November', 'December'
    ]
    return months[number - 1]


def linear_regression(X,y):
    model = LinearRegression()
    model.fit(X.reshape(-1,1), y)
    predictions = model.predict(X)

    return predictions


def gen_country_graphic(Country) -> BytesIO:

    data = get_data(Country)


    if data.empty:
        return "Country Not Found"
    else:
        plt.figure(figsize=(6, 4))
        plt.bar(data['Month'], data['totalRevenue'], width=.8)
        # Add labels and title
        plt.xlabel('Month', fontsize=12)  # Adjust font size
        plt.ylabel('Amount Spent', fontsize=12)  # Adjust font size
        plt.title('Amount Spent in ' + Country + ' (2011)', fontsize=14)  # Adjust font size
        # Rotate x-axis labels if needed
        plt.xticks(rotation=70)  # Rotate labels by 45 degrees
        def format_func(value, tick_number):
            return f'{value/1:.0f}'
        # Set the custom formatter for y-axis tick labels
        plt.gca().yaxis.set_major_formatter(FuncFormatter(format_func))
        # Display the plot
        plt.tight_layout()

        if data.shape[0] > 1:
            x = np.array(data.index.values.reshape(-1,1))
            y = linear_regression(x, data['totalRevenue'].values)
            plt.plot(data.index.values, y, linestyle='dashed', color='blue', linewidth=2.5)




        # Save the plot to a BytesIO object
        figfile = BytesIO()
        plt.savefig(figfile, format='png')
        figfile.seek(0)  # Move the cursor to the beginning of the BytesIO object
        plt.clf()
        plt.close()

        return figfile



def best_selling_products(year) -> BytesIO:
    client = MongoClient('localhost', 27017)
    db = client['OnlineRetail']
    collection = db['OnlineRetail']

    # Da Query
    pipeline = [
        {
            '$match': {
                '$expr': { '$eq': [{ '$year': "$InvoiceDate" }, year] }
            }
        },
        {
            '$project': {
                'Description': 1,
                'Quantity': 1
            }
        },
        {
            '$group': {
                '_id': "$Description",
                'TotalQuantity': { '$sum': "$Quantity" }
            }
        },
        {
            '$sort': { "TotalQuantity": -1 }
        },
        {
            '$limit': 10
        }
    ]
    # Runs query
    results = collection.aggregate(pipeline)

    # Store Result
    data = pd.DataFrame(results)

    # Plot results
    fig, ax = plt.subplots(figsize=(16, 8))

    # Plot the results part II
    ax.bar(data['_id'], data['TotalQuantity'])

    # Add labels and title
    ax.set_xlabel('Product Description')
    ax.set_ylabel('Total Quantity Sold')
    ax.set_title('Top 10 Best Selling Products')

    # Rotate x-axis to look fancy
    plt.xticks(rotation=70)

    # Save the plot
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    plt.close()

    return figfile

