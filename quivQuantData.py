import yfinance as yf
import pandas as pd
from pathlib import Path
import quiverquant

key = "https://api.quiverquant.com"
quiver = quiverquant.quiver(key)

df = quiver.congress_trading()
df = df[df['TransactionDate'] >= '2023-01-01']
print(df)

alist = []
for index, row in df.iterrows():
    try:
        startdate = row[1]
        startprice = yf.download(row[2], start = startdate, end = startdate + pd.Timedelta(days = 1))
        endprice = yf.donwload(row[2], start = '2023-03-02', end = '2023-03-03')

        startprice = float(startprice['Close'])
        endprice = float(endprice['Close'])
        pot_change = ((endprice - startprice)/startprice)*100

        alist.append(pot_change)
    except:
        alist.append('skipped')

df['return_after_trade'] = alist


purchase_df = df[df['Transaction'] == 'Purchase'].sort_values('return_after_trade', ascending = False)

csv_filename = 'purchase_data.csv'
purchase_df.to_csv(csv_filename)
