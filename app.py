import dash
import json
import os
import datetime
import pandas as pd
data=pd.read_csv('https://raw.githubusercontent.com/chrisyeh09111/flying-dog-beers/master/export_dataframe_cut.csv')
data['date'] = pd.to_datetime(data.date, unit='ms')
data['date1']=data['date'].apply(lambda x:pd.to_datetime(x).date())
data['year']=data['date1'].apply(lambda x :x.year)
data['month']=data['date1'].apply(lambda x :x.month)
# data['month_year'] = pd.to_datetime(data['date']).dt.to_period('M')
data=data.groupby(['year','month','date1']).agg({'dur':['sum','count','mean','nunique'], 'scr':['mean']})
data.reset_index(inplace=True) 
data['total_dur']=data['dur']['sum']
data['no_of_plays']=data['dur']['count']
data['avg_play_time_per_day']=data['dur']['mean']
data['mean_score']=data['scr']['mean']
data['number_of_students']=data['dur']['nunique']
data['avg_play_day']=data['no_of_plays']/data['number_of_students']

import dash_core_components as dcc
import dash_html_components as html
import json
available_indicators = ['total_dur','no_of_plays','avg_play_time_per_day','mean_score','avg_play_day','number_of_students']

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.layout = html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='total_dur'
            )
    ,

    dcc.Graph(id='indicator-graphic'),

    dcc.Slider(
                id='xaxis-column',
                        
                min=data['year'].min(),
                max=data['year'].max(),
                marks={str(year): str(year) for year in data['year'].unique()},
                step=None,
                value= 2019
            ),
    dcc.Slider(
                id='zaxis-column',
                        
                min=data['month'].min(),
                max=data['month'].max(),
                marks={str(year): str(year) for year in data['month'].unique()},
                step=None,
                value= 1
            )
])
@app.callback(
    dash.dependencies.Output('indicator-graphic', 'figure'),
    [
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('zaxis-column', 'value')   
    ])
def update_graph( yaxis_column_name,xaxis_column_name,zaxis_column_name):
    df=data[data['year']==xaxis_column_name]
    df=df[df['month']==zaxis_column_name]
    
    return {
        'data': [
               {'x': df['date1'], 'y':df[yaxis_column_name], 'type': 'bar', 'name': 'SF'},
            ],
        'layout': {'title': 'Dash Data Visualization'
                   
                   
             }}
            

if __name__ == '__main__':
    app.run_server()
