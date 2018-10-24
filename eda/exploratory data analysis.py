
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from bokeh.plotting import figure, output_file, show
from bokeh.layouts import gridplot
from bokeh.palettes import viridis
from bokeh.io import output_notebook
from bokeh.models import ColumnDataSource,HoverTool,LinearAxis, Range1d
import matplotlib as mpl
import seaborn as sns
from fastdtw import fastdtw
from sklearn import preprocessing


# In[2]:

data = pd.read_csv('training_data.csv')


# In[3]:

data.info()


# we have a total of 26 columns here,the names of which are fairly self explanatory,comprising of
# exchange rates,stock indices,gold and crude_oil price and blockchain info along with the bitcoin price.
# 
# The date range is from 1st jan 2017 to 23rd mar 2018 giving us 10705 rows.
# the data was already cleaned therefore is devoid of any null values.

# In[4]:

data['Date'] = pd.to_datetime(data['Date'])


# In[5]:

#we would be defining some helpful functions here for our analysis
def normalize_series(series):
    normalized = (series - series.mean()) / (series.max() - series.min())
    return normalized

def generate_bokeh_plots(df,feature_list):
    source = ColumnDataSource(df)
    for feature in feature_list:
        if feature != 'Price':
            p = figure(plot_width=800, plot_height=250, x_axis_type="datetime",title=feature.upper())
            p.line('Date', feature, color='navy', alpha=0.5,source=source)
            p.line('Date','Price', color='red', alpha=0.9,source=source)
            show(p)
        
def correlation_plot(df):
    corr = df.corr()
    sns.heatmap(corr,cmap='binary_r',annot=True)
    plt.show()

def dtw_similarity(df):
    exc_dict = {key:fastdtw(np.array(df[key]),np.array(df['Price']))[0] for key in df.columns if key not in ['Price','Date']}
    s = pd.Series([value for value in exc_dict.values()], index=exc_dict.keys())
    return s.round(3)
        


# In[6]:

#let us check the mean and interquartile ranges of these columns


# In[7]:

data.describe().round(3)


# lets draw box plots for exchange data along with the price
# we need to normalise the data though as the jpy exchange rate has different range

# In[8]:

sns.distplot(data['Price'])
plt.show()


# #let us check the distribution of our bitcoin price
# #the data is right skewed as we can see from the figure
# #let us also check the log price to see the distribution

# In[9]:

sns.distplot(np.log(data['Price']))
plt.show()


# In[11]:

output_notebook()


# In[12]:

exchange_list = ['eur','cny','chf','gbp','jpy','Price']
exchange_data = normalize_series(data[exchange_list])
exchange_data['Date'] = data['Date']


# In[13]:

exchange_data.plot(kind='box')
plt.show()


# In[14]:

generate_bokeh_plots(exchange_data,exchange_list)


# #we can observe that the two time series behave similarly from Dec 17 onward.
# #we can observe this pattern in every exchange rate time-series vs price charts
# #let us examine the correlation table as well

# In[15]:

correlation_plot(exchange_data)


# the correlation values confirm that the values behave similarly but have a negative correlation

# In[16]:

source = ColumnDataSource(exchange_data)
p1 = figure(title='eur')
p2 = figure(title='cny')
p3 = figure(title='chf')
p4 = figure(title='gbp')
p5 = figure(title='jpy')

colors = viridis(5)

p1.circle('Price','eur', size=3, color=colors[0],source=source)
p2.circle('Price','cny', size=3, color=colors[1],source=source)
p3.circle('Price','chf', size=3, color=colors[2],source=source)
p4.circle('Price','gbp', size=3, color=colors[3],source=source)
p5.circle('Price','jpy', size=3, color=colors[4],source=source)

grid = gridplot([p1, p2, p3, p4, p5], ncols=3, plot_width=250, plot_height=250)
show(grid)


# # Dynamic Time Warping

# Dynamic Time Warping
# Dynamic time warping finds the optimal non-linear alignment between two time series. The Euclidean distances between alignments are then much less susceptable to pessimistic similarity measurements due to distortion in the time axis. There is a price to pay for this, however, because dynamic time warping is quadratic in the length of the time series used.
# 
# Dynamic time warping works in the following way. Consider two time series Q and C of the same length n where
# Q=q1,q2,...,qn
# and
# C=c1,c2,...,cn
# The first thing we do is construct an n×n matrix whose i,jth element is the Euclidean distance between qi and cj. We want to find a path through this matrix that minimizes the cumulative distance. This path then determines the optimal alignment between the two time series. It should be noted that it is possible for one point in a time series to be mapped to multiple points in the other time series.
# 

# In[17]:

#let us compute the similarity measures between exchange and the price and see how they compare
#we would be using the Dynamic time warping algorithm to compute the distance between the two time series
exchange_data_dtw = dtw_similarity(exchange_data)


# #let's move our attention towards the stock indices,the crude_oil and gold price
# #starting with the crude_oil and gold prices

# In[18]:

crude_oil_list = ['crude_oil','Gold','Price']
crude_oil_gold = normalize_series(data[crude_oil_list])
crude_oil_gold['Date'] = data['Date']


# In[19]:

generate_bokeh_plots(crude_oil_gold,crude_oil_list)


# #we can observe that as the bitcoin price started going up dec 17 we can see a decrease in both the gold and oil prices
# #behaving quite opposite to the price of bitcoin

# In[20]:

correlation_plot(crude_oil_gold)


# In[21]:

source = ColumnDataSource(crude_oil_gold)
p1 = figure(title='crude_oil')
p2 = figure(title='Gold')

colors = viridis(2)

p1.circle('Price','crude_oil', size=3, color=colors[0],source=source)
p2.circle('Price','Gold', size=3, color=colors[1],source=source)


grid = gridplot([p1, p2], ncols=2, plot_width=250, plot_height=250)
show(grid)


# In[22]:

crude_oil_gold_dtw = dtw_similarity(crude_oil_gold)


# lets move further towards the stock indices data

# In[23]:

stock_indices_list = ['SP500','Nasdaq','Nikkei','Ftse','Eurostoxx','Vix','DowJones','Sse','Price']
stock_indices = normalize_series(data[stock_indices_list])
stock_indices['Date'] = data['Date']


# In[37]:

generate_bokeh_plots(stock_indices,stock_indices_list)


# One distinctive observation that we can make from the above plots is that from the period starting roughly from 
# 15th january 2018 onwards,we notice that some of the the stock indices and the price behave similar to each other,specifically falling and rising together.
# 
# As we turn our attention towards the VIX vs price plot,we find that the series' move in the opposite directions
# roughly around the start of february 2018,we see a fall in the bitocin price and a sharp rise in the VIX index.
# Since, the VIX index measures the volatility in the market or an investor's gauge of fear,we see that there is a sharp increase in the VIX index(scores more than 35 which indicate volatility) and a fall in the bitcoin prices.
# 
# This could be owing to the volatility in the market at that time.
# 

# In[25]:

stock_indices.hist()
plt.show()


# In[26]:

correlation_plot(stock_indices)


# almost all of the stock indices have a positive correlation with the bitcoin price
# although correlation is not causation, this tells us that stock indices and the bitcoin price are behaving similarly overall.
# since the stock indices are an indicator of economies of the countries that they are based on,this gives us an idea on the adoption and usage of bitcoin in a country with respect to their respective economies.

# In[27]:

source = ColumnDataSource(stock_indices)
p1 = figure(title='SP500')
p2 = figure(title='Nasdaq')
p3 = figure(title='Nikkei')
p4 = figure(title='Ftse')
p5 = figure(title='Eurostoxx')
p6 = figure(title='Vix')
p7 = figure(title='DowJones')
p8 = figure(title='Sse')


colors = viridis(8)

