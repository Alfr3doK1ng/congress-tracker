import yfinance as yf
import pandas as pd
from pathlib import Path
import quiverquant
import matplotlib.pyplot as plt

key = "https://api.quiverquant.com"
quiver = quiverquant.quiver(key)


# df = quiver.congress_trading()
# df.to_csv('quiverDF.csv', index=False)
df = pd.read_csv('quiverDF.csv')
# df = df[df['TransactionDate'] >= '2024-02-01']
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

purchase_df = df[df['Transaction'] == 'Purchase'].sort_values('ReportDate', ascending = True)
# purchase_df = df.sort_values('return_after_trade', ascending = False)

csv_filename = 'purchase_data.csv'
purchase_df.to_csv(csv_filename)
print('total return is: ', purchase_df['return_after_trade'].drop_duplicates().sum())

# Drop duplicates based on 'return_after_trade'
purchase_df = purchase_df.drop_duplicates(subset=['return_after_trade'])

# Convert 'ReportDate' to datetime format for correct sorting
purchase_df['ReportDate'] = pd.to_datetime(purchase_df['ReportDate'])

# Sort the dataframe by 'ReportDate'
purchase_df = purchase_df.sort_values('ReportDate')

# Calculate the cumulative sum of 'return_after_trade' to get the accumulated change
purchase_df['accumulated_change'] = purchase_df['return_after_trade'].cumsum()

# Plot the accumulated change over time
plt.figure(figsize=(12, 6))
plt.plot(purchase_df['ReportDate'], purchase_df['accumulated_change'], marker='o', linestyle='-')
plt.title('Accumulated Potential Change Over Time')
plt.xlabel('Report Date')
plt.ylabel('Accumulated Potential Change (%)')
plt.grid(True)
plt.show()