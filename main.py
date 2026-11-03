import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly.express as px
import dash
from dash import Dash,html,dcc,Input,Output
# import data
deliveries=pd.read_csv("Dataset/deliveries.csv")
matches=pd.read_csv('Dataset/matches.csv')
# merge data
matches=matches.rename(columns={'id':'match_id'})
dataset=deliveries.merge(matches,on='match_id')
# reducing dataset to top 10 batsman acc. to run score
hghstrun=dataset.groupby('batsman')['batsman_runs'].sum().sort_values(ascending=False).head(10).reset_index()
hghstrun=hghstrun.set_index('batsman')
# clean data containing only highest run scorer 
dataset=dataset[dataset['batsman'].isin(hghstrun.index)]

# linking external bootstrap
external_stylesheets = [
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
]

# creating dash app obj
app=dash.Dash(__name__,external_stylesheets=external_stylesheets)

# option selection dropdown
option=[]
for i in dataset['batsman'].unique():
    option.append({'label':i,'value':i})

app.layout=html.Div([
    html.Div([
        html.H2('Bats-Man Year Wise Run Analysis',style={'text-align':'center'})
    ],className='row'),
    html.Div([
        html.Div([
            dcc.Dropdown(id='choose',options=option,value='V Kohli'),
            dcc.Graph(id='plotgraph')
            

        ],className='col-md-12')
    ],className='row')
],className='container')
@app.callback(Output('plotgraph','figure'),Input('choose','value'))
def drawing(value):
    rearrange=dataset[dataset['batsman']==value]
    graphvalue=rearrange.groupby('season')['batsman_runs'].sum().reset_index()
    figure=go.Figure(data=go.Bar(x=graphvalue['season'],y=graphvalue['batsman_runs']),layout=go.Layout(title='Batsman Runs'))
    return figure
server = app.server
if __name__=='__main__':
    app.run(debug=True)
