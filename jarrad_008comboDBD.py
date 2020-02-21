import os
from pathlib import Path
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

IRP2019_P = pd.read_excel('2019-IRP.xlsx',sheet_name="IRP1_P").round(1)
IRP2019_E = pd.read_excel('2019-IRP.xlsx',sheet_name="IRP1_E").round(1)
CSIR_LC_2019_P = pd.read_excel('2019-CSIR_LC.xlsx',sheet_name="IRP1_P").round(1)
CSIR_LC_2019_E = pd.read_excel('2019-CSIR_LC.xlsx',sheet_name="IRP1_E").round(1)


IRP2019_P2 = (IRP2019_E*0.8).round(1)
IRP2019_E2 = (IRP2019_P*0.8).round(1)
CSIR_LC_2019_P2 =(CSIR_LC_2019_P*0.8).round(1)
CSIR_LC_2019_E2 = (CSIR_LC_2019_E*0.8).round(1)


powerlist =list(CSIR_LC_2019_E.columns)
print(powerlist)
removelist=[powerlist[0],powerlist[11],powerlist[13]]
removelist

for i in removelist:
    print(f'remove {i}')
    powerlist.remove(i)


tracebar=[] #colorcop

colours=["rgb(128, 43, 0)",    # COA
         "rgb(0, 153, 0)",     # NUC
         "rgb(255, 255, 0)",   # GAS
         "rgb(255, 102, 0)",   # PEA
         "rgb(0, 102, 102)",   # HYD
         "rgb(0, 102, 255)",   # WIN
         "rgb(204, 0, 153)",   # CSP
         "rgb(204, 0, 0)",     # SPV
         "rgb(0, 102, 102)",   # DPV
         "rgb(51, 51, 51)",    # BIO
         "rgb(64, 255, 0)",    # PST
]





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
    brand="Wind Energy Calculator",
    brand_style={'font-size': 35},
    brand_href="#",
    color="primary",
    dark=True,)])





Dropdown= html.Div([
             dcc.Dropdown(
                    id='Dropdown',
                    options=[
                        {'label': 'Installed capacity [MW]', 'value': "P", },
                        {'label': 'Energy produced [GWh]', 'value': "E", },
 ],
                    value='P',

                    multi=False,
                    ),
            ],)


DownloadOptions = html.Div(
    [
        dbc.DropdownMenu(
            [
                dbc.DropdownMenuItem("A button", id="dropdown-button"),
                dbc.DropdownMenuItem(
                    "Internal link", href="/l/components/dropdown_menu"
                ),
                dbc.DropdownMenuItem(
                    "External Link", href="https://github.com"
                ),
                dbc.DropdownMenuItem(
                    "External relative",
                    href="/l/components/dropdown_menu",
                    external_link=True,
                ),
            ],
            label="Menu",
        ),
        html.P(id="item-clicks", className="mt-3"),
    ]
)


DropdownCase =html.Div([
             dcc.Dropdown(
                    id='DropdownCase',
                    options=[
                        {'label': 'Installed capacity [MW]', 'value': "P", },
                        {'label': 'Energy produced [GWh]', 'value': "E", },
 ],
                    value='P',

                    multi=False,
                    ),
            ],)

####################################################################################

downloadSwitches = dbc.FormGroup(
    [
        dbc.Label("Toggle a bunch"),
        dbc.Checklist(
            options=[
                {"label": "Option 1", "value": 1},
                {"label": "Option 2", "value": 2},
            ],
            value=[],
            id="switches-input",
            switch=True,
        ),
    ]
)



checklist = dbc.Checklist(
    id="checklist-selected-style",
    options=[
        {"label": "Option 1", "value": 1},
        {"label": "Option 2", "value": 2},
        {"label": "Option 3", "value": 3},
    ],
    labelCheckedStyle={"color": "red"},
)

# def donwloadIRP2019_P():
print('hey')
df = IRP2019_P
xlsx_io = io.BytesIO()
writer = pd.ExcelWriter(xlsx_io, engine='xlsxwriter')
IRP2019_P.to_excel(writer, index=False, sheet_name="IRP2019_P")
IRP2019_E.to_excel(writer, index=False, sheet_name="IRP2019_E")
writer.save()
xlsx_io.seek(0)
# https://en.wikipedia.org/wiki/Data_URI_scheme
media_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
data = base64.b64encode(xlsx_io.read()).decode("utf-8")
href_data_downloadable = f'data:{media_type};base64,{data}'


