
from io import BytesIO
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
import pandas as pd
from pymongo import MongoClient
from sklearn.linear_model import LinearRegression

class dashboard_api:
    
    def __init__(self, host='localhost', port=27017, db_name='OnlineRetail', collection='OnlineRetail'):
        self.client = MongoClient(host, port)
        print(db_name)
        self.db = self.client[db_name]
        self.collection = self.db[collection]
        self.connections = {}

    def get_data(self, Country):
         
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
        result = list(self.collection.aggregate(pipeline))  

      
        result = pd.DataFrame(result)
        result['Month'] = result['_id'].apply(self.number_to_month)
        return result

    
    
    def number_to_month(self, number):
        months = [
            'January', 'February', 'March', 'April',
            'May', 'June', 'July', 'August',
            'September', 'October', 'November', 'December'
        ]
        return months[number - 1]
    

    def linear_regression(self, X,y):
        model = LinearRegression()
        model.fit(X.reshape(-1,1), y)
        predictions = model.predict(X)

        return predictions
    
    
    def gen_graphic(self, Country) -> BytesIO:

        data = self.get_data(Country)

        
        if data.empty:
            return "Country Not Found"
        else:            
            plt.figure(figsize=(8, 6))
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
                y = self.linear_regression(x, data['totalRevenue'].values)
                plt.plot(data.index.values, y, linestyle='dashed', color='blue', linewidth=2.5)
            
            
            

            # Save the plot to a BytesIO object
            figfile = BytesIO()
            plt.savefig(figfile, format='png')
            figfile.seek(0)  # Move the cursor to the beginning of the BytesIO object
            plt.clf()
            plt.close()

            return figfile


