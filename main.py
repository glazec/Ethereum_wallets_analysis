import numpy as np
import csv
import pandas as pd
import pysnooper
import datetime
import matplotlib.pyplot as plt

# custom conversion function df.apply

# data=''
# with open('data/onenight_zerion.csv', newline='') as csvfile:
#     spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
#     for row in spamreader:
#         data = data+','.join(row)


# print(spamreader.list_dialects())
# my_data = np.loadtxt('data/onenight_zerion.csv', delimiter=',')


# @pysnooper.snoop()
def main():
    col_names = ['Date', 'Time', 'Transaction Type', 'Status', 'Application', 'Accounting Type', 'Buy Amount', 'Buy Currency', 'Buy Currency Address', 'Buy Fiat Amount', 'Buy Fiat Currency', 'Sell Amount', 'Sell Currency',
                 'Sell Currency Address', 'Sell Fiat Amount', 'Sell Fiat Currency', 'Fee Amount', 'Fee Currency', 'Fee Fiat Amount', 'Fee Fiat Currency', 'Sender', 'Receiver', 'Tx Hash', 'Link', 'Timestamp', 'Changes JSON']
    col_dtypes = {'Date': str, 'Time': str, 'Transaction Type': str, 'Status': str, 'Application': str, 'Accounting Type': str, 'Buy Amount': str, 'Buy Currency': str, 'Buy Currency Address': str, 'Buy Fiat Amount': str, 'Buy Fiat Currency': str, 'Sell Amount': str, 'Sell Currency': str,
                  'Sell Currency Address': str, 'Sell Fiat Amount': str, 'Sell Fiat Currency': str, 'Fee Amount': str, 'Fee Currency': str, 'Fee Fiat Amount': str, 'Fee Fiat Currency': str, 'Sender': str, 'Receiver': str, 'Tx Hash': str, 'Link': str, 'Timestamp': str, 'Changes JSON': str}
    parse_dates = ['Date', 'Time', 'Timestamp']
    df = pd.read_csv('data/ee_zerion.csv', skiprows=1,
                     delimiter=',', header=None, names=col_names, na_values=['no info', '.'], dtype=col_dtypes, parse_dates=parse_dates)
    print(min(df['Date']), ' To ', max(df['Date']))
    print('Total order numbers:', df.shape[0])
    pd.set_option('display.max_columns', None)

    # generate token lists
    tokens = generate_token_list(df)
    orders = []
    for i in tokens:
        try:
            token_name = i
            token_df = generate_single_token_df(df, token_name)
            orders.extend(analyze_single_token_trade(token_name, token_df))
        except BaseException as e:
            print(token_name)
            print(e)
    orders_pd = pd.DataFrame.from_dict(orders)
    orders_nocheat_pd = orders_pd[orders_pd['cheat'] == False]
    print(tokens)
    print('Total order: ', len(orders))
    print('No Cheat order: ', len(orders_nocheat_pd))
    print('Profit order:', len(
        orders_nocheat_pd[orders_nocheat_pd['balance'] > 0]))
    print('Order Success ration:', cacualte_order_success_ratio(orders_nocheat_pd))
    print('Net profit:', sum(orders_nocheat_pd['balance']))
    print('Median Duration:', np.median(
        orders_nocheat_pd['duration']).astype('timedelta64[m]'))
    # print(orders_nocheat_pd['size'])
    print(cacualte_order_success_ratio(
        orders_nocheat_pd[orders_nocheat_pd['size_eth'] > 2]))
    profit_size_margin = [cacualte_order_success_ratio(
        orders_nocheat_pd[orders_nocheat_pd['size_eth'] > i]) for i in np.arange(20, step=0.1)]
    fig, axs = plt.subplots(2)
    fig.suptitle('Order Success')
    axs[0].plot(list(np.arange(20, step=0.1)), profit_size_margin)
    axs[1].hist(orders_nocheat_pd['size_eth'], bins=np.arange(50, step=0.1))
    plt.show()
    # print(np.sum([i['balance'] for i in orders]))
    # print(np.sum())
    # print(len([i['balance'] > 0 for i in orders])/len(orders))


def cacualte_order_success_ratio(order_df):
    return len(order_df[order_df['balance'] > 0])/len(order_df)


def analyze_single_token_trade(token_name, token_df):
    balance = {token_name: 0, "ETH": 0}
    send_receive_balance = {token_name: 0, "ETH": 0}
    trading_size = {token_name: 0, "ETH": 0}
    orders = []
    order = init_order()
    # if the wallet send or receive the token, we do not count it as order
    for index, txn in token_df.iterrows():
        txn['Sell Currency']
        if balance[token_name] == 0 and balance['ETH'] == 0 and token_name not in txn['Sell Currency']:
            # this does not belong to any closed orders
            pass
        else:
            if order['closetime'] == '':
                order['closetime'] = txn['Timestamp']
            if txn['Transaction Type'] == 'Contract Execution':
                # we cannot filter this out
                pass
            elif txn['Transaction Type'] == 'Approval':
                # we can not filter this out
                # deduct approval cost from balance
                pass
            elif txn['Transaction Type'] == 'Send':
                balance[txn['Sell Currency']] -= float(txn['Sell Amount'])
                send_receive_balance[txn['Sell Currency']
                                     ] -= float(txn['Sell Amount'])
            elif txn['Transaction Type'] == 'Receive':
                balance[txn['Buy Currency']] += float(txn['Buy Amount'])
                send_receive_balance[txn['Buy Currency']
                                     ] += float(txn['Buy Amount'])
            # deal with multi currency and single currency trade
            elif txn['Transaction Type'] == 'Trade':
                if '\n' in txn['Buy Currency']:
                    # buy token: the token we receive
                    buy_currency_buffer = txn['Buy Currency'].split('\n')
                    buy_amount_buffer = txn['Buy Amount'].split('\n')
                    for i in range(len(buy_currency_buffer)):
                        balance[buy_currency_buffer[i]
                                ] += np.negative(float(buy_amount_buffer[i]))
                        trading_size[buy_currency_buffer[i]
                                     ] += float(buy_amount_buffer[i])
                else:
                    balance[txn['Buy Currency']] = (float(txn['Buy Amount']) if str(
                        txn['Buy Amount']) != 'nan' else 0)+balance[txn['Buy Currency']]
                # sell token: the token we sent
                if '\n' in txn['Sell Currency']:
                    sell_currency_buffer = txn['Sell Currency'].split('\n')
                    sell_amount_buffer = txn['Sell Amount'].split('\n')
                    for i in range(len(sell_currency_buffer)):
                        balance[sell_currency_buffer[i]
                                ] += np.negative(float(sell_amount_buffer[i]))
                        trading_size[sell_currency_buffer[i]
                                     ] += float(sell_amount_buffer[i])
                else:
                    balance[txn['Sell Currency']] += np.negative(
                        float(txn['Sell Amount']) if str(txn['Sell Amount']) != 'nan' else 0)
                    trading_size[txn['Sell Currency']] += (
                        float(txn['Sell Amount']) if str(txn['Buy Amount']) != 'nan' else 0)
        # manipulate the balance and fill order detail
            if np.around(balance[token_name], 4) == 0 and txn['Transaction Type'] == 'Trade':
                if np.around(send_receive_balance[token_name], 4) != 0:
                    order['cheat'] = True
                    send_receive_balance = {token_name: 0, "ETH": 0}
                order['balance'] = balance['ETH']
                order['opentime'] = txn['Timestamp']
                order['size_eth'] = trading_size["ETH"]
                order['duration'] = order['closetime']-order['opentime']
                order['token_pair'] = token_name
                orders.append(order)
                balance = {'ETH': 0, token_name: 0}
                order = init_order()
                trading_size = {"ETH": 0, token_name: 0}
    return orders


def generate_single_token_df(df, token_name):
    # method 1 to filter tokens
    token_1_df = df[df['Sell Currency'].str.startswith(
        token_name, na=False) & df['Sell Currency'].str.endswith(
        token_name, na=False)]
    token_delta_df = df[~df['Sell Currency'].str.startswith(
        token_name, na=False)]
    token_2_df = token_delta_df[token_delta_df['Buy Currency'].str.startswith(
        token_name, na=False) & df['Buy Currency'].str.endswith(
        token_name, na=False)]
    token_df = pd.concat([token_1_df, token_2_df])
    # method 2 to fillter tokens
    # token_df = df[df['Changes JSON'].str.contains(
    #     token_name, regex=False, na=False)]
    # drop the fail or cancelled txn
    token_df = token_df[df['Status'] == 'Confirmed']
    token_df.sort_values(by=['Timestamp'], inplace=True, ascending=False)
    token_df[['Sell Currency', 'Buy Currency']] = token_df[[
        'Sell Currency', 'Buy Currency']].fillna(value='')
    return token_df


def generate_token_list(df):
    # generate token lists
    tokens = []
    [tokens.extend(str(i).split('\n'))
     for i in df['Sell Currency'] if str(i) != 'nan']
    tokens = np.unique(tokens)
    # remove stable tokens
    tokens = np.delete(tokens, np.where(tokens == "ETH"))
    tokens = np.delete(tokens, np.where(tokens == "USDT"))
    tokens = np.delete(tokens, np.where(tokens == "USDC"))
    tokens = np.delete(tokens, np.where(tokens == "UNI-V2"))
    tokens = np.delete(tokens, np.where(tokens == "SBREE"))
    tokens = np.delete(tokens, np.where(tokens == "BREE"))

    # print(token_df)
    return tokens


def init_order():
    # init order data
    return {'opentime': '', 'closetime': '',
            'currency': 'ETH', 'balance': 0, 'size': {}, 'cheat': False, 'duration': '', 'token_pair': ''}


def trade_time_hist(times):
    # trade_time_hist([i.hour for i in data['Time']])
    plt.hist(times, bins=np.arange(25))
    plt.xlabel('Time')
    plt.show()


if __name__ == "__main__":
    main()
