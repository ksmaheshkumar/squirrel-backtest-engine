from Functioner import *
import pandas as pd

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))


# Time_column = csv_reader('Data/JANIFTY.csv',2)
# Price_column = csv_reader('Data/JANIFTY.csv',3)
# Trade_Date = csv_reader('Data/^NSEI.csv',0)
# Open_Price = csv_reader('Data/^NSEI.csv',1)


test = pd.read_csv('Data/JANIFTY.csv')
Time_column = test['TIME']
Price_column = test['OPEN']

NSEI = pd.read_csv('Data/^NSEI.csv')
Trade_Date = NSEI['Date']
Open_Price = NSEI['Open']


Strangle = leg_tracker(Time_column,Trade_Date,Price_column,Open_Price)

#This function calculates the Entry Point
def Entry(x,z,b,m):
    a = 0
    c = 0
    while a < len(x):
        while c < len(z):
            if x[a] == Trade_Date[b] and z[c] == '09:20':
                return m[c]
                break
            else:
                c += 1
            a += 1

#This function calculates the Exit
def Exit(x,c,m,k,z):
    a = 0
    b = 0
    while a < len(x):
        while b < len(z):
            if x[a] == Trade_Date[c] and z[b] >= m:
                return z[b]
                break
            elif x[a] == Trade_Date[c] and (k[b] == '14:50' or k[b] == '14:51' or k[b] == '14:52' or k[b] == '14:53'):
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
while k < (len(Trade_Date)):

    upperStrike = pd.read_csv('Data/2020/JAN2020/NIFTY' + str(Strangle['Upper Leg'][str(Trade_Date[k])]) + str('CE.csv'))
    lowerStrike = pd.read_csv('Data/2020/JAN2020/NIFTY' + str(Strangle['Lower Leg'][str(Trade_Date[k])]) + str('PE.csv'))

    date_ce = upperStrike['date']
    time_ce = upperStrike['time']
    premium_ce = upperStrike['D']

    date_pe = lowerStrike['date']
    time_pe = lowerStrike['time']
    premium_pe = lowerStrike['D']

    date_pe=date_pe.str.replace('/','-')
    date_ce=date_ce.str.replace('/','-')

    entry_upper_strike = Entry(date_ce,time_ce,k,premium_ce)
    entry_lower_strike = Entry(date_pe,time_pe,k,premium_pe)
    if entry_lower_strike is not None or entry_upper_strike is not None:
        Upper_SL = entry_upper_strike * 1.2
        Lower_SL = entry_lower_strike * 1.2
        exit_upper_strike = Exit(date_ce,k,Upper_SL,time_ce,premium_ce)
        exit_lower_strike = Exit(date_pe,k,Lower_SL,time_pe,premium_pe)
        #Here Strike Price , Date , Entry , Exit , Net P&L Everything will be printed
        #print("Trade on: ",Trade_Date[k])
        #print("Upper Strike :",Strangle['Upper Leg'][str(Trade_Date[k])],"CE")
        #print("Entry :",entry_upper_strike)
        #print("Exit  :",exit_upper_strike)
        #print("Lower Strike :",Strangle['Lower Leg'][str(Trade_Date[k])],"PE")
        #print("Entry :",entry_lower_strike)
        #print("Exit  :",exit_lower_strike)
        #print('\n')
        date_column.append(Trade_Date[k])
        upper_strike_column.append(Strangle['Upper Leg'][str(Trade_Date[k])])
        upper_entry.append(entry_upper_strike)
        upper_exit.append(exit_upper_strike)
        profit_upper.append(entry_upper_strike-exit_upper_strike)
        lower_strike_column.append(Strangle['Lower Leg'][str(Trade_Date[k])])
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
