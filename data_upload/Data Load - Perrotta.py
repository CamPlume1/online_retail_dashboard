import pandas as pd
from pymongo import MongoClient

# Step 1: Read Excel file
excel_file = "Online_Retail.xlsx"
df = pd.read_excel(excel_file)

# Step 2: Convert data to list of dictionaries
data = df.to_dict(orient='records')

# Step 3: Connect to MongoDB
client = MongoClient('localhost', 27017)  # Assuming MongoDB is running locally
db = client['OnlineRetail']
collection = db['OnlineRetail']

# Step 4: Insert data into MongoDB
collection.insert_many(data)

print("Data inserted successfully into MongoDB.")