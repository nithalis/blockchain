import pandas as pd
import numpy as np
import math

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

test = 'ethtxs_1_11.csv'
big = 'eth_txs_201901.csv'
small = 'ethtxs_1_1001.csv'
df_all = pd.read_csv(test)

df = df_all[['from_address', 'to_address', 'value']]

df['value'] = df['value'].apply(pd.to_numeric, errors='coerce')
print(df.dtypes)

count_deposits = df.value_counts(['to_address'])
count_deposits.name = "receiving_count"

count_withdraws = df.value_counts(['from_address'])
count_withdraws.name = "sending_count"

deposits_group = df.groupby(['to_address'])
check = deposits_group.value_counts()
print(check)
'''
incoming = deposits_group.nunique()['from_address']
incoming.name = 'unique_incoming'

incoming_std = deposits_group.std()['value']
incoming_std.name = "receiving_std"
incoming_mean = deposits_group.mean()['value']
incoming_mean.name = "receiving_mean"
incoming_min = deposits_group.min()['value']
incoming_min.name = "receiving_min"
incoming_max = deposits_group.max()['value']
incoming_max.name = "receiving_max"


deposits_group = deposits_group.sum()
deposits_group = deposits_group.merge(incoming, how = 'inner', on='to_address')
deposits_group = deposits_group.merge(incoming_std, how = 'inner', on='to_address')
deposits_group = deposits_group.merge(incoming_mean, how = 'inner', on='to_address')
deposits_group = deposits_group.merge(incoming_min, how = 'inner', on='to_address')
deposits_group = deposits_group.merge(incoming_max, how = 'inner', on='to_address')
deposits_group = deposits_group.merge(count_deposits, how = 'inner', on ='to_address')


withdraws_group = df.groupby(['from_address'])
outgoing = withdraws_group.nunique()['to_address']
outgoing.name = 'unique_outgoing'
withdraws_group = withdraws_group.sum()
withdraws_group = withdraws_group.merge(outgoing, how = 'inner', on='from_address')
withdraws_group = withdraws_group.merge(count_withdraws, how = 'inner', on ='from_address')
'''
print("RECEVING")
print(deposits_group.head())
print()
'''
print("SENDING")
print(withdraws_group.head())
print()


print("Merging")

df_merge = withdraws_group.merge(deposits_group, how = 'outer', left_index=True, right_index=True)
# print(df_merge.head(15))
df_merge.rename(columns={"value_x": "tamt_sending", "value_y": "tamt_receiving"},inplace = True)

#print(df_merge.loc[['0xA855C20A1351AcD2690c716E2709C7dfF3978D12']])
print(df_merge.loc[['0xbCEaA0040764009fdCFf407e82Ad1f06465fd2C4']])
# print(df_merge.loc[['only_send']])


print()
df_both = df_merge.dropna()

# print(df_merge.shape)
print()
# print(df_new.head(15))
print()

df_merge["total_value"] = df_merge['tamt_receiving'] - df_merge['tamt_sending']
df_merge["avg_receive"] = df_merge['tamt_receiving'] / df_merge['receiving_count']
df_merge["avg_send"] = df_merge['tamt_sending'] / df_merge['sending_count']

#print(df_merge.describe())
print(df_merge.shape)
print()

only_send = df_merge[df_merge['tamt_receiving'].isnull()]
print(only_send.head())
print(only_send.isnull())
print()
print("Only Send Shape", only_send.shape)
only_receive = df_merge[df_merge['tamt_sending'].isnull()]
print("Only Receive Shape", only_receive.shape)
print(only_receive.head())
#print(test.index)
print()
#print(df_merge.index)
# only_receive = df_merge[df_merge.index.isin(no_receive.index) == False]
# only_send = df_merge[df_merge.index.isin(no_receive.index) == False]

print("Receive shape")
print(only_receive.head())
print("Sending shape")
print(only_send.head())
print()
print()

#df_send = df_merge.drop(test)
print(only_receive.describe())
print()
print(only_send.describe())
'''
