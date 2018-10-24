
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
from preprocess_and_data_collection import preprocess_series


# #we would be averaging bitcoin prices from 01-01-2017 to 23-03-2017 for these popular exchanges
# BTCC(China)
# Kraken(UK)
# Bitstamp(US and UK)
# GDAX(US)

# In[13]:

BTCC_unp = pd.read_csv('BTCC.csv',index_col='DATE')
kraken_unp = pd.read_csv('kraken.csv',index_col='DATE')
bitstamp_unp = pd.read_csv('bitstamp_hourly.csv',index_col='DATE')
GDAX_unp = df=pd.read_csv('GDAX.csv',index_col='DATE')


# In[14]:

BTCC = preprocess_series(BTCC_unp)
kraken = preprocess_series(kraken_unp)
bitstamp = preprocess_series(bitstamp_unp)
GDAX = preprocess_series(GDAX_unp)


# In[27]:

bitcoin_price = (BTCC + kraken + bitstamp + GDAX) / 4


# In[32]:

#bitcoin_price.isnull().sum()


# In[31]:

#bitcoin_price.head()


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



