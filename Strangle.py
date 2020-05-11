from functioner import *
import pandas as pd

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

test = pd.read_csv('Data/JANIFTY.csv')
time_column = test['TIME']
price_column = test['OPEN']

NSEI = pd.read_csv('Data/^NSEI.csv')
trade_date = NSEI['Date']
open_price = NSEI['Open']


strangle = leg_tracker(time_column,trade_date,price_column,open_price)

#This function calculates the Entry Point
def entry(x,z,b,m):
    a = 0
    c = 0
    while a < len(x):
        while c < len(z):
            if x[a] == trade_date[b] and z[c] == '09:20':
                return m[c]
                break
            else:
                c += 1
            a += 1

#This function calculates the Exit
def exit(x,c,m,k,z):
    a = 0
    b = 0
    while a < len(x):
        while b < len(z):
            if x[a] == trade_date[c] and z[b] >= m:
                return z[b]
                break
            elif x[a] == trade_date[c] and (k[b] == '14:50' or k[b] == '14:51' or k[b] == '14:52' or k[b] == '14:53'):
                return z[b]
                break
            else:
                a += 1
                b += 1

date_column = []
upper_strike_column = []
lower_strike_column = []
upper_entry = []
lower_entry = []
upper_exit = []
lower_exit = []
profit_upper = []
profit_lower = []
year_list = ['JAN2020','FEB2020','JAN2019','FEB2019','MAR2019','APR2019','MAY2019','JUN2019','JUL2019','AUG2019','SEP2019','OCT2019','NOV2019','DEC2019','']
k = 0
while k < (len(trade_date)):

    upperStrike = pd.read_csv('Data/2020/JAN2020/NIFTY' + str(strangle['Upper Leg'][str(trade_date[k])]) + str('CE.csv'))
    lowerStrike = pd.read_csv('Data/2020/JAN2020/NIFTY' + str(strangle['Lower Leg'][str(trade_date[k])]) + str('PE.csv'))

    date_ce = upperStrike['date']
    time_ce = upperStrike['time']
    premium_ce = upperStrike['D']

    date_pe = lowerStrike['date']
    time_pe = lowerStrike['time']
    premium_pe = lowerStrike['D']

    date_pe=date_pe.str.replace('/','-')
    date_ce=date_ce.str.replace('/','-')

    entry_upper_strike = entry(date_ce,time_ce,k,premium_ce)
    entry_lower_strike = entry(date_pe,time_pe,k,premium_pe)
    if entry_lower_strike is not None or entry_upper_strike is not None:
        upper_sl = entry_upper_strike * 1.2
        lower_sl = entry_lower_strike * 1.2
        exit_upper_strike = exit(date_ce,k,upper_sl,time_ce,premium_ce)
        exit_lower_strike = exit(date_pe,k,lower_sl,time_pe,premium_pe)
        #Here Strike Price , Date , Entry , Exit , Net P&L Everything will be printed
        #print("Trade on: ",trade_date[k])
        #print("Upper Strike :",strangle['Upper Leg'][str(trade_date[k])],"CE")
        #print("Entry :",entry_upper_strike)
        #print("Exit  :",exit_upper_strike)
        #print("Lower Strike :",strangle['Lower Leg'][str(trade_date[k])],"PE")
        #print("Entry :",entry_lower_strike)
        #print("Exit  :",exit_lower_strike)
        #print('\n')
        date_column.append(trade_date[k])
        upper_strike_column.append(strangle['Upper Leg'][str(trade_date[k])])
        upper_entry.append(entry_upper_strike)
        upper_exit.append(exit_upper_strike)
        profit_upper.append(entry_upper_strike-exit_upper_strike)
        lower_strike_column.append(strangle['Lower Leg'][str(trade_date[k])])
        lower_entry.append(entry_lower_strike)
        lower_exit.append(exit_lower_strike)
        profit_lower.append(entry_lower_strike-exit_lower_strike)
        k += 1
    else :
        k += 1
Data = {
        'Date' : date_column,
        'Upper Strike': upper_strike_column,
        'Upper Entry': upper_entry,
        'Upper Exit':  upper_exit,
        'Upper Profit': profit_upper,
        'Lower Strike': lower_strike_column,
        'Lower Entry': lower_entry,
        'Lower Exit':  lower_exit,
        'Lower Profit': profit_lower
}
df = pd.DataFrame(Data,columns=['Date','Upper Strike','Upper Entry','Upper Exit','Upper Profit','Lower Strike','Lower Entry','Lower Exit','Lower Profit'])
print(df)
