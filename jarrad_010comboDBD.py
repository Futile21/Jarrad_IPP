# Layout updating

import os
from pathlib import Path
import dash
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
import dash_daq as daq
import io
import base64
import dash_table

IRP2019_P = pd.read_excel('2019-IRP.xlsx', sheet_name="IRP1_P").round(1)
IRP2019_E = pd.read_excel('2019-IRP.xlsx', sheet_name="IRP1_E").round(1)

CSIR_LC_2019_P = pd.read_excel('2019-CSIR_LC.xlsx', sheet_name="IRP1_P").round(1)
CSIR_LC_2019_E = pd.read_excel('2019-CSIR_LC.xlsx', sheet_name="IRP1_E").round(1)


IRP2019_P2 = (IRP2019_P * 0.8).round(1)
IRP2019_E2 = (IRP2019_E * 0.8).round(1)

CSIR_LC_2019_P2 = (CSIR_LC_2019_P * 0.8).round(1)
CSIR_LC_2019_E2 = (CSIR_LC_2019_E * 0.8).round(1)

IRP2019_P2['Year']=IRP2019_P['Year']
IRP2019_E2['Year']=IRP2019_P['Year']

CSIR_LC_2019_P2['Year']=IRP2019_P['Year']
CSIR_LC_2019_E2['Year']=IRP2019_P['Year']

powerlist = list(CSIR_LC_2019_E.columns)
print(powerlist)
powerlist.remove('Year')
print(powerlist)
years = CSIR_LC_2019_E['Year']


# tracebar = []  # colorcop

# colours=["rgb(128, 43, 0)",    # COA
#          "rgb(0, 153, 0)",     # NUC
#          "rgb(255, 255, 0)",   # GAS
#          "rgb(255, 102, 0)",   # PEA
#          "rgb(0, 102, 102)",   # HYD
#          "rgb(0, 102, 255)",   # WIN
#          "rgb(204, 0, 153)",   # CSP
#          "rgb(204, 0, 0)",     # SPV
#          "rgb(0, 102, 102)",   # DPV
#          "rgb(51, 51, 51)",    # BIO
#          "rgb(64, 255, 0)",    # PST
# ]
#               1           2           3       4           5           6           7           8       9           10
# colours = ['#8c664a', '#ff270f', '#969696', '#e8d2ca', '#2760a6', '#9db1cf', '#eea632', '#ffed11', '#d7c700', '#007770',
#            '#dfe5ef', '#0a346f', '#4f4f4f']
#               11          12      13
# colours = ['#8c664a', '#ff270f', '#969696', '#e8d2ca', '#2760a6', '#9db1cf', '#eea632', '#ffed11', '#d7c700', '#007770'
#                     , '#0a346f', ]


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

navbar = html.Div([dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("CSIR", href="https://www.csir.co.za/")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("More pages", header=True),
                dbc.DropdownMenuItem("More Info", href=""),
                dbc.DropdownMenuItem("Nothing", href=""),
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),
    ],
    brand="Installed capacity and Energy produced thing",
    brand_style={'font-size': 35},
    color="primary",
    dark=True, )])

DropdownCase_Allyear = html.Div([
    dcc.Dropdown(
        id='DropdownCase_Allyear',
        options=[
            {"label": "IPP 2019", "value": 'IRP2019'},
            {"label": "CSIR 2019", "value": 'CSIR_LC'},
            {"label": "IPP 2019 2", "value": 'IRP2019_2'},
            {"label": "CSIR 2019 2", "value": 'CSIR_LC_2'},
        ],
        value='IRP2019',
        multi=False,
    ),
], )

DropdownCase_Oneyear = html.Div([
    dcc.Dropdown(
        id='DropdownCase_Oneyear',
        options=[
            {"label": "IPP 2019", "value": 'IRP2019'},
            {"label": "CSIR 2019", "value": 'CSIR_LC'},
            {"label": "IPP 2019 2", "value": 'IRP2019_2'},
            {"label": "CSIR 2019 2", "value": 'CSIR_LC_2'},
        ],
        value='IRP2019',
        multi=False,
    ),
], )

DropdownCase_Pie = html.Div([
    dcc.Dropdown(
        id='DropdownCase_pie',
        options=[
            {"label": "IPP 2019", "value": 'IRP2019'},
            {"label": "CSIR 2019", "value": 'CSIR_LC'},
            {"label": "IPP 2019 2", "value": 'IRP2019_2'},
            {"label": "CSIR 2019 2", "value": 'CSIR_LC_2'},
        ],
        value='IRP2019',
        multi=False,
    ),
], )

DropdownCase_Cost = html.Div([
    dcc.Dropdown(
        id='DropdownCase_Cost',
        options=[
            {"label": "IPP 2019", "value": 'IRP2019'},
            {"label": "CSIR 2019", "value": 'CSIR_LC'},
            {"label": "IPP 2019 2", "value": 'IRP2019_2'},
            {"label": "CSIR 2019 2", "value": 'CSIR_LC_2'},
        ],
        value=['IRP2019'],
        multi=True,
    ),
], )


