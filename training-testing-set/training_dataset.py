
# coding: utf-8

# In[1]:

import sqlite3
import pandas as pd
import numpy as np


# In[2]:

conn = sqlite3.connect('project_data.db')


# In[3]:

c = conn.cursor()


# In[4]:

c.execute("select name from sqlite_master")
c.fetchall()


# In[29]:

exchange_data = pd.read_sql_query("select * from exchange_data",conn,index_col='index',parse_dates=['index'])
exchange_data.index.names = ['Date']
exchange_data.head()


# In[30]:

crude_oil = pd.read_sql_query("select * from crude_oil",conn,index_col='index',parse_dates=['index'])
crude_oil.index.names = ['Date']
crude_oil.head()


# In[31]:

gold_price = pd.read_sql_query("select * from gold_price",conn,index_col='index',parse_dates=['index'])
gold_price.index.names = ['Date']
gold_price.head()


# In[32]:

stock_exchange = pd.read_sql_query("select * from stock_exchange",conn,index_col='index',parse_dates=['index'])
stock_exchange.index.names = ['Date']
stock_exchange.head()


# In[33]:

block_chain = pd.read_sql_query("select * from blockchain",conn,index_col='index',parse_dates=['index'])
block_chain.index.names = ['Date']
block_chain.head()


# In[43]:

bitcoin_price = pd.read_sql_query("select * from bitcoin_price",conn,index_col='index',parse_dates=['index'])
bitcoin_price.index.names = ['Date']
bitcoin_price.head()


# In[44]:

training_dataset = pd.concat([exchange_data,crude_oil,gold_price,stock_exchange,block_chain,bitcoin_price],axis=1)


# In[45]:

training_dataset.head()


# In[46]:

training_dataset.info()


# In[47]:

training_dataset.to_sql('training_data',conn,if_exists='replace')


# In[48]:

c.execute("select name from sqlite_master")
c.fetchall()


# In[49]:

training_dataset.to_csv('training_data.csv')


# In[ ]:



