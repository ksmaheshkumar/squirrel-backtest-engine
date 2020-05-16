# Backtest that Strategy 
import os
import pandas as pd
import datetime
os.chdir(os.path.dirname(os.path.abspath(__file__)))
p='N::-100_S_PE_20,N::200_B_CE_20&et=11:19:00,15:19:00&s=intraday&ed=1,0&sfm=false&sfd=1577836800000&std=1580375444968'
#This function will take overall Strategy code as an argument and split it for better execution
def strategy(p):
    position   = p.split('&')[0].split(',')
    entry_time = p.split('&')[1].split(',')[0].split('=')[1]
    exit_time  = p.split('&')[1].split(',')[1]
    date       = str(datetime.datetime.fromtimestamp(int(p.split('&')[5].split('=')[1])/1000)).split(' ')[0].split('-')
    start_date = date[0]+date[1]+date[2]
    date       = str(datetime.datetime.fromtimestamp(int(p.split('&')[6].split('=')[1])/1000)).split(' ')[0].split('-')
    end_date   = date[0]+date[1]+date[2]
    combination = []
    for i in range(0,len(position)):
        index  = position[i].split('::')[0]
        strike = position[i].split('::')[1].split('_')[0] 
        action = position[i].split('::')[1].split('_')[1]
        option = position[i].split('::')[1].split('_')[2]
        lot    = position[i].split('::')[1].split('_')[3]
        leg    = [index,strike,action,option,lot,entry_time,exit_time,start_date,end_date]
        combination.append(leg)
    return combination
#Calculate the Entry Price and at Start Date and Exit Price at all dates until End Date
test = pd.read_csv('Data/JANIFTY.csv')
time_column  = test['TIME']
price_column = test['OPEN']
date_column  = test['NOT REQUIRED']
def price_column(entry_time,start_date):
    """for d in date_column:
        for t in time_column:
            #Error here 
            if str(t) == entry_time and str(d) == date_column: 
                price = float((price_column[list(date_column).index(d)]))
                strike_difference = 100 if data[0] == 'BN' else 50
                a = (price//strike_difference)*strike_difference
                b = a + strike_difference 
                atm = int(b if price - a > b - price else a)
                return atm"""
def Calculator(list):
    index  = list[0]
    strike = list[1]
    action = list[2]
    option = list[3]
    lot    = list[4]
    entry_time = list[5].split(':')[0] + ':' + list[5].split(':')[1]
    exit_time  = list[6].split(':')[0] + ':' + list[6].split(':')[1]
    start_date = list[7]
    end_date   = list[8]
    traded_strike = price_column(entry_time,start_date)
    return traded_strike
    csv_data = pd.read_csv('Data/2020/JAN2020/NIFTY' + str(strike_traded) + str(list[3]) + str('.csv'))
    return csv_data
for s in strategy(p):
    Calculator(s)