Slider = html.Div([daq.Slider(
    id="slider",
    min=2018,
    max=2050,
    step=1,
    value=2018,
    marks={'2018': '2018',
           '2034': '2034',
           '2050': '2050'},
    size=450,
    handleLabel={"showCurrentValue": True, "label": "VALUE"
                 },
    included=False,
    ),
    ], style={
        # 'padding-top': 20,
        # 'padding-bottom': 20,
        # "width": '100vw',
        # "border": {"width":"10", "color":"black"},
        "height": "3vh",
        # "background-color": "yellow",
    })

radios_inputPie = html.Div([
    dbc.Label("Pie Graph",
              # align="center",
              ),
    dbc.RadioItems(
        id="radios_inputPie",
        options=[
            {"label": "Installed capacity", "value": "Installed capacity"},
            {"label": "Energy produced", "value": "Energy produced"},
        ],
        value="Installed capacity",
        # inline=True,
    )
])

####################################################################################
####################################################################################

from plotly.validators.scatter.marker import SymbolValidator


raw_symbols = SymbolValidator().values
namestems = []
for i in range(0,len(raw_symbols),2):
    name = raw_symbols[i+1]
    namestems.append(name.replace("-open", "").replace("-dot", ""))

namestems=set(namestems)
options=[{"label": i, "value": i} for i in namestems],





DropdownMarker = html.Div([
    dcc.Dropdown(
        id='DropdownM',
        options=options[0],
        value='circle',
        multi=False,
    ),
], )