p1.circle('Price','SP500', size=3, color=colors[0],source=source)
p1.xaxis.axis_label = "Price"
p1.yaxis.axis_label = "SP500"
p2.circle('Price','Nasdaq', size=3, color=colors[1],source=source)
p2.xaxis.axis_label = "Price"
p2.yaxis.axis_label = "Nasdaq"
p3.circle('Price','Nikkei', size=3, color=colors[2],source=source)
p3.xaxis.axis_label = "Price"
p3.yaxis.axis_label = "Nikkei"
p4.circle('Price','Ftse', size=3, color=colors[3],source=source)
p4.xaxis.axis_label = "Price"
p4.yaxis.axis_label = "Ftse"
p5.circle('Price','Eurostoxx', size=3, color=colors[4],source=source)
p5.xaxis.axis_label = "Price"
p5.yaxis.axis_label = "Eurostoxx"
p6.circle('Price','Vix', size=3, color=colors[5],source=source)
p6.xaxis.axis_label = "Price"
p6.yaxis.axis_label = "Vix"
p7.circle('Price','DowJones', size=3, color=colors[6],source=source)
p7.xaxis.axis_label = "Price"
p7.yaxis.axis_label = "DowJones"
p8.circle('Price','Sse', size=3, color=colors[7],source=source)
p8.xaxis.axis_label = "Price"
p8.yaxis.axis_label = "Sse"

grid = gridplot([p1, p2, p3, p4, p5,p6,p7,p8], ncols=2, plot_width=250, plot_height=250)
show(grid)


# In[28]:

stock_indices_dtw = dtw_similarity(stock_indices)


# In[29]:

blockchain_list = ['average_block_size','cost_%_trans_vol','difficulty','est_trans_vol_usd','hash_rate','market_cap','median_confirm_time','miner_revenue','trans/block','confirmed_transactions','Price']
blockchain_info = normalize_series(data[blockchain_list])
blockchain_info['Date'] = data['Date']


# In[38]:

generate_bokeh_plots(blockchain_info,blockchain_list)


# In[31]:

correlation_plot(blockchain_info)


# In[32]:

source = ColumnDataSource(blockchain_info)
p1 = figure(title='average_block_size')
p2 = figure(title='cost_%_trans_vol')
p3 = figure(title='difficulty')
p4 = figure(title='est_trans_vol_usd')
p5 = figure(title='hash_rate')
p6 = figure(title='market_cap')
p7 = figure(title='median_confirm_time')
p8 = figure(title='trans/block')
p9 = figure(title='confirmed_transactions')

colors = viridis(9)

p1.circle('Price','average_block_size', size=3, color=colors[0],source=source)
p1.xaxis.axis_label = "Price"
p1.yaxis.axis_label = "average_block_size"

p2.circle('Price','cost_%_trans_vol', size=3, color=colors[1],source=source)
p2.xaxis.axis_label = "Price"
p2.yaxis.axis_label = "cost_%_trans_vol"

p3.circle('Price','difficulty', size=3, color=colors[2],source=source)
p3.xaxis.axis_label = "Price"
p3.yaxis.axis_label = "difficulty"

p4.circle('Price','est_trans_vol_usd', size=3, color=colors[3],source=source)
p4.xaxis.axis_label = "Price"
p4.yaxis.axis_label = "est_trans_vol_usd"

p5.circle('Price','hash_rate', size=3, color=colors[4],source=source)
p5.xaxis.axis_label = "Price"
p5.yaxis.axis_label = "hash_rate"

p6.circle('Price','market_cap', size=3, color=colors[5],source=source)
p6.xaxis.axis_label = "Price"
p6.yaxis.axis_label = "market_cap"

p7.circle('Price','median_confirm_time', size=3, color=colors[6],source=source)
p7.xaxis.axis_label = "Price"
p7.yaxis.axis_label = "median_confirm_time"

p8.circle('Price','trans/block', size=3, color=colors[7],source=source)
p8.xaxis.axis_label = "Price"
p8.yaxis.axis_label = "trans/block"

p9.circle('Price','confirmed_transactions', size=3, color=colors[8],source=source)
p9.xaxis.axis_label = "Price"
p9.yaxis.axis_label = "confirmed_transactions"

grid = gridplot([p1, p2, p3, p4, p5,p6,p7,p8,p9], ncols=3, plot_width=250, plot_height=250)
show(grid)


# In[33]:

blockchain_dtf = dtw_similarity(blockchain_info)


# In[34]:

combined_df = pd.concat([exchange_data_dtw,crude_oil_gold_dtw,stock_indices_dtw,blockchain_dtf])


# In[35]:

combined_df.sort_values().plot(kind='bar')
plt.show()


# this bar chart shows the various features and the distance values using dynamic time warping algorithm
# 
# as a measure of similarity between their time series and the bitcoin price in ascending order.
# 
# the exchange rates have the highest dissimilarity with the bitcoin price.

# 
