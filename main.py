import numpy as np
import csv
import pandas as pd
import pysnooper
import datetime
import matplotlib.pyplot as plt

#custom conversion function df.apply

# data=''
# with open('data/onenight_zerion.csv', newline='') as csvfile:
#     spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
#     for row in spamreader:
#         data = data+','.join(row)


# print(spamreader.list_dialects())
# my_data = np.loadtxt('data/onenight_zerion.csv', delimiter=',')


# @pysnooper.snoop()
def main():
    col_names = ['Date', 'Time', 'Transaction Type', 'Status', 'Application', 'Accounting Type', 'Buy Amount', 'Buy Currency', 'Buy Currency Address', 'Buy Fiat Amount', 'Buy Fiat Currency', 'Sell Amount', 'Sell Currency', 'Sell Currency Address', 'Sell Fiat Amount', 'Sell Fiat Currency', 'Fee Amount', 'Fee Currency', 'Fee Fiat Amount', 'Fee Fiat Currency', 'Sender', 'Receiver', 'Tx Hash', 'Link', 'Timestamp', 'Changes JSON']
    col_dtypes = {'Date':str, 'Time':str, 'Transaction Type':str, 'Status':str, 'Application':str, 'Accounting Type':str, 'Buy Amount':str, 'Buy Currency':str, 'Buy Currency Address':str, 'Buy Fiat Amount':str, 'Buy Fiat Currency':str, 'Sell Amount':str, 'Sell Currency':str,'Sell Currency Address':str, 'Sell Fiat Amount':str, 'Sell Fiat Currency':str, 'Fee Amount':str, 'Fee Currency':str, 'Fee Fiat Amount':str, 'Fee Fiat Currency':str, 'Sender':str, 'Receiver':str, 'Tx Hash':str, 'Link':str, 'Timestamp':str, 'Changes JSON':str}
    parse_dates = ['Date', 'Time','Timestamp']
    df = pd.read_csv('data/onenight_zerion.csv', skiprows=1,
                       delimiter=',', header=None, names=col_names, na_values=['no info', '.'], dtype=col_dtypes, parse_dates=parse_dates)
    print(min(df['Date']),' To ',max(df['Date']))
    print('Total order numbers:', df.shape[0])

    # generate token lists
    tokens=[]
    [tokens.extend(str(i).split('\n')) for i in df['Sell Currency'] if str(i)!='nan']
    tokens=np.unique(tokens)
    # filter tokens
    pd.set_option('display.max_columns', None)
    token_name = 'SPORE'
    print(df.head())
    # method 1 to filter tokens
    # token_1_df = df[df['Sell Currency'].str.contains(
    #     token_name, regex=False, na=False)]
    # token_delta_df = df[~df['Sell Currency'].str.contains(
    #     token_name, regex=False, na=False)]
    # token_2_df = token_delta_df[token_delta_df['Buy Currency'].str.contains(
    #     token_name, regex=False, na=False)]
    # token_df = pd.concat([token_1_df,token_2_df])
    # method 2 to fillter tokens
    token_df = df[df['Changes JSON'].str.contains(token_name, regex=False,na=False)]
    #drop the fail or cancelled txn
    token_df = token_df[df['Status'] == 'Confirmed']
    token_df.sort_values(by=['Timestamp'], inplace=True, ascending=False)

    # organize into orders
    # orders{startTime,closeTime,buyAmount,Buycurrency,Fiat,Sell,profit,type:success,fail}
    
    #profit or loss
    # need to deduct fees
    balance = {token_name: 0, "ETH": 0}
    send_receive_balance = {token_name: 0, "ETH": 0}
    trading_size = {token_name: 0, "ETH": 0}
    orders=[]
    order = {'opentime': '', 'closetime': '', 'currency': 'ETH',
             'balance': 0, 'token': token_name, 'size': {}}
    # if the wallet send or receive the token, we do not count it as order
    for index, txn in token_df.iterrows():
        if balance[token_name] == 0 and balance['ETH']==0 and token_name not in txn['Sell Currency']:
            # this does not belong to any closed orders
            pass
        else:
            # print('========')
            # print(index)
            # print(txn['Buy Currency'])
            # print(txn['Sell Currency'])
            # print(txn['Buy Amount'])
            # print(txn['Buy Amount'])
            # print(balance['ETH'])
            # print(balance[token_name])
            # print(balance)
            if order['closetime']=='':
                order['closetime'] = txn['Timestamp']
            if txn['Transaction Type']=='Contract Execution':
                # we cannot filter this out
                pass
            elif txn['Transaction Type'] == 'Approval':
                # we can not filter this out
                # deduct approval cost from balance
                pass
            elif txn['Transaction Type'] == 'Send':
                balance[txn['Sell Currency']]-=float(txn['Sell Amount'])
                send_receive_balance[txn['Sell Currency']] -= float(txn['Sell Amount'])
                pass
            elif txn['Transaction Type'] == 'Receive':
                balance[txn['Buy Currency']] += float(txn['Buy Amount'])
                send_receive_balance[txn['Buy Currency']] += float(txn['Buy Amount'])

                pass
            #deal with multi currency and single currency trade
            elif txn['Transaction Type'] == 'Trade':
                if '\n' in txn['Buy Currency']:
                # buy token: the token we receive
                    buy_currency_buffer=txn['Buy Currency'].split('\n')
                    buy_amount_buffer = txn['Buy Amount'].split('\n')
                    for i in range(len(buy_currency_buffer)):
                        balance[buy_currency_buffer[i]] += np.negative(float(buy_amount_buffer[i]))
                        trading_size[buy_currency_buffer[i]] += float(buy_amount_buffer[i])
                else:
                    balance[txn['Buy Currency']] += (
                        float(txn['Buy Amount']) if str(txn['Buy Amount']) != 'nan' else 0)
                # sell token: the token we sent
                if '\n' in txn['Sell Currency']:
                    sell_currency_buffer=txn['Sell Currency'].split('\n')
                    sell_amount_buffer = txn['Sell Amount'].split('\n')
                    print('========zip=====')
                    print(dict(zip(sell_currency_buffer, sell_amount_buffer)))
                    for i in range(len(sell_currency_buffer)):
                        balance[sell_currency_buffer[i]] += np.negative(float(sell_amount_buffer[i]))
                        trading_size[sell_currency_buffer[i]] += float(sell_amount_buffer[i])
                else:
                    balance[txn['Sell Currency']] += np.negative(float(txn['Sell Amount']) if str(txn['Sell Amount']) != 'nan' else 0)
                    trading_size[txn['Sell Currency']]+= (float(txn['Sell Amount']) if str(txn['Buy Amount']) != 'nan' else 0)
        #manipulate the balance and fill order detail
            if balance[token_name] == 0:
                if send_receive_balance[token_name]!=0:
                    order['cheat']=True
                    send_receive_balance = {token_name: 0, "ETH": 0}
                order['balance'] = balance['ETH']
                order['opentime'] = txn['Timestamp']
                order['size']=trading_size
                orders.append(order)
                balance = {'ETH': 0, token_name: 0}
                order = {'opentime': '', 'closetime': '',
                         'currency': 'ETH', 'balance': 0,'size':{},'cheat':False}
                trading_size = {"ETH": 0, token_name: 0}
            #close the order
    print(orders)
    # print(token_df)


def trade_time_hist(times):
    # trade_time_hist([i.hour for i in data['Time']])
    plt.hist(times,bins=np.arange(25))
    plt.xlabel('Time')
    plt.show()




if __name__ == "__main__":
    main()