DropdownButton = dbc.Button(html.Div([html.A(
                                         children='IRP2019 download',
                                         id='download-link',
                                         download="IRP2019.xlsx",
                                         target="_blank",
                                         style={"text": "none"},
                                     )]),
                               id='downloadButton',
                               color="primary",
                               className="mr-1",
                               href=href_data_downloadable,
                               size="lg",

                               )


card = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Custom CSS", className="card-title"),
            html.P(
                "This card has inline styles applied controlling the width. "
                "You could also apply the same styles with a custom CSS class."
            ),
        downloadSwitches,
        DropdownButton,
        checklist,
        ]
    ),
    color="dark",
    inverse=True
    # style={"width": "18rem"},
)





collapse = html.Div(
    [
        dbc.Button(
            "Open collapse",
            id="collapse-button",
            className="mb-3",
            color="success",
        ),
        dbc.Collapse(
            card,
            id="collapse",
        ),
    ]
)


####################################################################################


Powerlayout={
  "grid": {"rows": 1, "columns": 2},
  "title": "Installed capacity [MW]",
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
  },
  "yaxis": {
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
  "height": 900,
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
  },

  "barmode": "stack",
  "autosize": False,
  "showlegend": True,
}



PowerGraphs= html.Div(
    [dcc.Graph(id="PowerGraphs",figure=dict(data=tracebar,layout=Powerlayout))],
    style={
        #'padding-top': 20,
        'padding-bottom': 20,
        "width": '100%',


    },
    )






######################### Text GenWind

Text_GenWind =  html.Div([
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
    ],)

years = CSIR_LC_2019_E['Year']


# fill in layout

PieLayout= {#"grid": {"rows": 1, "columns": 2},
            "height": 900,
            "legend": {
            "x": 1.1,
            "y": 0.55,
            # "xref": "paper",
            # "yref": "paper",
            # "bgcolor": "rgba(255, 255, 255, 0.5)",
            "traceorder": "normal",
            "legend_orientation":"h",
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
        "pad": {"r": 10, "t": 87},
        "showactive": False,
        "type": "buttons",
        "x": 0.1,
        "xanchor": "right",
        "y": 0,
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
    "pad": {"b": 10, "t": 50},
    "len": 0.9,
    "x": 0.1,
    "y": 0,
    "steps": []
}

PieData = [
    {
        "labels": powerlist,
        "values": np.array(CSIR_LC_2019_E[CSIR_LC_2019_E['Year'] == 2018][powerlist])[0],
        #"domain": {"column": 0},
        'domain': {'x': [.01, .36],
                   'y': [0, 1]},
        "title": f"2018 <br> {int(sum(np.array(CSIR_LC_2019_E[CSIR_LC_2019_E['Year'] == 2018][powerlist])[0])/1000)} [unit]",
        "hole": .4,
        "type": "pie",
        "textposition":"inside",
        # "scalegroup":'one',
        "marker": {"colors":colours},  # all of then ( they are linked )
        # "width": 1000,

    },
    {
        "labels": powerlist,
        "values": np.array(CSIR_LC_2019_E[CSIR_LC_2019_E['Year'] == 2050][powerlist])[0],
        "title": f"2050 <br> {int(sum(np.array(CSIR_LC_2019_E[CSIR_LC_2019_E['Year'] == 2050][powerlist])[0])/1000)} [unit]",
        #"domain": {"column": 1},
        'domain': {'x': [.37,
                         0.37 + 0.35 * (1 + (sum(np.array(IRP2019_E[IRP2019_E['Year'] == 2018][powerlist])[0]) /
                                             sum(np.array(IRP2019_E[IRP2019_E['Year'] == 2050][powerlist])[0])))],
                   'y': [0, 1]},
        "name": "Change",
        "hole": .4,
        "type": "pie",
        "textposition":"inside",
        # "scalegroup":'one',
    }]



# make frames

PieFrames= []
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

    frame["data"]=[
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
            "coloraxis":colours,
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
        },]


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


######################################







PieGraphs= html.Div(
    [dcc.Graph(id="Pie",figure=dict(data=PieData,
                                    layout=PieLayout,
                                    frames=PieFrames))
     ],
    style={
        # 'padding-top': 20,
        'padding-bottom': 20,
        # "height": 1500,
    }
)


html.A(
    'Download Data',
    id='download-link',
    download="table.xls",
    href="",
    target="_blank"
)