slidertest = html.Div([daq.Slider(
    id="slidertest",
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



Graph=html.Div([
            dcc.Graph(
                figure=dict(
                    data=[],
                    layout=layout,
                    ),
                id='Graph',
            ),
            ])





####################################################################################
####################################################################################





FormInput = dbc.FormGroup([
        dbc.Label("Installed capacity amd Energy produced or both"),
        dbc.Checklist(
            options=[
                {"label": "Installed capacity", "value": "Installed capacity"},
                {"label": "Energy produced", "value": "Energy produced"},
            ],
            value=["Installed capacity"],
            id="switches-input",
            switch=True,
        ),
        dbc.Label('Scenarios'),
        dbc.Checklist(
            id="scenarios",
            options=[
                {"label": "IPP 2019", "value": 'IRP2019'},
                {"label": "CSIR 2019", "value": 'CSIR_LC'},
                {"label": "IPP 2019 2", "value": 'IRP2019_2'},
                {"label": "CSIR 2019 2", "value": 'CSIR_LC_2'},
            ],
            value=['IRP2019'],
            labelCheckedStyle={"color": "red"},
            inline=True,

        ),
    ])

DropdownButton = html.Div([
                        dbc.Button(
                                html.Div([html.A(
                                        children='Download',
                                        id='download-link',
                                        download="IRP2019.xlsx",
                                        target="_blank",
                                        style={"text": "none"},
                                    )]),
                                id='downloadButton',
                                color="primary",
                                className="mr-1",
                                href='',
                                size="lg",
                            )
                        ])

DL_card = html.Div([
    dbc.Card(
        dbc.CardBody(
            [
                html.H5("Download options", className="card-title"),
                html.P("How to Download  pick. "),
                html.P(children="Push Download Button",
                       style={'padding-bottom': 10,}),
                FormInput,
                DropdownButton,
            ]
        ),
        color="dark",
        inverse=True
        # style={"width": "18rem"},
        )
    ])

# collapse = html.Div([
#         dbc.Button(
#             "Open collapse",
#             id="collapse-button",
#             className="mb-3",
#             color="success",
#         ),
#         dbc.Collapse(
#             card,
#             id="collapse",
#         ),
#     ])

####################################################################################


Powerlayout = {
    "grid": {"rows": 1, "columns": 2},
    "title": "",
    "width": 1300,
    "xaxis": {
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
        "type": "linear",
        "ticks": "",
        # "domain": [0.55, 0.95],
        "mirror": False,
        "showgrid": True,
        "showline": False,
        "zeroline": False,
        "range": [0, 19e4],
        # "gridcolor": "rgb(255, 255, 255)",
        # "linecolor": "rgb(34,34,34)",
        "linewidth": 1,
        "title": "Installed capacity [MW]",
        "autorange": False,
    },
    "height": 600,
    "legend": {
        # "x": 1.019163763066202,
        # "y": 0.5147321428571429,
        # "xref": "paper",
        # "yref": "paper",
        # "bgcolor": "rgba(255, 255, 255, 0.5)",
        "traceorder": "normal"
    },
    # "margin": {"l": 100},
    "xaxis2": {
        "type": "linear",
        "ticks": "",
        "title": "Years",
        "anchor": "y2",
        "domain": {"column": 0},
        "mirror": False,
        "showgrid": True,
        "showline": True,
        "zeroline": False,
        "autorange": True,
        # "gridcolor": "rgb(255, 255, 255)",
        # "linecolor": "rgb(34,34,34)",
        "linewidth": 2,
    },
    "yaxis2": {
        "type": "linear",
        "ticks": "",
        "anchor": "x2",
        "domain": {"column": 1},
        "mirror": False,
        "showgrid": True,
        "showline": False,
        "zeroline": False,
        "range": [0, 4.5e5],
        # "gridcolor": "rgb(255, 255, 255)",
        # "linecolor": "rgb(34,34,34)",
        "linewidth": 1,
        "autorange": False,
        "title": "Energy produced [GWh]",
    },

    "barmode": "stack",
    "autosize": False,
    "showlegend": True,
}



IRP2019_Divlayout=Powerlayout.copy()
IRP2019_Divlayout['title'] ='IRP 2019'

CSIR_LC_Divlayout=Powerlayout.copy()
CSIR_LC_Divlayout['title']='CSIR_LC_Div'

IRP2019_2_Divlayout=Powerlayout.copy()
IRP2019_2_Divlayout['title']='IRP2019_2_Div'

CSIR_LC_2_Divlayout=Powerlayout.copy()
CSIR_LC_2_Divlayout['title']='CSIR_LC_2_Div'


l = {}

for case in scenariosDict:
    print(case)

    DF_E = scenariosDict[case]["Installed capacity"]
    DF_P = scenariosDict[case]["Energy produced"]

    traces = []

    for i, power in enumerate(powerlist):
        # print(i)
        traces.append(
            dict(
                type='scatter',
                x=np.array(DF_P['Year']),
                y=np.array(DF_P[power]),
                name=power,
                legendgroup=power,
                marker=dict(color=colours[i]),
                stackgroup='one',
                line={'width': 0.75
                      },
                fillcolor=colours[i],
            )
        )

        traces.append(
            dict(
                type='scatter',
                x=np.array(DF_E['Year']),
                y=np.array(DF_E[power]),
                name=power,
                legendgroup=power,
                xaxis='x2',
                yaxis='y2',
                showlegend=False,
                marker=dict(color=colours[i]),
                stackgroup='Two',
                line={'width': 0.75
                      },
                fillcolor=colours[i],
            ))

    l[case] = {"data": traces}




PowerGraphs = html.Div([
        dcc.Graph(id="PowerGraphs", figure=dict(data=[], layout=Powerlayout))
        ], style={
            # 'padding-top': 20,
            'padding-bottom': 20,
            # "width": '100%',
            "height": '100',

        },)

IRP2019_Div=html.Div([
            dcc.Graph(
                figure=dict(
                    data=l['IRP2019']['data'],
                    layout=IRP2019_Divlayout,
                    ),
                # id='IRP2019_Div',
            ),
            ],
            id='IRP2019_Div',
            hidden=True,)


CSIR_LC_Div=html.Div([
            dcc.Graph(
                figure=dict(
                    data=l['CSIR_LC']['data'],
                    layout=CSIR_LC_Divlayout,
                    ),
                # id='IRP2019',
            ), ],
            id='CSIR_LC_Div',
            hidden=True,)

IRP2019_2_Div=html.Div([
            dcc.Graph(
                figure=dict(
                    data=l['IRP2019_2']['data'],
                    layout=IRP2019_2_Divlayout,
                    ),
                # id='IRP2019'
                ), ],
            id='IRP2019_2_Div',
            hidden=True)

CSIR_LC_2_Div=html.Div([
            dcc.Graph(
                figure=dict(
                    data=l['CSIR_LC_2']['data'],
                    layout=CSIR_LC_2_Divlayout,
                    ),
                # id='IRP2019'
                ), ],
            id='CSIR_LC_2_Div',
            hidden=True)



####################################################################################

Powerlayout_oneyear = {
    "grid": {"rows": 1, "columns": 2},
    "title": "",
    # "width": 1300,
    "xaxis": {
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
        # "tick0" : 2018,
        "dtick": 1,

    },
    "yaxis": {
        "type": "linear",
        "ticks": "",
        # "domain": [0.55, 0.95],
        "mirror": False,
        "showgrid": True,
        "showline": False,
        "zeroline": False,
        "range": [0, 19e4],
        # "gridcolor": "rgb(255, 255, 255)",
        # "linecolor": "rgb(34,34,34)",
        "linewidth": 1,
        "title": "Installed capacity [MW]",
        "autorange": False,
    },
    "height": 500,
    "legend": {
        # "x": 1.019163763066202,
        # "y": 0.5147321428571429,
        # "xref": "paper",
        # "yref": "paper",
        # "bgcolor": "rgba(255, 255, 255, 0.5)",
        "traceorder": "normal"
    },
    # "margin": {"l": 100},
    "xaxis2": {
        "type": "linear",
        "ticks": "",
        "title": "Years",
        "anchor": "y2",
        "domain": {"column": 0},
        "mirror": False,
        "showgrid": True,
        "showline": True,
        "zeroline": False,
        "autorange": True,
        # "gridcolor": "rgb(255, 255, 255)",
        # "linecolor": "rgb(34,34,34)",
        "linewidth": 2,
        "dtick": 1,
    },
    "yaxis2": {
        "type": "linear",
        "ticks": "",
        "anchor": "x2",
        "domain": {"column": 1},
        "mirror": False,
        "showgrid": True,
        "showline": False,
        "zeroline": False,
        "range": [0, 4.5e5],
        # "gridcolor": "rgb(255, 255, 255)",
        # "linecolor": "rgb(34,34,34)",
        "linewidth": 1,
        "autorange": False,
        "title": "Energy produced [GWh]",
    },

    "barmode": "stack",
    "autosize": True,
    "showlegend": True,
}

PowerGraphs_oneyear = html.Div([
        dcc.Graph(id="PowerGraphs_oneyear", figure=dict(data=[], layout=Powerlayout))
        ], style={
            # 'padding-top': 20,
            'padding-bottom': 20,
            # "width": '100%',
            # "height": '100',

        },)


####################################################################################


Costlayout = {
    "title": "Cost",
    # "width": 1300,
    "height": 600,
    "legend": {
        "traceorder": "normal"
    },
    "xaxis": {
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
        "type": "linear",
        "ticks": "",
        # "domain": [0.55, 0.95],
        "mirror": False,
        "showgrid": True,
        "showline": False,
        "zeroline": True,
        # "range": [0, 16e4],
        # "gridcolor": "rgb(255, 255, 255)",
        # "linecolor": "rgb(34,34,34)",
        "linewidth": 2,
        "title": "Cost in Rands",
        "autorange": True,
    },
    # "autosize": True,
    "showlegend": True,
    # "width": '1500',
}


# t=[go.Scatter(
#         x=years,
#         y=DF_E["COA"],
#         name='COA price',
#         fill='tozeroy',
#         # fillcolor=str(colours[1]),
#         line=dict(
#                     # color='firebrick',
#                     width=4,
#                     dash='dash'
#                     )
#         )]


costGraph=html.Div([
            dcc.Graph(
                figure=dict(
                    data=[],
                    layout=Costlayout,
                    ),
                id="costGraph"
                ),
            ],)



######################### Text GenWind

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



# fill in layout

PieLayout = {  # "grid": {"rows": 1, "columns": 2},
    "height": 830,
    "legend": {
        "x": .95,
        "y": 0.55,
        # "xref": "paper",
        # "yref": "paper",
        # "bgcolor": "rgba(255, 255, 255, 0.5)",
        "traceorder": "normal",
        "legend_orientation": "h",
    },
}
PieLayout["sliders"] = {
    "args": [
        "transition", {
            "duration": 400,
            "easing": "cubic-in-out"
        }
    ],
    "initialValue": "2018",
    "plotlycommand": "animate",
    "values": CSIR_LC_2019_E['Year'],
    "visible": True
}
PieLayout["updatemenus"] = [
    {
        "buttons": [
            {
                "args": [None, {"frame": {"duration": 500, "redraw": True},
                                "fromcurrent": True, "transition": {"duration": 300,
                                                                    "easing": "quadratic-in-out"}}],
                "label": "Play",
                "method": "animate"
            },
            {
                "args": [[None], {"frame": {"duration": 0, "redraw": True},
                                  "mode": "immediate",
                                  "transition": {"duration": 0}}],
                "label": "Pause",
                "method": "animate"
            }
        ],
        "direction": "left",
        # "pad": {"r": 10, "t": 87},
        "showactive": False,
        "type": "buttons",
        "x": 0.1,
        "xanchor": "right",
        "y": 0.0,
        "yanchor": "top"
    }
]
sliders_dict = {
    "active": 0,
    "yanchor": "top",
    "xanchor": "left",
    "currentvalue": {
        "font": {"size": 20},
        "prefix": "Year:",
        "visible": True,
        "xanchor": "right"
    },
    "transition": {"duration": 300, "easing": "cubic-in-out"},
    # "pad": {"b": 10, "t": 50},
    "len": 0.95,
    "x": 0.0,
    "y": 0.0,
    "steps": []
}
PieData = [
    {
        "labels": powerlist,
        "values": np.array(CSIR_LC_2019_E[CSIR_LC_2019_E['Year'] == 2018][powerlist])[0],
        # "domain": {"column": 0},
        'domain': {'x': [.01, .30],
                   'y': [0, 1]},
        "title": f"2018 <br> {int(sum(np.array(CSIR_LC_2019_E[CSIR_LC_2019_E['Year'] == 2018][powerlist])[0]) / 1000)} [unit]",
        "hole": .4,
        "type": "pie",
        "textposition": "inside",
        # "scalegroup":'one',
        "marker": {"colors": colours},  # all of then ( they are linked )
        # "width": 1000,

    },
    {
        "labels": powerlist,
        "values": np.array(CSIR_LC_2019_E[CSIR_LC_2019_E['Year'] == 2050][powerlist])[0],
        "title": f"2050 <br> {int(sum(np.array(CSIR_LC_2019_E[CSIR_LC_2019_E['Year'] == 2050][powerlist])[0]) / 1000)} [unit]",
        # "domain": {"column": 1},
        'domain': {'x': [.35,
                         0.35 + 0.38 * (1 + (sum(np.array(IRP2019_E[IRP2019_E['Year'] == 2018][powerlist])[0]) /
                                             sum(np.array(IRP2019_E[IRP2019_E['Year'] == 2050][powerlist])[0])))],
                   'y': [0, 1]},
        "name": "Change",
        "hole": .4,
        "type": "pie",
        "textposition": "inside",
        # "scalegroup":'one',
    }]

# make frames

PieFrames = []
for year in years:
    frame = {"data": [], "layout": [], "name": str(year)}
    # frame["data"].append(go.Pie(labels=powerlist,
    #                             values=np.array(CSIR_LC_2019_E[CSIR_LC_2019_E['Year'] == year][powerlist])[0],
    #                             textinfo='label+percent',
    #                             textposition='inside',
    #                             scalegroup='one',
    #                             hole=.3,
    #                             domain= {"column": 1},
    #                             ))

    frame["data"] = [
        {
            "labels": powerlist,
            "values": np.array(CSIR_LC_2019_E[CSIR_LC_2019_E['Year'] == 2018][powerlist])[0],
            # "domain": {"column": 0},
            'domain': {'x': [.01, .36],
                       'y': [0, 1]},
            "hole": .4,
            "type": "pie",
            "textposition": "inside",
            "scalegroup": 'one',
            "title": f"2018 <br> {round(int(sum(np.array(CSIR_LC_2019_E[CSIR_LC_2019_E['Year'] == 2018][powerlist])[0]) / 1000))} [unit]",
            "coloraxis": colours,
        },
        {
            "labels": powerlist,
            "values": np.array(CSIR_LC_2019_E[CSIR_LC_2019_E['Year'] == year][powerlist])[0],
            # "domain": {"column": 1},
            'domain': {'x': [.37,
                             0.37 + 0.35 * (1 + (sum(np.array(IRP2019_E[IRP2019_E['Year'] == 2018][powerlist])[0]) /
                                                 sum(np.array(IRP2019_E[IRP2019_E['Year'] == year][powerlist])[0])))],
                       'y': [0, 1]},
            "hole": .4,
            "type": "pie",
            "textposition": "inside",
            "scalegroup": 'one',
            "title": f"{year} <br> {round(int(sum(np.array(CSIR_LC_2019_E[CSIR_LC_2019_E['Year'] == year][powerlist])[0]) / 1000))} [unit]",
            "coloraxis": colours,
        }, ]

    PieFrames.append(frame)
    slider_step = {"args": [
        [year],
        {"frame": {"duration": 300, "redraw": True},
         "mode": "immediate",
         "transition": {"duration": 300}}
    ],
        "label": year,
        "method": "animate"}
    sliders_dict["steps"].append(slider_step)

PieLayout["sliders"] = [sliders_dict]

PieGraphs = html.Div([
    dcc.Graph(id="Pie", figure=dict(data=PieData,
                                     layout=PieLayout,
                                     frames=PieFrames))
     ], style={
        # 'padding-top': 20,
        'padding-bottom': 20,
        # "height": 1500,
    })

######################################


table_header_style = {
    "backgroundColor": "rgb(2,21,70)",
    "color": "white",
    "textAlign": "center",
}

columns=[{'name': 'Energy Type', 'id': 'power'},
         {'name': 'Installed capacity [unit]', 'id': 'Installed capacity', 'type': 'numeric'},
         {'name': 'Energy produced [unit]', 'id': 'Energy produced', 'type': 'numeric'},
         ]

table=html.Div([html.H3(children="Table",
                        id="Table_Head"),
                dash_table.DataTable(
                        id="table",
                        style_header=table_header_style,
                        style_data_conditional=[
                            {
                                "if": {"column_id": "param"},
                                "textAlign": "right",
                                "paddingRight": 10,
                            },
                            {
                                "if": {"row_index": "odd"},
                                "backgroundColor": "white",
                            },
                        ],
                        columns=columns,
                    )
                ])


tab1_content =html.Div([
                    dbc.Card(
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col(DropdownCase_Allyear,
                                        sm=3,
                                        width={"offset": 1}
                                        ),
                            ]),
                            dbc.Row([
                                dbc.Col(PowerGraphs,
                                        sm=10,
                                        width={"offset": 1}
                                        ),
                            ]),
                            ]
                        ),
                        className="mt-3",
                        )
                    ])

