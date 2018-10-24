
# coding: utf-8

# In[71]:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import quandl
import datetime


# #we would be extracting financial variables such as 
# 1.exchange rates(USD/CHN,USD/GBP,USD/EUR etc) 
# 2.crude oil
# 3.gold prices
# 4.stock indices
# 5.Blockchain features

# Eurostoxx--https://query1.finance.yahoo.com/v7/finance/download/%5ESTOXX50E?period1=148318920
# FTSE100--https://query1.finance.yahoo.com/v7/finance/download/%5ESTOXX50E?period1=1483189200&period2=1522591200&interval=1d&events=history&crumb=HT16U7Irg1K
# SSE--https://query1.finance.yahoo.com/v7/finance/download/000001.SS?period1=1483189200&period2=1522591200&interval=1d&events=history&crumb=HT16U7Irg1K
# DowJones--https://fred.stlouisfed.org/graph/fredgraph.csv?chart_type=line&recession_bars=on&log_scales=&bgcolor=%23e1e9f0&graph_bgcolor=%23ffffff&fo=Open+Sans&ts=12&tts=12&txtcolor=%23444444&show_legend=yes&show_axis_titles=yes&drp=0&cosd=2016-12-31&coed=2018-03-28&height=450&stacking=&range=Custom&mode=fred&id=DJIA&transformation=lin&nd=2008-03-31&ost=-99999&oet=99999&lsv=&lev=&mma=0&fml=a&fgst=lin&fgsnd=2009-06-01&fq=Daily&fam=avg&vintage_date=&revision_date=&line_color=%234572a7&line_style=solid&lw=2&scale=left&mark_type=none&mw=2&width=1168
# Nikkei--https://fred.stlouisfed.org/graph/fredgraph.csv?chart_type=line&recession_bars=off&log_scales=&bgcolor=%23e1e9f0&graph_bgcolor=%23ffffff&fo=Open+Sans&ts=12&tts=12&txtcolor=%23444444&show_legend=yes&show_axis_titles=yes&drp=0&cosd=2016-12-31&coed=2018-03-24&height=450&stacking=&range=Custom&mode=fred&id=NIKKEI225&transformation=lin&nd=1949-05-16&ost=-99999&oet=99999&lsv=&lev=&mma=0&fml=a&fgst=lin&fgsnd=2009-06-01&fq=Daily%2C+Close&fam=avg&vintage_date=&revision_date=&line_color=%234572a7&line_style=solid&lw=2&scale=left&mark_type=none&mw=2&width=1168
# Nasdaq--https://fred.stlouisfed.org/graph/fredgraph.csv?chart_type=line&recession_bars=on&log_scales=&bgcolor=%23e1e9f0&graph_bgcolor=%23ffffff&fo=Open+Sans&ts=12&tts=12&txtcolor=%23444444&show_legend=yes&show_axis_titles=yes&drp=0&cosd=2016-12-31&coed=2018-03-27&height=450&stacking=&range=Custom&mode=fred&id=NASDAQCOM&transformation=lin&nd=1971-02-05&ost=-99999&oet=99999&lsv=&lev=&mma=0&fml=a&fgst=lin&fgsnd=2009-06-01&fq=Daily&fam=avg&vintage_date=&revision_date=&line_color=%234572a7&line_style=solid&lw=2&scale=left&mark_type=none&mw=2&width=1168
# VIX--https://fred.stlouisfed.org/graph/fredgraph.csv?chart_type=line&recession_bars=on&log_scales=&bgcolor=%23e1e9f0&graph_bgcolor=%23ffffff&fo=Open+Sans&ts=12&tts=12&txtcolor=%23444444&show_legend=yes&show_axis_titles=yes&drp=0&cosd=2016-12-31&coed=2018-03-27&height=450&stacking=&range=Custom&mode=fred&id=VIXCLS&transformation=lin&nd=1990-01-02&ost=-99999&oet=99999&lsv=&lev=&mma=0&fml=a&fgst=lin&fgsnd=2009-06-01&fq=Daily%2C+Close&fam=avg&vintage_date=&revision_date=&line_color=%234572a7&line_style=solid&lw=2&scale=left&mark_type=none&mw=2&width=1168
# crudeoil--https://fred.stlouisfed.org/graph/fredgraph.csv?chart_type=line&recession_bars=on&log_scales=&bgcolor=%23e1e9f0&graph_bgcolor=%23ffffff&fo=Open+Sans&ts=12&tts=12&txtcolor=%23444444&show_legend=yes&show_axis_titles=yes&drp=0&cosd=2016-12-31&coed=2018-03-24&height=450&stacking=&range=Custom&mode=fred&id=DCOILWTICO&transformation=lin&nd=1986-01-02&ost=-99999&oet=99999&lsv=&lev=&mma=0&fml=a&fgst=lin&fgsnd=2009-06-01&fq=Daily&fam=avg&vintage_date=&revision_date=&line_color=%234572a7&line_style=solid&lw=2&scale=left&mark_type=none&mw=2&width=1168

# In[204]:

