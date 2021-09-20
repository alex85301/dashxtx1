#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 21:17:10 2020

@author: alexbaverstock
"""

import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import yfinance as yf 

df_wide1 = yf.download("ATEC.AX APT.AX ALC.AX ALU.AX APX.AX AMS.AX AD8.AX BTH.AX BVS.AX CAR.AX CAT.AX CL1.AX CDA.AX CPU.AX DTL.AX DHG.AX DUB.AX ELO.AX EML.AX FCL.AX HSN.AX IFM.AX IRI.AX IRE.AX KGN.AX 360.AX LNK.AX LVT.AX MP1.AX NEA.AX NET.AX NXT.AX OTW.AX PCK.AX PPS.AX PME.AX PPH.AX REA.AX RBL.AX RAP.AX RHP.AX TNE.AX VHT.AX WEB.AX WTC.AX XRO.AX",
                    start="2020-03-01", end="2022-09-09")
df_wide1 = df_wide1[['Close']]
df_wide1 = df_wide1.reset_index()
df = df_wide1=pd.melt(df_wide1, id_vars=['Date'])
#print(df_long.head(20))

# Initiali
dash_app = dash.Dash()
app = dash_app.server
#app = dash.Dash(__name__)
#app.config.suppress_callback_exceptions = True

def get_options(list_stocks):
    dict_list = []
    for i in list_stocks:
        dict_list.append({'label': i, 'value': i})

    return dict_list

dash_app.layout = html.Div(
    children=[
        html.Div(className='row',
                 children=[
                    html.Div(className='four columns div-user-controls',
                             children=[
                                 html.H2('DASH ASX XTX TECH INDEX'),
                                 html.P('Visualising time series with Plotly - Dash.'),
                                 html.P('Pick one or more stocks from the dropdown below.'),
                                 html.Div(
                                     className='div-for-dropdown',
                                     children=[
                                         dcc.Dropdown(id='stockselector', options=get_options(df['variable_1'].unique()),
                                                      multi=True, value=[df['variable_1'].sort_values()[0]],
                                                      style={'backgroundColor': '#1E1E1E'},
                                                      className='stockselector'
                                                      ),
                                     ],
                                     style={'color': '#1E1E1E'})
                                ]
                             ),
                    html.Div(className='eight columns div-for-charts bg-grey',
                             children=[
                                 dcc.Graph(id='timeseries', config={'displayModeBar': True}, animate=True)
                             ])
                              ])
        ]

)


# Callback for timeseries price
@dash_app.callback(Output('timeseries', 'figure'),
              [Input('stockselector', 'value')])
def update_graph(selected_dropdown_value):
    trace1 = []
    df_sub = df
    for stock in selected_dropdown_value:
        trace1.append(go.Scatter(x=df_sub[df_sub['variable_1'] == stock].Date,
                                 y=df_sub[df_sub['variable_1'] == stock]['value'],
                                 mode='lines',
                                 opacity=0.7,
                                 name=stock,
                                 textposition='bottom center'))
    traces = [trace1]
    data = [val for sublist in traces for val in sublist]
    figure = {'data': data,
              'layout': go.Layout(
                  colorway=["#5E0DAC", '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
                  template='plotly_dark',
                  paper_bgcolor='rgba(0, 0, 0, 0)',
                  plot_bgcolor='rgba(0, 0, 0, 0)',
                  margin={'b': 15},
                  hovermode='x',
                  autosize=True,
                  title={'text': 'Stock Prices', 'font': {'color': 'white'}, 'x': 0.5},
                  #xaxis={'range': [df_sub.index.min(), df_sub.index.max()]},
              ),

              }

    return figure


if __name__ == '__main__':
    dash_app.run_server(True)
