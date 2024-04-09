from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from io import BytesIO
from datetime import datetime
import matplotlib.dates as mdates


def get_time_series_data(country: str, year: int):
    client = MongoClient('localhost', 27017)
    db = client['OnlineRetail']
    collection = db['OnlineRetail']
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31)
    pipeline = [
        {
            '$match': {
                'Country': country,
                'InvoiceDate': {
                    '$gte': start_date,
                    '$lte': end_date
                }
            }
        },
        {
            '$project': {
                'YearMonth': {
                    '$dateToString': {'format': "%Y-%m", 'date': "$InvoiceDate"}
                },
                'Quantity': "$Quantity"
            }
        },
        {
            '$group': {
                '_id': "$YearMonth",
                'TotalQuantity': {'$sum': "$Quantity"}
            }
        },
        {
            '$sort': {'_id': 1}
        }
    ]

    result = list(collection.aggregate(pipeline))
    client.close()

    # Transform the result into a pandas DataFrame
    result_df = pd.DataFrame(result)
    result_df['YearMonth'] = pd.to_datetime(result_df['_id'])
    result_df.drop('_id', axis=1, inplace=True)
    result_df.sort_values('YearMonth', inplace=True)
    return result_df


def gen_time_series_graphic(country: str, year: int) -> BytesIO:
    data = get_time_series_data(country, year)

    if data.empty:
        return "No data available in the dataset."

    plt.figure(figsize=(14, 7))
    plt.plot(data['YearMonth'], data['TotalQuantity'], marker='o')

    # Adding plot title and labels
    plt.title(f'Monthly Quantity Sold in {country} for the Year {year}')
    plt.xlabel('Month')
    plt.ylabel('Total Quantity')
    plt.grid(True)

    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%B'))  # %B for full month name, %b for abbreviated

    plt.xticks(rotation=45)  # Rotate for better readability

    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    plt.close()
    return figfile