def preprocess_series(df):
    #convert the index to datetime index
    df.index = pd.to_datetime(df.index)
    #slice the date range to 01-01-2017 -- 23-03-2017
    df = df['2017-01-01':'2018-03-23']
    #print(len(df))
    #print('dtype--',df.dtypes)
    #drop duplicate values
    df = df[~df.index.duplicated(keep=False)]
    #check datatype of the column,should only consist of numbers(fill with nans)
    df = df.apply(pd.to_numeric,errors='coerce')
    #print('null--',df.isnull().sum())
    #reindex if the date range not available.
    start = datetime.datetime(2017, 1, 1)
    end = datetime.datetime(2018, 3, 23)
    index = pd.date_range(start, end,freq='1H')
    df = df.reindex(index)
    #bfill or ffill to fill the values
    df = df.fillna(method='pad')
    if df.isnull().sum().values[0] != 0:
        df = df.fillna(method='bfill')
    #upsample to hourly
    #df = df.asfreq('60Min',method='pad')
    #return
    return pd.DataFrame(df)

# In[206]:

def get_exchange_data():
    #https://www.ofx.com/en-au/forex-news/historical-exchange-rates/
    eur = preprocess_series(pd.read_csv('US_EUR.csv',index_col='DATE'))
    cny = preprocess_series(pd.read_csv('US_CNY.csv',index_col='DATE'))
    chf = preprocess_series(pd.read_csv('US_CHF.csv',index_col='DATE'))
    gbp = preprocess_series(pd.read_csv('US_GBP.csv',index_col='DATE'))
    jpy = preprocess_series(pd.read_csv('US_JPN.csv',index_col='DATE'))
    exchange_data = pd.concat([eur,cny,chf,gbp,jpy],axis=1)
    exchange_data.columns = ['eur','cny','chf','gbp','jpy']
    return exchange_data


# In[324]:

#exchange_data = get_exchange_data()
#exchange_data.head()


# In[218]:

#https://fred.stlouisfed.org/series/DCOILWTICO
def get_crudeoil_data():
    oil_data = preprocess_series(pd.read_csv('WTI_crude_oil.csv',index_col='DATE'))
    return oil_data


# In[322]:

#crude_oil = get_crudeoil_data()
#crude_oil.head()


# In[222]:

#https://www.gold.org/data/gold-price
def get_gold_data():
    gold = preprocess_series(pd.read_csv('gold_price.csv',index_col='DATE'))
    return gold


# In[321]:

#gold_prices = get_gold_data()
#gold_prices.head()


# In[250]:

def get_stock_exchange_data():
    #https://query1.finance.yahoo.com/v7/finance/download/%5ESTOXX50E?period1=148318920
    SP500 = preprocess_series(pd.read_csv('SP500.csv',index_col='DATE')) 
    Nasdaq = preprocess_series(pd.read_csv('Nasdaq.csv',index_col='DATE'))
    nikkei = preprocess_series(pd.read_csv('NIKKEI225.csv',index_col='DATE'))
    ftse = preprocess_series(pd.read_csv('FTSE100.csv',index_col='DATE'))
    eurostoxx = preprocess_series(pd.read_csv('Eurostoxx_50.csv',index_col='DATE'))
    Vix = preprocess_series(pd.read_csv('VIX.csv',index_col='DATE'))
    dow_jones = preprocess_series(pd.read_csv('Dow_Jones.csv',index_col='DATE'))
    Sse = preprocess_series(pd.read_csv('SSE.csv',index_col='DATE'))
    
    stock_exchange_data = pd.concat([SP500,Nasdaq,nikkei,ftse,eurostoxx,Vix,dow_jones,Sse],axis=1)
    stock_exchange_data.columns = ['SP500','Nasdaq','Nikkei','Ftse','Eurostoxx','Vix','DowJones','Sse']
    return stock_exchange_data


# stock_indices = get_stock_exchange_data()
# stock_indices.head()

# In[329]:

def get_blockchain_info():
    start = datetime.datetime(2017, 1, 1)
    end = datetime.datetime(2018, 3, 23)
    freq='1H'
    index = pd.date_range(start, end,freq=freq)
    data_dict = dict()
    keys = [('BCHAIN/DIFF','difficulty'),('BCHAIN/AVBLS','average_block_size'),('BCHAIN/ATRCT','median_confirm_time'),            ('BCHAIN/MIREV','miner_revenue'),('BCHAIN/HRATE','hash_rate'),('BCHAIN/CPTRV','cost_%_trans_vol'),            ('BCHAIN/NTRBL','trans/block'),('BCHAIN/MKTCP','market_cap'),('BCHAIN/ETRVU','est_trans_vol_usd')] 
    for key,name in keys:
        preprocessed_series = preprocess_series(quandl.get(key, start_date='2017-01-01', end_date='2018-03-23'))
        flattened_array = np.concatenate(preprocessed_series.round(2).values).ravel()
        data_dict[name] = flattened_array
    blockchain_features = pd.DataFrame.from_dict(data_dict,orient='columns')
    blockchain_features.index = index
    confirmed_transactions = preprocess_series(pd.read_csv('confirmed_transactions.csv',index_col='DATE'))
    blockchain_features = pd.concat([blockchain_features,confirmed_transactions],axis=1)
    return blockchain_features


# blk = get_blockchain_info()
# blk.info()

# blk.head()

# complete_dataset = pd.concat([exchange_data,crude_oil,gold_prices,stock_indices,blk],axis=1)

# complete_dataset.head()

# In[ ]:



