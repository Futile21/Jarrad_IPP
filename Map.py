import dash
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output,State
import pandas as pd

import numpy as np
import dash_daq as daq
import io
import base64



from plotly import tools
from plotly.subplots import make_subplots


#
# IRP2019_P = pd.read_excel('2019-IRP.xlsx',sheet_name="IRP1_P")
#
# print(IRP2019_P["Year"])
#
# dictionary = {}
#
# sliderMarks ={}
#
#
# for i,year in enumerate((IRP2019_P["Year"])):
#     print(f"i is {year} and year is {str(year)}")
#     sliderMarks[year]={'label':str(year)}
# print(sliderMarks)

#######################################################################

line_type=['solid','longdashdot','dash','dot']

# colours_emission = [
#                 'rgb(64, 64, 63)',
#                 'rgb(2, 71, 117)',
#                 'rgb(117, 2, 2)',
#                 'rgb(237, 145, 33)',
#                 'rgb(1, 133, 4)',
#                 ]

colours_emission = [
                'hsl(0, 0%, x%)',
                'hsl(204, 97%, x%)',
                'hsl(0, 100%, x%)',
                'hsl(30, 100%, x%)',
                'hsl(120, 100%, x%)',
                ]

#######################################################################


Text_GenWind = html.Div([
    dbc.Jumbotron([
        html.H4(children='Power Graph and Rose Chart Display', ),
        html.P(children='Further analysis of the selected point on the map of South Africa is displayed in the power '
                        'graph and rose chart. The selection can be customised using the drop-down menus for hub '
                        'height(s) and turbine(s). This allows for a graphic represent of each of the selected '
                        'criteria.'),
        html.P(children='A normal distribution for each of the hub height’s selected is plotted on the graph. The axis '
                        'on the left estimates the wind probability density percentages based on time series data '
                        'collected. Power curves are plotted over the normal distribution graphs from the turbine '
                        'selections made. The power curve(s) are linked to the right axis and are displayed as power '
                        'generated (kW).'),
        html.P(children='The rose chart to the right of the graph represents the wind direction as a percentage based '
                        'on the hub height(s) selected.'),

    ])
], )





IRP2019_P = pd.read_excel('2019-IRP.xlsx',sheet_name="IRP1_P")
IRP2019_E = pd.read_excel('2019-IRP.xlsx',sheet_name="IRP1_E")
CSIR_LC_2019_P = pd.read_excel('2019-CSIR_LC.xlsx',sheet_name="IRP1_P")
CSIR_LC_2019_E = pd.read_excel('2019-CSIR_LC.xlsx',sheet_name="IRP1_E")


years = CSIR_LC_2019_E['Year']

IRP2019_P2 = (IRP2019_P * 0.8).round(1)
IRP2019_E2 = (IRP2019_E * 0.8).round(1)

CSIR_LC_2019_P2 = (CSIR_LC_2019_P * 0.8).round(1)  ########### fix 0.8 years
CSIR_LC_2019_E2 = (CSIR_LC_2019_E * 0.8).round(1)


powerlist = list(CSIR_LC_2019_E.columns)
powerlist.remove('Year')


# colours = ['#8c664a', '#ff270f', '#969696', '#e8d2ca', '#2760a6', '#9db1cf', '#eea632', '#ffed11', '#d7c700', '#007770'
                    # , '#0a346f', ]

# colours = ['#8c664a', '#ff270f', '#969696', '#e8d2ca', '#2760a6', '#9db1cf', '#eea632', '#ffed11', '#d7c700', '#007770',
#            '#dfe5ef', '#0a346f', '#4f4f4f']

colours = ['rgb(140, 102, 74)',
           'rgb(255, 39, 15)',
           'rgb(150, 150, 150)',
           'rgb(232, 210, 202)',
           'rgb(39, 96, 166)',
           'rgb(157, 177, 207)',
           'rgb(238, 166, 50)',
           'rgb(255, 237, 17)',
           'rgb(215, 199, 0)',
           'rgb(0, 119, 112)',
           'rgb(223, 229, 239)',
           'rgb(10, 52, 111)',
           'rgb(79, 79, 79)']

###############################################################################################################################################

scenariosDict = {
    'IRP2019': {"Energy produced": IRP2019_P, "Installed capacity": IRP2019_E, },
    'CSIR_LC': {"Energy produced": CSIR_LC_2019_P, "Installed capacity": CSIR_LC_2019_E, },
    'IRP2019_2': {"Energy produced": IRP2019_P2, "Installed capacity": IRP2019_E2, },
    'CSIR_LC_2': {"Energy produced": CSIR_LC_2019_P2, "Installed capacity": CSIR_LC_2019_E2, },
}



import plotly.graph_objects as go


token = "pk.eyJ1IjoiamFja2x1byIsImEiOiJjajNlcnh3MzEwMHZtMzNueGw3NWw5ZXF5In0.fk8k06T96Ml9CLGgKmk81w"

from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/south-africa.geojson') as response:
    SAD = json.load(response)

des = []
num = []

from random import random

for i in range(len(SAD['features'])):
    des.append(SAD['features'][i]['properties']['name'])
    num.append( round(10000*random()))

# des
for i, name in enumerate(des):
    #     print(i)
    SAD['features'][i]['id'] = name


DATA = go.Choroplethmapbox(
    geojson=SAD,
    locations=des,
    z=num,
    colorscale="Bluered_r",
    marker_line_width=0
                                   )

RSAlayout=dict(
                autosize=True,
                margin=go.layout.Margin(l=0, r=35, t=35, b=0,),
                colorbar=dict(title="Colorbar",),
                title="South Africa Overview",
                mapbox=dict(
                    accesstoken=token,
                    center=dict(lat=-28, lon=22),
                    style="light",
                zoom=4,),)

MAP=html.Div([
            dcc.Graph(
                figure=dict(
                    data=[DATA],
                    layout=RSAlayout,
                    ),
                id="emission"
                ),
            ],)


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP,'https://codepen.io/chriddyp/pen/bWLwgP.css'])
app.layout = html.Div(children=[
    html.Div([
        Text_GenWind,
        MAP,
    ])

])





if __name__ == '__main__':
    app.run_server(port=8842,debug=True)

