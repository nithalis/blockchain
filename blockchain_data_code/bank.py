import pandas as pd
import numpy as np
import math

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

big = 'eth_txs_201901.csv'
small = 'ethtxs_1_1001.csv'
df = pd.read_csv(small)
'''
print(math.isnan(df.iat[31,6]))
print(df.iat[31,6] is math.nan)
df = df.replace(float('nan'), None)
print(df.iat[31,6] == None)

vals = df.loc[math.isnan(df['to_address'])]
print(vals)

print(df.shape)
df.dropna()
print(df.shape)

'''
print("#######################################")
df_deposits = df[['to_address', 'value']]
#print(df_deposits.dtypes)
df_deposits['value'] = df_deposits['value'].apply(pd.to_numeric, errors='coerce')
#print(df_deposits.dtypes)
# df_deposits = df_deposits.set_index('to_address')

s = df_deposits.value_counts(['to_address'])
s.name = "To_Counts"
#print(s.name)

df_deposits = df_deposits.groupby(['to_address']).sum()
df_deposits = df_deposits.merge(s, how = 'inner', on ='to_address')
df_deposits = df_deposits.sort_values(by='To_Counts', ascending=False)
print(df_deposits.head())



print("##############################")
print()

df_withdraws = df[['from_address', 'value']]
df_withdraws['value'] = df_withdraws['value'].apply(pd.to_numeric, errors='coerce')
# df_withdraws = df_withdraws.set_index('from_address')

s = df_withdraws.value_counts(['from_address'])
s.name = "From_Counts"
print(s.name)

df_withdraws = df_withdraws.groupby(['from_address']).sum()
df_withdraws = df_withdraws.merge(s, how = 'inner', on ='from_address')
df_withdraws = df_withdraws.sort_values(by='From_Counts', ascending=False)

print(df_withdraws.head())
print()


print('###############################')

df_merge = df_withdraws.merge(df_deposits, how = 'outer', left_index=True, right_index=True)
df_all = df_merge.dropna()

df_all["total_value"] = df_all['value_y'] - df_all['value_x']
df_all["avg_dep"] = df_all['value_y'] / df_all['To_Counts']
df_all["avg_with"] = df_all['value_x'] / df_all['From_Counts']

df_all = df_all.sort_values(by='total_value', ascending=False)
print(df_all.head(15))
