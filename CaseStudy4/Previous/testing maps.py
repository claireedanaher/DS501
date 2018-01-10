import plotly
import pandas as pd

df = pd.read_csv('city_summary.csv')

for col in df.columns:
    df[col] = df[col].astype(str)


scl = [[0.0, 'rgb(255,237,221)'],[0.2, 'rgb(255,174,104)'],[0.4, 'rgb(255,162,81)'],\
            [0.6, 'rgb(255,157,71)'],[0.8, 'rgb(255,139,38)'],[1.0, 'rgb(255,119,0)']]



df['text'] = df['state'] + '<br>' + 'Top City: ' +df['City'] + '<br>' + 'Top Genre:  ' + df['Top Genre'] + '<br>' + 'Tags: ' + df['Tags']

data = [ dict(
        type='choropleth',
        colorscale = scl,
        autocolorscale = False,
        locations = df['code'],
        z = df['ranking_value'].astype(float),
        locationmode = 'USA-states',
        text = df['text'],
        marker = dict(
            line = dict (
                color = 'rgb(255,255,255)',
                width = 2
            ) ),
        colorbar = dict(
            title = "Ranking Value")
        ) ]

layout = dict(
        title = '2017 Aggregated Soundcloud Listening Data by State<br>(Hover for breakdown)',
        geo = dict(
            scope='usa',
            projection=dict( type='albers usa' ),
            showlakes = True,
            lakecolor = 'rgb(255, 255, 255)'),
             )
    
fig = dict( data=data, layout=layout )
plotly.offline.plot( fig, filename='d3-cloropleth-map' )