tab2_content = html.Div([
                    dbc.Card(
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col(DropdownCase_Oneyear,
                                        sm=3,
                                        width={"offset": 1}
                                        ),
                                dbc.Col(Slider,
                                        sm=5),

                            ]),
                            dbc.Row([
                                dbc.Col(
                                    html.Div(
                                        [
                                            PowerGraphs_oneyear,
                                        ]),
                                    sm=8,
                                ),
                                dbc.Col(
                                    table,
                                    sm=3,
                                ),
                            ])
                        ]),
                    className="mt-3",
                    )])

tab3_content = html.Div([
                    dbc.Card(
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col(DropdownCase_Pie,
                                        sm=3,
                                        width={"offset": 1}
                                        ),
                                dbc.Col(radios_inputPie,
                                        sm=3,
                                        width={"offset": 0}
                                        ),
                            ]),
                            dbc.Row([
                                dbc.Col(PieGraphs,
                                        sm=10,
                                        width={"offset": 1}
                                        ),
                            ]),

                        ]),
                    className="mt-3",
                    )])

tab4_content = html.Div([
                    dbc.Card(
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col(DropdownCase_Cost,
                                        sm=4,
                                        width={"offset": 1}
                                        ),
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    costGraph,
                                    IRP2019_Div,
                                    CSIR_LC_Div,
                                    IRP2019_2_Div,
                                    CSIR_LC_2_Div,
                                ],
                                    sm=10,
                                    width={"offset": 1}
                                    ),
                            ]),

                        ]),
                    className="mt-3",
                    )])

tabs = dbc.Tabs([
        dbc.Tab(tab1_content, label="All the years"),
        dbc.Tab(tab2_content, label="One Year at a time "),
        dbc.Tab(tab3_content, label="Pie "),
        dbc.Tab(tab4_content, label="Cost "),
    ])





###############################################################################################################################################




app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, 'https://codepen.io/chriddyp/pen/bWLwgP.css',
                                                dbc.themes.GRID])

server = app.server

app.layout = html.Div(children=[
    html.Div([navbar]),
    html.Div([html.H1('DPV ask about')]),
    html.Div([
        dbc.Row([
            dbc.Col(Text_GenWind,
                    sm=6),
            dbc.Col(DL_card,
                    sm=6),
             ]),

        dbc.Row([
            # dbc.Col(Dropdown,
            #         sm=3,
            #         width={"offset": 1}),
            # dbc.Col(Slider,
            #         sm=3),
            # dbc.Col(radios_inputPie,
            #         width={"offset": 1},
            #         sm=2),
        ]),
        dbc.Row([
            dbc.Col(tabs,
                    sm=12,
                    align="center",
                    width={"offset": 0}
                    ),
        ]),
        dbc.Row([
            dbc.Col(html.Div(
                [dbc.Jumbotron(
                    html.P("tester")
                )]
            ),
                sm=8,
                align="center",
                width={"offset": 2})
        ]),
        # dbc.Row([
        #     dbc.Col(PieGraphs,
        #             sm=8,
        #             align="center",
        #             width={"offset": 2})
        # ]),
        dbc.Row([
            dbc.Col([
                dbc.Row([
                    dbc.Col(Fillswitches, align="end", width={"offset": 1}),
                    dbc.Col([radios_dash], align="end", width={"offset": 1}),
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
                DropdownMarker, ],
                sm=2,
                width={"offset": 0}),
            dbc.Col(slidertest,
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
    ])])


###############################################################################################################################################
###############################################################################################################################################
###############################################################################################################################################

@app.callback(Output("Graph", "figure"),
              [Input('DropdownM', 'value'),
               Input('Fillswitches', 'value'),
               Input('lineW', 'value'),
               Input('MarkerW', 'value'),
               Input('slidertest', 'value'),
               Input('radios_dash', 'value'),],)
def updatePowerGraph(DropdownM,Fillswitches,lineW,MarkerW,slider,radios_dash):
    print("hey")
    print(f'DropdownValue is {DropdownM}')
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
    DF_E = IRP2019_P
    DF_P = IRP2019_E

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
                marker_symbol=DropdownM,
                )
        )


    # layout["title"] = DropdownValue

    figure = dict(data=traces, layout=layout)
    return figure

###############################################################################################################################################
###############################################################################################################################################
###############################################################################################################################################

@app.callback(Output("PowerGraphs", "figure"),
              [Input('DropdownCase_Allyear', 'value'),],)
def updatePowerGraph(DropdownValue):
    # print("hey")
    # print(f'DropdownValue is {DropdownValue}')
    # print("hey 2")
    # print(f'DropdownValue is {sliderValue}')
    # print(f'DropdownValue is {type(sliderValue)}')
    # print(f'SwitchesValue is {switchesValue}')

    #######################################

    Powerlayout['title'] =DropdownValue


    figure = dict(data=l[DropdownValue]['data'], layout=Powerlayout)
    return figure



###############################################################################################################################################

@app.callback(Output("PowerGraphs_oneyear", "figure"),
              [Input('DropdownCase_Oneyear', 'value'),
               Input('slider', 'value'), ],
              [
                  # State("RadioPower", "value"),
              ], )
def updatePowerGraph_oneYear(DropdownValue, sliderValue):
    print("hey DropdownCase_Allyear")
    print(f'DropdownValue is {DropdownValue}')
    # print("hey 5")

    #######################################

    scenariosDict[DropdownValue]
    DF_E = scenariosDict[DropdownValue]["Installed capacity"]
    DF_P = scenariosDict[DropdownValue]["Energy produced"]


    traces = []



    for i, power in enumerate(powerlist):
        traces.append(
            go.Bar(x=[str(sliderValue)],
                   y=DF_E[DF_E['Year'] == sliderValue][power],
                   name=power,
                   legendgroup=power,
                   # fillcolor=colours[i],
                   marker=dict(color=colours[i]),
                   xaxis='x2',  #
                   yaxis='y2',  #
                   )
        )

        traces.append(
            go.Bar(x=[sliderValue],
                   y=DF_P[DF_P['Year'] == sliderValue][power],
                   name=power,
                   legendgroup=power,
                   showlegend=False,
                   marker=dict(color=colours[i]),
                   ))

    Powerlayout_oneyear["title"] = DropdownValue

    figure = dict(data=traces, layout=Powerlayout_oneyear)
    return figure




############################################################################################################################################### PIE


@app.callback(Output("Pie", "figure"),
              [Input('DropdownCase_pie', 'value'),
               Input('radios_inputPie', 'value'), ],
              [
                  # State("RadioPower", "value"),
              ], )
def updateMapRSA(DropdownValue, radios_inputPie):
    #######################################
    # print(f' the pie {DropdownValue} and {radios_inputPie}')
    scenariosDict[DropdownValue]
    DF_Pie = scenariosDict[DropdownValue][radios_inputPie]

    # print(DF_Pie)

    PieData = [
        {
            "labels": powerlist,
            "values": np.array(DF_Pie[DF_Pie['Year'] == 2018][powerlist])[0],
            # "domain": {"column": 0},
            'domain': {'x': [.01, .36],
                       'y': [0, 1]},
            "title": f"2018 <br> {int(sum(np.array(DF_Pie[DF_Pie['Year'] == 2018][powerlist])[0]) / 1000)} [unit]",
            "hole": .4,
            "type": "pie",
            "textposition": "inside",
            # "scalegroup":'one',
            "marker": {"colors": colours},  # all of then ( they are linked )
            # "width": 1000,

        },
        {
            "labels": powerlist,
            "values": np.array(DF_Pie[DF_Pie['Year'] == 2050][powerlist])[0],
            "title": f"2050 <br> {int(sum(np.array(DF_Pie[DF_Pie['Year'] == 2050][powerlist])[0]) / 1000)} [unit]",
            # "domain": {"column": 1},
            'domain': {'x': [.37,
                             0.37 + 0.35 * (1 + (sum(np.array(DF_Pie[DF_Pie['Year'] == 2018][powerlist])[0]) /
                                                 sum(np.array(DF_Pie[DF_Pie['Year'] == 2050][powerlist])[0])))],
                       'y': [0, 1]},
            "name": "Change",
            "hole": .4,
            "type": "pie",
            "textposition": "inside",
            # "scalegroup":'one',
        }]

    PieFrames = []
    for year in years:
        frame = {"data": [], "layout": [], "name": str(year)}
        # frame["data"].append(go.Pie(labels=powerlist,
        #                             values=np.array(CSIR_LC_2019_E[CSIR_LC_2019_E['Year'] == year][powerlist])[0],
        #                             textinfo='label+percent',
        #                             textposition='inside',
        #                             scalegroup='one',
        #                             hole=.3,
        #                             domain= {"column": 1},
        #                             ))

        frame["data"] = [
            {
                "labels": powerlist,
                "values": np.array(DF_Pie[DF_Pie['Year'] == 2018][powerlist])[0],
                # "domain": {"column": 0},
                'domain': {'x': [.01, .36],
                           'y': [0, 1]},
                "hole": .4,
                "type": "pie",
                "textposition": "inside",
                "scalegroup": 'one',
                "title": f"2018 <br> {round(int(sum(np.array(DF_Pie[DF_Pie['Year'] == 2018][powerlist])[0]) / 1000))} [unit]",
                "coloraxis": colours,
            },
            {
                "labels": powerlist,
                "values": np.array(DF_Pie[DF_Pie['Year'] == year][powerlist])[0],
                # "domain": {"column": 1},
                'domain': {'x': [.37,
                                 0.37 + 0.35 * (1 + (sum(np.array(DF_Pie[DF_Pie['Year'] == 2018][powerlist])[0]) /
                                                     sum(np.array(DF_Pie[DF_Pie['Year'] == year][powerlist])[
                                                             0])))],
                           'y': [0, 1]},
                "hole": .4,
                "type": "pie",
                "textposition": "inside",
                "scalegroup": 'one',
                "title": f"{year} <br> {round(int(sum(np.array(DF_Pie[DF_Pie['Year'] == year][powerlist])[0]) / 1000))} [unit]",
                "coloraxis": colours,
            }, ]

        PieFrames.append(frame)
        slider_step = {"args": [
            [year],
            {"frame": {"duration": 300, "redraw": True},
             "mode": "immediate",
             "transition": {"duration": 300}}
        ],
            "label": year,
            "method": "animate"}
        sliders_dict["steps"].append(slider_step)

    PieLayout["title"] = DropdownValue + " " +radios_inputPie
    figure = dict(data=PieData, layout=PieLayout, frames=PieFrames)
    return figure


# @app.callback(
#     Output("collapse", "is_open"),
#     [Input("collapse-button", "n_clicks")],
#     [State("collapse", "is_open")],
# )
# def toggle_collapse(n, is_open):
#     if n:
#         return not is_open
#     return is_open


#####################################################################


@app.callback([
    Output("table", "data"),
    Output("Table_Head", "children"),],

    [Input('DropdownCase_Oneyear', 'value'),
     Input('slider', 'value')],
)
def update_output(DropdownValue,slider):
    DF_E = scenariosDict[DropdownValue]["Installed capacity"]
    DF_P = scenariosDict[DropdownValue]["Energy produced"]

    dataupdate = []
    # dictionary={}
    cont = 0
    SUM_DF_P = DF_P[DF_P['Year'] == slider][powerlist].values[0].sum()
    SUM_DF_E = DF_E[DF_E['Year'] == slider][powerlist].values[0].sum()
    for power in powerlist:
        # x= DF_P[DF_P['Year']==slider][power].values[0]
        E = f"{DF_E[DF_E['Year'] == slider][power].values[0]}     " \
            f"[{round((DF_E[DF_E['Year'] == slider][power].values[0] / SUM_DF_E) * 100)} %]"

        P = f"{DF_P[DF_P['Year'] == slider][power].values[0]}     " \
            f"[{round((DF_P[DF_P['Year'] == slider][power].values[0] / SUM_DF_P) * 100)} %]"

        dataDict = {'power': power,
                    "Installed capacity": E,
                    "Energy produced": P,
                    }
        dataupdate.append(dataDict)
        cont += 1
    #     print(p)
    dataupdate.append({
        'power': "Total",
        "Installed capacity": round(SUM_DF_E),
        "Energy produced": round(SUM_DF_P), })

    print("two")
    print(dataupdate)
    Table_Head = f"{DropdownValue} {slider} Year"
    # print(dataupdate)
    return dataupdate,Table_Head


#####################################################################


@app.callback([
                Output("costGraph", "figure"),
                Output("IRP2019_Div", "hidden"),
                Output("CSIR_LC_Div", "hidden"),
                Output("IRP2019_2_Div", "hidden"),
                Output("CSIR_LC_2_Div", "hidden"),
               ],
              [Input('DropdownCase_Cost', 'value'),],)
def updatePowerGraph(DropdownValue):
    print("hey")
    print(f'DropdownValue is {DropdownValue}')
    print("hey 2")
    # print(f'DropdownValue is {sliderValue}')
    # print(f'DropdownValue is {type(sliderValue)}')
    # print(f'SwitchesValue is {switchesValue}')

    #######################################

    # scenariosDict[DropdownValue]
    IRP2019 = True
    CSIR_LC = True
    IRP2019_2 = True
    CSIR_LC_2 = True

    if "IRP2019" in DropdownValue:
        IRP2019=False


    if "CSIR_LC" in DropdownValue:
        CSIR_LC=False


    if "IRP2019_2" in DropdownValue:
        IRP2019_2=False


    if "CSIR_LC_2" in DropdownValue:
        CSIR_LC_2=False


    traces = []
    for j in DropdownValue:
        print(f"j is {j} ")
        DF_cost=scenariosDict[j]["Energy produced"]


        traces.append(
            go.Scatter(
                x=years,
                y=DF_cost['COA'],
                name="COA price "+j,
                # fill='tozeroy',
                line=dict(
                    # color='firebrick',
                    width=4,
                    dash='dash'),
               )
            )

    print(traces)
    figure = dict(data=traces, layout=Costlayout)

    return figure, IRP2019, CSIR_LC,IRP2019_2,CSIR_LC_2


#####################################################################

@app.callback(
    Output('download-link', 'href'),
    [Input('switches-input', 'value'),
     Input('scenarios', 'value')])
def update_download_button(switches, scenarios):
    print(switches)
    print(scenarios)
    xlsx_io = io.BytesIO()
    writer = pd.ExcelWriter(xlsx_io, engine='xlsxwriter')
    for scenario in scenarios:
        for i in switches:
            scenariosDict[scenario][i].to_excel(writer, sheet_name=scenario + " " + i)

    writer.save()
    xlsx_io.seek(0)
    #     https://en.wikipedia.org/wiki/Data_URI_scheme
    media_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    data = base64.b64encode(xlsx_io.read()).decode("utf-8")
    href_data_downloadable = f'data:{media_type};base64,{data}'
    return href_data_downloadable


if __name__ == '__main__':
    app.run_server(port=8848, debug=True)
