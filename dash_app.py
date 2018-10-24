
# coding: utf-8

# In[2]:

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd


# In[3]:

app = dash.Dash(__name__)
app.config['suppress_callback_exceptions']=True
server = app.server


# In[13]:

hourly = pd.read_csv('hourly_prediction.csv',index_col='DATE')
hourly.index = pd.to_datetime(hourly.index)
daily = pd.read_csv('daily_prediction.csv',index_col='DATE')
daily.index = pd.to_datetime(daily.index)
RMSE_values = {'RNN_hourly':'386.07','SARIMA_hourly':'115.786','RNN_daily':'487.260','elastic_net':'601.59','XGB_daily':'1042.74'}
dtw_results = pd.read_csv('dtw_results.csv')
news_data = pd.read_csv('news_data_sentiment.csv',encoding='ISO-8859-1',index_col='DATE')
news_data.index = pd.to_datetime(news_data.index)
pos_news = news_data[news_data.event==1][news_data.sentiment >0]
neu_news = news_data[news_data.event==1][news_data.sentiment == 0]
neg_news = news_data[news_data.event==1][news_data.sentiment < 0]
neg_news['sentiment'] = pd.np.abs(neg_news['sentiment'])

def get_menu():
    menu = html.Div([

        dcc.Link('Results   ', href='/results', className="results tab"),

        dcc.Link('analysis   ', href='/analysis', className="analysis tab"),


    ], className="row ")
    return menu

results = html.Div([
    get_menu(),
    html.Div([
    html.H1(children='Prediction Results')],
    style={'width': '100%', 'display': 'inline-block'}),
    
    html.Div([
    dcc.Dropdown(id='model options',
                options=[
            {'label': u'RNN-24H', 'value': 'RNN_hourly'},
            {'label': u'SARIMA-24H', 'value': 'SARIMA_hourly'},
            {'label': u'ELASTIC NET', 'value': 'elastic_net'},
            {'label': u'RNN-Daily', 'value': 'RNN_daily'},
            {'label': u'XGBoost-Daily', 'value': 'XGB_daily'}
        ],
        value = 'RNN_hourly')],
    style={'width': '400', 'display': 'inline-block'}),
    

    html.Div(id='rmse'),
    #style={'width': '400', 'display': 'inline-block'},
    
    dcc.Graph(
        id='predictions')
    #dcc.Graph(
        #id='residuals')
])

@app.callback(
    dash.dependencies.Output(component_id='rmse', component_property='children'),
    [dash.dependencies.Input(component_id='model options', component_property='value')]
)

def update_rmse(model):
    return 'RMSE value:{}'.format(RMSE_values[model])

@app.callback(
    dash.dependencies.Output(component_id='predictions', component_property='figure'),
    [dash.dependencies.Input(component_id='model options', component_property='value')]
)

def update_graph(selected_model):
    if selected_model in ['RNN_hourly','SARIMA_hourly']:
        trace1 = go.Scatter(
                                    x = hourly.index,
                                    y = hourly.price,
                                    line = {"color": "rgb(53, 83, 255)"},
                                    mode = "lines",
                                    name = "bitcoin price"
                                )
        trace2 = go.Scatter(
                                    x = hourly.index,
                                    y = hourly[selected_model],
                                    line = {"color": "orange"},
                                    mode = "lines",
                                    name = selected_model
                                )

    else:
        trace1 = go.Scatter(
                                    x = daily.index,
                                    y = daily.price,
                                    line = {"color": "rgb(53, 83, 255)"},
                                    mode = "lines",
                                    name = "bitcoin price"
                                )
        trace2 = go.Scatter(
                                    x = daily.index,
                                    y = daily[selected_model],
                                    line = {"color": "orange"},
                                    mode = "lines",
                                    name = selected_model
                                )
    return {'data':[trace1,trace2],
            'layout': go.Layout(
                                autosize = True,
                                #width = 700,
                                #height = 200,
                                font = {
                                    "family": "Raleway",
                                    "size": 10
                                  },
                                 margin = {
                                    "r": 40,
                                    "t": 40,
                                    "b": 30,
                                    "l": 40
                                  },
                                  showlegend = True,
                                  titlefont = {
                                    "family": "Raleway",
                                    "size": 10
                                  },
                                xaxis = {
                                    "autorange": True,
                                    #"range": ["2018-05-15", "2018-05-17"],
                                    "showline": True,
                                    "type": "date",
                                    "zeroline": False
                                  },
                               yaxis = {
                                    "autorange": True,
                                    #"range": [18.6880162434, 278.431996757],
                                    "showline": True,
                                    "type": "linear",
                                    "zeroline": False
                                  }
            )
    }

