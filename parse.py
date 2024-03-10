import pandas as pd

file_path = '2024FD.txt'
df = pd.read_csv(file_path, sep='\t', header=None, names=['Prefix', 'Last', 'First', 'Suffix', 'FilingType', 'StateDst', 'Year', 'FilingDate', 'DocID'])
df.drop(0, inplace=True)
df.reset_index(drop=True, inplace=True)
# Convert FilingDate to datetime
df['FilingDate'] = pd.to_datetime(df['FilingDate'])

# Sort by FilingDate
df_sorted = df.sort_values(by='FilingDate', ascending=False)

# Display the sorted DataFrame
print(df_sorted)
