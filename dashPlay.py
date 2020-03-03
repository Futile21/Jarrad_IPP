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

###############################################################################################################################################



from plotly.validators.scatter.marker import SymbolValidator


raw_symbols = SymbolValidator().values
namestems = []
for i in range(0,len(raw_symbols),2):
    name = raw_symbols[i+1]
    namestems.append(name.replace("-open", "").replace("-dot", ""))

namestems=set(namestems)
options=[{"label": i, "value": i} for i in namestems],






Dropdown = html.Div([
    dcc.Dropdown(
        id='DropdownCase',
        options=options[0],
        value='circle',
        multi=False,
    ),
], )

Slider = html.Div([daq.Slider(
    id="slider",
    min=0,
    max=1,
    step=0.05,
    value=0.5,
    marks={'0': '0',
           '0.5': '0.5',
           '1': '1'},
    size=450,
    handleLabel={"showCurrentValue": True, "label": "VALUE"
                 },
    included=False,
    ),
    ], style={
        "height": "3vh",
    })

radios_dash = html.Div([   #['solid', 'dot', 'dash', 'longdash', 'dashdot', 'longdashdot']
    dbc.Label("Dash",
              # align="center",
              ),
    dbc.RadioItems(
        id="radios_dash",
        options=[
            {"label": "solid", "value": "solid"},
            {"label": "Dash", "value": "dash"},
            {"label": "dot", "value": "dot"},
            {"label": "Dash + dot", "value": "dashdot"},
            {"label": "longdash", "value": "longdash"},
            {"label": "longdashdot", "value": "longdashdot"},
        ],
        inline=True,
        value="solid",
        # inline=True,
    )
])


Fillswitches = html.Div([
                dbc.Checklist(
                    options=[
                        {"label": "line", "value": "line"},
                        {"label": "markers", "value": "markers"},
                    ],
                    value=['line'],
                    id="Fillswitches",
                    switch=True,
                ),])

lineW = html.Div([
        html.P("Line range 0-25"),
        dbc.Input(type="number", min=0, max=10, step=0.25,id="lineW"),],)

MarkerW = html.Div([
        html.P("Marker range 0-25"),
        dbc.Input(type="number", min=0, max=10, step=0.25,id="MarkerW"),],)

layout = {
    "title": "TEST",
    # "width": '6h',
    "height": 600,
    "legend": {
        # "x": 1.019163763066202,
        # "y": 0.5147321428571429,
        # "xref": "paper",
        # "yref": "paper",
        # "bgcolor": "rgba(255, 255, 255, 0.5)",
        "traceorder": "normal"
        },
    # "barmode": "stack",
    "autosize": False,
    "showlegend": True,
    "width": '1500',
    "xaxis": {
        'anchor': 'y',
        'domain': [0.0, 1],

        "ticks": "",
        "mirror": False,
        "showgrid": True,
        "showline": True,
        "zeroline": False,
        "autorange": True,
        # "gridcolor": "rgb(255, 255, 255)",
        # "linecolor": "rgb(34,34,34)",
        "linewidth": 2,
        "title": "Years",
    },
    "yaxis": {
        'anchor': 'x',
        'domain': [0.0, 1.0],

        "type": "linear",
        "ticks": "",
        # "domain": [0.55, 0.95],
        "mirror": False,
        "showgrid": True,
        "showline": False,
        "zeroline": False,
        # "range": [0, 16e4],
        # "gridcolor": "rgb(255, 255, 255)",
        # "linecolor": "rgb(34,34,34)",
        "linewidth": 1,
        "title": "Y Name",
        "autorange": True,
    }
    }






DF_E = IRP2019_P
DF_P = IRP2019_E





Graph=html.Div([
            dcc.Graph(
                figure=dict(
                    data=[],
                    layout=layout,
                    ),
                id='Graph',
            ),
            ])









app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP,'https://codepen.io/chriddyp/pen/bWLwgP.css'])
app.layout = html.Div(children=[
    html.Div([
        Text_GenWind,
        # costGraph,
        # costGraph2,
        dbc.Row([
            dbc.Col([
                    dbc.Row([
                            dbc.Col(Fillswitches,align="end",width={"offset": 1}),
                            dbc.Col([radios_dash],align="end",width={"offset": 1}),
                            ],
                        align='end')
                    ],
                    width={"offset": 0.5},
                    sm=2),
            dbc.Col([lineW],
                sm=2,
                width={"offset": 0}),
            dbc.Col([MarkerW],
                    sm=2,
                    width={"offset": 0}),
            dbc.Col([
                    html.Label('Markers'),
                    Dropdown,],
                    sm=2,
                    width={"offset": 0}),
            dbc.Col(Slider,
                    sm=3),
            # dbc.Col(radios_inputPie,
            #         width={"offset": 1},
            #         sm=1),

        ]),
        # subplot,
        html.Div([
                dbc.Row([
                    dbc.Col([
                        Graph,
                             ],
                        sm=10,
                        width={"offset": 1}
                    ),
                ]),
        ])
    ]

    )

])






@app.callback(Output("Graph", "figure"),
              [Input('DropdownCase', 'value'),
               Input('Fillswitches', 'value'),
               Input('lineW', 'value'),
               Input('MarkerW', 'value'),
               Input('slider', 'value'),
               Input('radios_dash', 'value'),],)
def updatePowerGraph(DropdownValue,Fillswitches,lineW,MarkerW,slider,radios_dash):
    print("hey")
    print(f'DropdownValue is {DropdownValue}')
    print(f'Fillswitches is {Fillswitches}')
    print(f'lineW is {lineW}')
    print("hey 2")
    # print(f'DropdownValue is {sliderValue}')
    # print(f'DropdownValue is {type(sliderValue)}')
    # print(f'SwitchesValue is {switchesValue}')

    #######################################

    # scenariosDict[DropdownValue]
    # DF_E = scenariosDict[DropdownValue]["Installed capacity"]
    # DF_P = scenariosDict[DropdownValue]["Energy produced"]

    traces = []

    if 'markers' in Fillswitches:
        Mode='markers'

    if 'line' in Fillswitches:
        Mode='lines'

    if ('line' in Fillswitches) and ('markers' in Fillswitches):
        Mode='lines+markers'

    # print(f'mode is {Mode}')
    for i, power in enumerate(powerlist):
        traces.append(
            go.Scatter(x=DF_P['Year'],
                y=DF_P[power],
                name=power,
                legendgroup=power,
                mode=Mode,
                marker=dict(color=colours[i],
                            size=MarkerW,
                            # symbols='x',
                            ),
                stackgroup='one',
                line={'width': lineW,
                      "dash" : radios_dash,
                     },
                fillcolor=colours[i].replace(")", f",{slider})").replace("rgb", "rgba"),
                marker_symbol=DropdownValue,
                )
        )


    # layout["title"] = DropdownValue

    figure = dict(data=traces, layout=layout)
    return figure



if __name__ == '__main__':
    app.run_server(port=8841,debug=True)