# In[12]:
analysis = html.Div([
                    get_menu(),
                    html.H1('Analysis',
                            className="header"),

                    html.H3('Dynamic Time Warping'),
                    html.P("\
                        Dynamic time warping finds the optimal non-linear alignment between two time series.\
                        The Euclidean distances between alignments are then much less susceptable to pessimistic similarity\
                        measurements due to distortion in the time axis.\
                        There is a price to pay for this, however, because dynamic time warping is quadratic in the length of the time                         series used.\
                        Dynamic time warping works in the following way-\
                        Consider two time series Q and C of the same length n where Q=q1,q2,...,qn and C=c1,c2,...,cn\
                    The first thing we do is construct an n×n matrix whose i,jth element is the Euclidean distance between qi and cj.\
                    We want to find a path through this matrix that minimizes the cumulative distance.\
                    This path then determines the optimal alignment between the two time series.\
                    It should be noted that it is possible for one point in a time series to be mapped to multiple points in the other time series.",className='dtw'),
                  dcc.Graph(id='dtw importance',
                            figure={
                                    'data':[
                                            {'x': dtw_results['Factors'], 'y': dtw_results['values'], 'type': 'bar', 'name': 'dtw'}],
                                    'layout':{
                                            #'height':200,
                                            #'width':700,
                                            'title':'Time Series Comparison with Bitcoin Price'
                                             }
                                           }),
                  html.Div([
                  dcc.Dropdown(id='sentiment options',
                  options=[
                            {'label': u'positive', 'value': 'positive'},
                            {'label': u'negative', 'value': 'negative'},
                        ],
                        value = 'positive')],
                  style=dict(width=300,display='inline-block')),
                  
                  html.Br([]),   
                  dcc.Graph(id='news events'
                            #figure={
                                    
                                               
                            #}
                           )
                  

])

@app.callback(
    dash.dependencies.Output(component_id='news events', component_property='figure'),
    [dash.dependencies.Input(component_id='sentiment options', component_property='value')]
)

def update_sentiment(sentiment):
    if sentiment == 'positive':
        trace1 = go.Scatter(
                                    x = news_data.index,
                                    y = news_data.Price,
                                    line = {"color": "rgb(53, 83, 255)"},
                                    hoverinfo = None,
                                    mode = "lines",
                                    name = "price"
                                )
        trace2 = go.Scatter(
                                    x = pos_news.index,
                                    y = pos_news.Price,
                                    line = {"color": "green"},
                                    hovertext = pos_news.title,
                                    mode = "markers",
                                    marker={'size': pos_news['sentiment']+7,
                                            'line': {'width': 0.5, 'color': 'white'}
                                           },
                                    name = "pos_news"
                                )

    else:
        trace1 = go.Scatter(
                                    x = news_data.index,
                                    y = news_data.Price,
                                    line = {"color": "rgb(53, 83, 255)"},
                                    hoverinfo = None,
                                    mode = "lines",
                                    name = "price"
                                )
        trace2 = go.Scatter(
                                    x = neg_news.index,
                                    y = neg_news.Price,
                                    line = {"color": "red"},
                                    hovertext = neg_news.title,
                                    mode = "markers",
                                    marker={'size': neg_news['sentiment']+7,
                                            'line': {'width': 0.5, 'color': 'white'}
                                           },
                                    name = "neg_news"
                                )
    return {'data':[trace1,trace2],
            'layout':{
                      'title':'News Events and Bitcoin Price'}
           }

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/' or pathname == '/results':
        return results
    elif pathname == '/analysis':
        return analysis
    #else:
        #return noPage

external_css = ["https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css",
                "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "//fonts.googleapis.com/css?family=Raleway:400,300,600",
                "https://codepen.io/bcd/pen/KQrXdb.css",
                "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"]

for css in external_css:
    app.css.append_css({"external_url": css})

external_js = ["https://code.jquery.com/jquery-3.2.1.min.js",
               "https://codepen.io/bcd/pen/YaXojL.js"]

for js in external_js:
    app.scripts.append_script({"external_url": js})
    

    
if __name__ == '__main__':
    app.run_server(debug=True)


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



