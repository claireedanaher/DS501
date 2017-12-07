# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 17:02:19 2017

@author: Jonny
"""

import plotly
import plotly.plotly as py
import pandas as pd

df = pd.read_csv('soundcloud_test.csv')

for col in df.columns:
    df[col] = df[col].astype(str)

scl = [[0.0, 'rgb(255,180,0)'],[0.2, 'rgb(255,165,0)'],[0.4, 'rgb(255,150,0)'],\
            [0.6, 'rgb(255,135,0)'],[0.8, 'rgb(255,110,0)'],[1.0, 'rgb(255,100,0)']]

df['text'] = df['state'] + '<br>' + 'Top City: ' +df['City'] + '<br> ' + 'Number of Listeners: ' + df['total Hits']

data = [ dict(
        type='choropleth',
        colorscale = scl,
        autocolorscale = False,
        locations = df['code'],
        z = df['total Hits'].astype(float),
        locationmode = 'USA-states',
        text = df['text'],
        marker = dict(
            line = dict (
                color = 'rgb(255,255,255)',
                width = 2
            ) ),
        colorbar = dict(
            title = "Listeners")
        ) ]

layout = dict(
        title = '2017 Aggregated Soundcloud Listeners by State<br>(Hover for breakdown)',
        geo = dict(
            scope='usa',
            projection=dict( type='albers usa' ),
            showlakes = True,
            lakecolor = 'rgb(255, 255, 255)'),
             )
    
fig = dict( data=data, layout=layout )
plotly.offline.plot( fig, filename='d3-cloropleth-map' )