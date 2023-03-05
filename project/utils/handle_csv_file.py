import pandas as pd

def get_data_from_csv(csv_file):
    df = pd.read_csv(csv_file, usecols=['ASIN', 'Marketplace', 'Zipcode', 'Brand'])
    asin, marketplace, zipcode, brand  = df['ASIN'].tolist(), df['Marketplace'].tolist(), df['Zipcode'].tolist(), df['Brand'].tolist()
    return asin, marketplace, zipcode, brand