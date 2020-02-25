import dash
import dash_table
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output,State
import dash_html_components as html
import dash_core_components as dcc
import collections

IRP2019_P = pd.read_excel('2019-IRP.xlsx', sheet_name="IRP1_P").round(1)
IRP2019_E = pd.read_excel('2019-IRP.xlsx', sheet_name="IRP1_E").round(1)

CSIR_LC_2019_P = pd.read_excel('2019-CSIR_LC.xlsx', sheet_name="IRP1_P").round(1)
CSIR_LC_2019_E = pd.read_excel('2019-CSIR_LC.xlsx', sheet_name="IRP1_E").round(1)

IRP2019_P2 = (IRP2019_P * 0.8).round(1)
IRP2019_E2 = (IRP2019_E * 0.8).round(1)

CSIR_LC_2019_P2 = (CSIR_LC_2019_P * 0.8).round(1)
CSIR_LC_2019_E2 = (CSIR_LC_2019_E * 0.8).round(1)


powerlist =list(CSIR_LC_2019_E.columns)
print(powerlist)
removelist=[powerlist[0],powerlist[11],powerlist[13]]
removelist

for i in removelist:
    print(f'remove {i}')
    powerlist.remove(i)



scenariosDict = {
    'IRP2019': {"Energy produced": IRP2019_P, "Installed capacity": IRP2019_E, },
    'CSIR_LC': {"Energy produced": CSIR_LC_2019_P, "Installed capacity": CSIR_LC_2019_E, },
    'IRP2019_2': {"Energy produced": IRP2019_P2, "Installed capacity": IRP2019_E2, },
    'CSIR_LC_2': {"Energy produced": CSIR_LC_2019_P2, "Installed capacity": CSIR_LC_2019_E2, },
}

Dropdown = html.Div([
    dcc.Dropdown(
        id='DropdownCase',
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



g=(CSIR_LC_2019_E[CSIR_LC_2019_E['Year']==2018][powerlist])
h=(CSIR_LC_2019_P[CSIR_LC_2019_P['Year']==2018][powerlist])

data = {'Power' : powerlist, 'IPP':np.array(g)[0], 'Color' : np.array(h)[0]}
df = pd.DataFrame(data)


table1=dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in df.columns],
    data=df.to_dict('records'),
        )


import plotly.graph_objects as go
from plotly.colors import n_colors
colors = n_colors('rgb(255, 200, 200)', 'rgb(200, 0, 0)', 9, colortype='rgb')
a = np.random.randint(low=0, high=9, size=10)
b = np.random.randint(low=0, high=9, size=10)
c = np.random.randint(low=0, high=9, size=10)


colours = ['#8c664a', '#ff270f', '#969696', '#e8d2ca', '#2760a6', '#9db1cf', '#eea632', '#ffed11', '#d7c700', '#007770'
                    , '#0a346f', ]
e =[go.Table(
    header=dict(
        values=["<b>Power</b>", "<b>E<b>", "<b>P<b>"],
        line_color="black", fill_color='darkslategray',
        align='center', font=dict(color='black', size=20)
    ),
    cells=dict(
        values=[powerlist, np.array(g)[0], np.array(h)[0]],
        line_color=['black'],  # fill_color=['#ff270f',np.array(colors)[b], np.array(colors)[c]],
        fill_color=[colours, 'grey', 'grey'],
        align='center', font=dict(color='black', size=11)
    ))]

w={"height": 1000,}


table2=dcc.Graph(id="table2",
                 figure=dict(data=e, layout=w))

import dash_daq as daq
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




table_header_style = {
    "backgroundColor": "rgb(2,21,70)",
    "color": "white",
    "textAlign": "center",
}

columns=[{'name': 'Energy Type', 'id': 'power'},
         {'name': 'Installed capacity', 'id': 'Installed capacity', 'type': 'numeric'},
         {'name': 'Energy produced', 'id': 'Energy produced', 'type': 'numeric'},
         ]

data = []
cont = 0
# dictionary={}
for p in powerlist:
    dataDict = {'power': p, "Energy produced": 12 + cont, "Installed capacity": 13 + cont * 2}
    cont += 1
    data.append(dataDict)
#     print(p)


table3= dash_table.DataTable(
        id="results-table",
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
        data=data,
    )

app = dash.Dash(__name__)

app.layout = html.Div([
    table1,
    Slider,
    Dropdown,
    table3
])


#
# @app.callback(
#     Output("table2", "figure"),
#     [Input("slider", "value")],
# )
# def toggle_collapse(slider):
#     print("hey")
#     a = np.random.randint(low=0, high=9, size=11)
#     b = np.random.randint(low=0, high=9, size=11)
#
#     data = [go.Table(
#         header=dict(
#             values=["<b>Power</b>", "<b>E<b>", "<b>P<b>"],
#             line_color="black", fill_color='darkslategray',
#             align='center', font=dict(color='black', size=20)
#         ),
#         cells=dict(
#             values=[powerlist, a, b],
#             line_color=['black'],  # fill_color=['#ff270f',np.array(colors)[b], np.array(colors)[c]],
#             fill_color=[colours, 'grey', 'grey'],
#             align='center', font=dict(color='black', size=11)
#         ))]
#     figure = dict(data=data)
#     return figure



@app.callback(
    [
    Output("results-table", "data"),
    ],
    [Input('DropdownCase', 'value'),
     Input('slider', 'value')],
)
def update_output(DropdownValue,slider):
    print("one")

    DF_E = scenariosDict[DropdownValue]["Installed capacity"]
    DF_P = scenariosDict[DropdownValue]["Energy produced"]

    dataupdate = []
    # dictionary={}
    cont=0
    for power in powerlist:
        dataDict = {'power': power,
                    "Energy produced": DF_P[DF_P['Year']==slider][power],
                    "Installed capacity": DF_E[DF_E['Year']==slider][power]}
        dataupdate.append(dataDict)
        cont+=1
    #     print(p)
    print("two")
    print(dataupdate)
    return [dataupdate]



if __name__ == '__main__':
    app.run_server(debug=True)