###############################################################################################################################################

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP,'https://codepen.io/chriddyp/pen/bWLwgP.css',dbc.themes.GRID])
app.layout = html.Div(children=[
    html.Div([navbar]),
    html.Div([

        dbc.Row([
            dbc.Col(Text_GenWind,
                    sm=6),
              dbc.Col(collapse,
                      sm=6),
              ]),
        dbc.Row([
            dbc.Col(Dropdown,
                    sm=5),
            dbc.Col(daq.Slider(id="slider",
                               min=2018,
                               max=2050,
                               step=1,
                               value=2018,
                               marks={'2018': '2018',
                                      '2034': '2034',
                                      '2050': '2050'},
                               handleLabel={"showCurrentValue": True,"label": "VALUE"},
                               included=False,

                               ),
                    sm=5),
            dbc.Col(dbc.Checklist(
                            id="switches",
                            options=[
                                    {"label": "Option 1", "value": True},
                                    ],
                            value=[],
                            switch=True,
            ),

                    sm=2),
            ]),
        dbc.Row(
            dbc.Col(PowerGraphs,
                    sm=8,
                    align="center",
                    width={"offset": 2})
        ),
        dbc.Row(
            dbc.Col(html.Div(
                [dbc.Jumbotron(
                    html.P("this is a Pie Chart")
                )]
            ),
                    sm=8,
                    align="center",
                    width={"offset": 2})
        ),
        dbc.Row(
            dbc.Col(PieGraphs,
                    sm=6,
                    align="center",
                    width={"offset": 2})
        ),
        # dbc.Row(
        #     dbc.Col([DropdownButton,
        #              # html.A(
        #              #     children='hey',
        #              #     id='download-link',
        #              #     download="test.xlsx",
        #              #     href=href_data_downloadable,
        #              #     target="_blank"
        #              # )
        #              ],
        #             sm=6,
        #             align="center",
        #             width={"offset": 2})
        # ),
    ]

    )

])

###############################################################################################################################################
@app.callback(Output("PowerGraphs", "figure"),
                [   Input('Dropdown', 'value'),
                    Input('slider', 'value'),
                    Input('switches', 'value'),],
            [
                # State("RadioPower", "value"),
             ],)
def updateMapRSA(DropdownValue,sliderValue,switchesValue):

    # print(f'DropdownValue is {DropdownValue}')
    # print(f'DropdownValue is {sliderValue}')
    # print(f'DropdownValue is {type(sliderValue)}')
    # print(f'SwitchesValue is {switchesValue}')

#######################################

    if "P"==DropdownValue:
        # print("P")
        title="INSTALLED capacity [MW]"
        yTitle="Installed capacity [MW]"
        DF_IRP=CSIR_LC_2019_E  ##########################
        DF_CSIR=CSIR_LC_2019_P
        c=False
        yrange=[0,4.5e5]  #################
    if "E"==DropdownValue:
        # print("E")
        DF_IRP=IRP2019_E
        DF_CSIR=CSIR_LC_2019_E
        title="ENGERGY produced [GWh]"
        yTitle="Energy produced [GWh]"
        c=True
        yrange=[0,4.5e5]


    traces = []

    if len(switchesValue)>0: # True

        for i, power in enumerate(powerlist):

            traces.append(
                go.Bar(x=[sliderValue],
                       y=CSIR_LC_2019_E[CSIR_LC_2019_E['Year'] == sliderValue][power],
                       name=power,
                       legendgroup=power,
                       # fillcolor=colours[i],
                       marker=dict(color=colours[i]),
                       xaxis='x2',#
                       yaxis='y2',#
                       )
            )

            traces.append(
                go.Bar(x=[sliderValue],
                       y=CSIR_LC_2019_E[CSIR_LC_2019_E['Year'] == sliderValue][power],
                       name=power,
                       legendgroup=power,

                       showlegend=False,
                       marker=dict(color=colours[i]),
                       ))

    else:
        for i, power in enumerate(powerlist):
            traces.append(
                go.Bar(x=CSIR_LC_2019_P['Year'],
                       y=CSIR_LC_2019_P[power],
                       name=power,
                       legendgroup=power,
                       marker=dict(color=colours[i]),
                       )
            )

            traces.append(
                go.Bar(x=CSIR_LC_2019_E['Year'],
                       y=CSIR_LC_2019_E[power],
                       name=power,
                       legendgroup=power,
                       xaxis='x2',
                       yaxis='y2',
                       showlegend=False,
                       marker=dict(color=colours[i]),
                       ))




    figure = dict(data=traces,layout=Powerlayout)
    return figure



@app.callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


if __name__ == '__main__':
    app.run_server(port=8848,debug=True)

