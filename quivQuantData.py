import yfinance as yf
import pandas as pd
from pathlib import Path
import quiverquant

key = "https://api.quiverquant.com"
quiver = quiverquant.quiver(key)


# df = quiver.congress_trading()
# df.to_csv('quiverDF.csv', index=False)
df = pd.read_csv('quiverDF.csv')
# df = df[df['TransactionDate'] >= '2024-01-01']
print(df)
tracker = {}

alist = []
for index, row in df.iterrows():
    try:
        print(row)
        startdate = row[1]
        startprice = yf.download(row[3], start = pd.to_datetime(startdate) + pd.Timedelta(days = 0), end = pd.to_datetime(startdate) + pd.Timedelta(days = 1))
        endprice = yf.download(row[3], start = pd.to_datetime(startdate) + pd.Timedelta(days = 1) , end = pd.to_datetime(startdate) + pd.Timedelta(days = 2))
        print(startprice)
        print(endprice)

        startprice = float(startprice['Close'])
        endprice = float(endprice['Close'])
        pot_change = ((endprice - startprice)/startprice)*100

        alist.append(pot_change)
    except Exception as e:
        # alist.append('skipped')
        alist.append(0)
        print(f"An error occurred: {e}")

df['return_after_trade'] = alist

purchase_df = df[df['Transaction'] == 'Purchase'].sort_values('return_after_trade', ascending = False)
# purchase_df = df.sort_values('return_after_trade', ascending = False)

csv_filename = 'purchase_data.csv'
purchase_df.to_csv(csv_filename)
print('total return is: ', purchase_df['return_after_trade'].drop_duplicates().sum())
