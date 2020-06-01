import dash
import json
import os
import datetime
import pandas as pd
# dbi = dynamo.DBInterface(profile_name='prod', n_processes=8)

# # ss = dbi.students.all('phone,name,aggregates,class_code,student_pin,teacher,schoolCode')
# user_store = dbi.classes.get_by_school(
#             school_code='ZGOBJP',
#             projection='code,schoolCode,aggregates')
# os.chdir('C:/Users/chris/Desktop/studycat')
# with open('Copy of rise_2020-04-08.json') as f:
#     data = json.loads(f.read())
# data=data[0]
df = pd.read_csv('https://raw.githubusercontent.com/chrisyeh09111/flying-dog-beers/master/hello.csv')
df['aggregates']=df['aggregates'].apply(lambda x:json.loads(x.replace("\'","\"")))


import dash_core_components as dcc
import dash_html_components as html
available_indicators = df['name'].unique()

available_indicators1 = ['Progress Through Curriculum','Average Score','Number of Plays','Average Play Time (secs)','Average Student Play Time (secs)','Total Play Time (secs)']

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.layout = html.Div([
    dcc.Tabs(id='tabs-example', value='daily', children=[
        dcc.Tab(label='Daily', value='daily'),
        dcc.Tab(label='Weekly', value='weekly'),
        dcc.Tab(label='Monthly', value='monthly'),        
    ]),
    
    
    
    dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='GN_L3_B'
            ),dcc.RadioItems(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators1],
                value='as'
            )
                       
                       
                       
                       
                       
                       ,
                dcc.Graph(id='indicator-graphic')
    
            
    
])
@app.callback(
    dash.dependencies.Output('indicator-graphic', 'figure'),
    [
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('xaxis-column', 'value'),   
     dash.dependencies.Input('tabs-example', 'value')
    ])
def update_graph(yaxis_column, xaxis_column, tabs_exp):

    df1 = df[df['name']==yaxis_column]
    
    df1 = df1.reset_index()['aggregates'][0][tabs_exp]
    df1=pd.DataFrame(df1)
    if tabs_exp=='monthly':
        temp='m'
        df1['m']=df1['m'].apply(lambda x :int(x[-2:]))
    elif tabs_exp=='weekly':
        temp='w'
    else:
        temp= 'day'
    return {
        'data': [
               {'x': df1[temp], 'y':df1[xaxis_column], 'type': 'bar', 'name': 'SF'},
            ],
        'layout': {'title': 'Dash Data Visualization'
                   
                   
             }}
            

if __name__ == '__main__':
    app.run_server()
