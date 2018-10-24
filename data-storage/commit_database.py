
# coding: utf-8

# In[46]:

import sqlite3
import pandas as pd
import preprocess_and_data_collection as pdc
import bitcoin_price_portfolio as bpp


# In[2]:

#creating a database
def create_database(db_name):
    try:
        conn = sqlite3.connect(db_name)
    except Error as e:
        print(e)
    finally:
        conn.close()


# In[4]:

create_database('project_data.db')


# In[7]:

exchange_data = pdc.get_exchange_data()


# In[11]:

crude_oil = pdc.get_crudeoil_data()


# In[12]:

gold_price = pdc.get_gold_data()


# In[13]:

stock_exchange = pdc.get_stock_exchange_data()


# In[14]:

blockchain = pdc.get_blockchain_info()


# In[16]:

def get_basic_info(df):
    print(df.shape)
    print(df.isnull().sum())
    print(df.info())
    print(df.dtypes)
    


# In[20]:

for dt in [exchange_data,crude_oil,gold_price,stock_exchange,blockchain]:
    get_basic_info(dt)


# In[21]:

conn = sqlite3.connect('project_data.db')


# In[26]:

dataset_list = [exchange_data,crude_oil,gold_price,stock_exchange,blockchain]


# In[23]:

table_names = ['exchange_data','crude_oil','gold_price','stock_exchange','blockchain']


# In[30]:

for table_name,dataset in zip(table_names,dataset_list):
    dataset.to_sql(table_name,conn,if_exists='replace')
   


# In[33]:

c = conn.cursor()
c.execute("Select name from sqlite_master")
c.fetchall()


# In[42]:

for table in table_names:
    c.execute("select count(*) from {}".format(table_name))
    print(c.fetchone())


# In[44]:

def check_database(db_name):
    con = sqlite3.connect(db_name)
    c = con.cursor()
    c.execute("Select name from sqlite_master")
    print(c.fetchall())
    for table in table_names:
        c.execute("select count(*) from {}".format(table_name))
        print(c.fetchone())


# In[45]:

check_database('project_data.db')


# In[49]:

bpp.bitcoin_price.to_sql('bitcoin_price',conn,if_exists='replace')


# In[50]:

check_database('project_data.db')


# In[51]:




# In[ ]:



