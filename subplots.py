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




# powerlist =list(CSIR_LC_2019_E.columns)
# print(powerlist)
# removelist=[powerlist[0],powerlist[11],powerlist[13]]
# removelist
#
# for i in removelist:
#     print(f'remove {i}')
#     powerlist.remove(i)




# SubplotGraphs = html.Div([
#         dcc.Graph(id="SubplotGraphs", figure=dict(data=[], layout=Subplotlayout))
#         ])
#
#



# table_header = [
#     html.Thead(html.Tr([html.Th("First Name"), html.Th("Last Name")]))
# ]
#
#
#
#
# x=html.Div([
#     html.P("hey")
# ])
#
# row1 = html.Tr([html.Td("Arthur"), html.Td("Dent")])
# row2 = html.Tr([html.Td("Ford"), html.Td("Prefect")])
# row3 = html.Tr([html.Td("Zaphod"), html.Td("Beeblebrox")])
# row4 = html.Tr([html.Td("Trillian"), html.Td(x)])
#
#
#
# table_body = [html.Tbody([row1, row2, row3, row4],
#                          id="body")]
#
#
#
#
# table = dbc.Table(table_header + table_body,
#                   bordered=True,
#                   hover=True,
#                   responsive=True,
#                   striped=True,
#                   id='table'
#                   )


Dropdown = html.Div([
    dcc.Dropdown(
        id='DropdownCase',
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
        "height": "3vh",
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


# subplot=dbc.Row([
#             dbc.Col(
#                 html.Div(
#                 [
#                     SubplotGraphs,
#                 ]),
#             sm = 10,
#             width={"offset": 1},
#             ),
#         ])





trace1 = go.Scatter(
    x=[0, 1, 2],
    y=[10, 11, 12]
)
trace2 = go.Scatter(
    x=[2, 3, 4],
    y=[100, 110, 120],
)
trace3 = go.Scatter(
    x=[3, 4, 5],
    y=[1000, 1100, 1200],
)
fig = make_subplots(rows=3,
                    cols=1,
                    specs=[[{}], [{}], [{}]],
                    shared_xaxes=True,
                    shared_yaxes=True,
                    vertical_spacing=0.1)


fig.append_trace(trace1, 3, 1)
fig.append_trace(trace2, 2, 1)
fig.append_trace(trace3, 1, 1)

testlayout=dict(height=600, width=600, title='Stacked Subplots with Shared X-Axes')


# app.layout = html.Div([
#     dcc.Graph(figure=fig, id='my-figure')
# ])


l = {}

for case in scenariosDict:
    print(case)

    DF_E = scenariosDict[case]["Installed capacity"]
    DF_P = scenariosDict[case]["Energy produced"]

    traces = []

    for i, power in enumerate(powerlist):
        print(i)
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


Powerlayout = {
    "title": "",
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
        'domain': [0.0, 0.45],

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
        "range": [0, 16e4],
        # "gridcolor": "rgb(255, 255, 255)",
        # "linecolor": "rgb(34,34,34)",
        "linewidth": 1,
        "title": "Installed capacity [MW]",
        "autorange": False,
    },
    "xaxis2": {
        'anchor': 'y2',
        'domain': [0.55, 1.0],

        "type": "linear",
        "ticks": "",
        "title": "Years",
        # "anchor": "y2",
        # "domain": {"column": 0},
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
        'anchor': 'x2',
        'domain': [0.0, 1.0],

        "type": "linear",
        "ticks": "",
        # "anchor": "x2",
        # "domain": {"column": 1},
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
    }




IRP2019_Divlayout=Powerlayout.copy()
IRP2019_Divlayout['title'] ='IRP 2019'

CSIR_LC_Divlayout=Powerlayout.copy()
CSIR_LC_Divlayout['title']='CSIR_LC_Div'

IRP2019_2_Divlayout=Powerlayout.copy()
IRP2019_2_Divlayout['title']='IRP2019_2_Div'

CSIR_LC_2_Divlayout=Powerlayout.copy()
CSIR_LC_2_Divlayout['title']='CSIR_LC_2_Div'


print(colours[0])


Costlayout = {
    "title": "Cost",
    # "width": 1300,
    # "height": 600,
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






t=[go.Scatter(
        x=years,
        y=DF_E["COA"],
        name='COA price',
        fill='tozeroy',
        # fillcolor=str(colours[1]),
        line=dict(
                    # color='firebrick',
                    width=4,
                    dash='dash'
                    )
        )]


costGraph=html.Div([
            dcc.Graph(
                figure=dict(
                    data=t,
                    layout=Costlayout,
                    ),
                id="costGraph"
                ),
            ],)

t2=[go.Scatter(
        x=years,
        y=DF_E["COA"],
        name=power,
        marker=dict(color=colours[1]),
        fill='tozeroy',
        fillcolor=colours[1].replace(")", ",0.1)").replace("rgb", "rgba"),
        )]


costGraph2=html.Div([
            dcc.Graph(
                figure=dict(
                    data=t2,
                    ),
                ),
            ],)




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








app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP,'https://codepen.io/chriddyp/pen/bWLwgP.css'])
app.layout = html.Div(children=[
    html.Div([
        Text_GenWind,
        # costGraph,
        # costGraph2,
        dbc.Row([
            dbc.Col(Dropdown,
                    sm=3,
                    width={"offset": 1}),
            dbc.Col(Slider,
                    sm=3),
            dbc.Col(radios_inputPie,
                    width={"offset": 1},
                    sm=2),
        ]),
        # subplot,
        html.Div([
                dbc.Row([
                    dbc.Col([
                        costGraph,
                        IRP2019_Div,
                        CSIR_LC_Div,
                        IRP2019_2_Div,
                        CSIR_LC_2_Div,
                        # Text_GenWind
                             ],
                        sm=10,
                        width={"offset": 1}
                    ),
                ]),
        ])
    ]

    )

])






@app.callback([
                Output("IRP2019_Div", "hidden"),
                Output("CSIR_LC_Div", "hidden"),
                Output("IRP2019_2_Div", "hidden"),
                Output("CSIR_LC_2_Div", "hidden"),
               ],
              [Input('DropdownCase', 'value'),],)
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

    Subplotlayout=Powerlayout
    # Subplotlayout["title"] = DropdownValue[0]

    # figure = dict(data=l[DropdownValue[0]]['data'], layout=Subplotlayout)

    return  IRP2019, CSIR_LC,IRP2019_2,CSIR_LC_2




#
#
@app.callback(Output("costGraph", "figure"),
              [Input('DropdownCase', 'value'),],)
def updatePowerGraph(DropdownValue):
    print("hey")
    print(f'DropdownValue is {DropdownValue}')
    print("hey 2")
    # print(f'DropdownValue is {sliderValue}')
    # print(f'DropdownValue is {type(sliderValue)}')
    # print(f'SwitchesValue is {switchesValue}')

    #######################################

    # scenariosDict[DropdownValue]
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
    return figure

if __name__ == '__main__':
    app.run_server(port=8842,debug=True)

