import pandas as pd
import numpy as np
import math

def create_frame(df_grouped, other_col, prefix, merge_col):
    # count number of occurrences
    counts = df_grouped.count()
    counts.rename(columns={"value": prefix+"_count"},inplace = True)
    counts.drop(columns=[other_col], inplace=True)


    # count total value sent or received
    total = df_grouped.sum(numeric_only=True)
    total.rename(columns={"value": prefix+"_total"},inplace = True)

    # count number of unique partners
    partners = df_grouped.nunique()[other_col]
    partners.name = prefix+"_partners"

    '''
    # min value - only matters if not 0
    min = df_grouped['value'].min(numeric_only=True)
    min.name = prefix+"_min"
    # count number of zero values
    num_erc20 = df_grouped['value'].nsmallest(n=1, keep='all')
    num_erc20 = num_erc20.count(level=0)
    num_erc20.name = prefix+"_count_erc20"
    # max value
    max = df_grouped.max(numeric_only=True)
    max.rename(columns={"value": prefix+"_max"},inplace = True)

    # median value
    median = df_grouped.median(numeric_only=True)
    median.rename(columns={"value": prefix+"_median"},inplace = True)


    # merge all series to dataframe
    series_list = [total, partners, min, num_erc20, max, median]
    '''
    series_list = [total, partners]

    for s in series_list:
        counts = counts.merge(s, how='inner', on=merge_col)


    # ranking addresses by certain features
    rank_total = counts[prefix+"_total"].rank(ascending=False, pct=True)
    rank_total.name = prefix+"_total_rank"
    # print(rank_total)

    rank_partners = counts[prefix+"_partners"].rank(ascending=False, pct=True)
    rank_partners.name = prefix+"_partners_rank"
    # print(rank_partners)

    rank_erc20 = counts[prefix+"_count_erc20"].rank(ascending=False, pct=True)
    rank_erc20.name = prefix+"_count_erc20_rank"

    rank_list = [rank_total, rank_partners, rank_erc20]

    for rank in rank_list:
        counts = counts.merge(rank, how='inner', on=merge_col)


    return counts

def main():
    # functionality to print more columns
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)

    # listing all the different files to read
    test = 'ethtxs_1_11.csv'
    big = 'eth_txs_201901.csv'
    small = 'ethtxs_1_1001.csv'
    df_all = pd.read_csv(big)

    # read in the file
    df = df_all[['from_address', 'to_address', 'value']]

    # make the value of the transactions numeric
    df['value'] = df['value'].apply(pd.to_numeric, errors='coerce')

    # group receiving addresses
    group_to_address = df.groupby(['to_address'])
    receiving_features = create_frame(group_to_address, 'from_address', 'receiving', 'to_address')

    # group sending addresses
    group_from_address = df.groupby(['from_address'])
    sending_features = create_frame(group_from_address, 'to_address', 'sending', 'from_address')

    print("Created Sending and Receiving Frames")
    print()


    # merging dataframes
    df_merge = receiving_features.merge(sending_features, how = 'outer', left_index=True, right_index=True)

    df_send_receive = df_merge.dropna()
    df_send_receive['balance'] = df_send_receive['receiving_total'] - df_send_receive['sending_total']
    df_send_receive.to_csv("both_2.csv")

    only_send = df_merge[df_merge['receiving_count'].isnull()]
    only_send.dropna(axis=1, how='all', inplace=True)
    only_send.to_csv("send_2.csv")

    only_receive = df_merge[df_merge['sending_count'].isnull()]
    only_receive.dropna(axis=1, how='all', inplace=True)
    only_receive.to_csv("receive_2.csv")

    print("All done!")

if __name__ == "__main__":
    main()
