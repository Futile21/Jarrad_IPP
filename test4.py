import dash
import dash_table
import pandas as pd
import numpy as np

IRP2019_P = pd.read_excel('2019-IRP.xlsx', sheet_name="IRP1_P").round(1)
IRP2019_E = pd.read_excel('2019-IRP.xlsx', sheet_name="IRP1_E").round(1)

CSIR_LC_2019_P = pd.read_excel('2019-CSIR_LC.xlsx', sheet_name="IRP1_P").round(1)
CSIR_LC_2019_E = pd.read_excel('2019-CSIR_LC.xlsx', sheet_name="IRP1_E").round(1)



powerlist =list(CSIR_LC_2019_E.columns)
print(powerlist)
removelist=[powerlist[0],powerlist[11],powerlist[13]]
removelist

for i in removelist:
    print(f'remove {i}')
    powerlist.remove(i)

print("")
print(powerlist)
print(len(powerlist))




g=(CSIR_LC_2019_E[CSIR_LC_2019_E['Year']==2018][powerlist])
h=(CSIR_LC_2019_P[CSIR_LC_2019_P['Year']==2018][powerlist])

data = {'Power' : powerlist, 'IPP':np.array(g)[0], 'Color' : np.array(h)[0]}
df = pd.DataFrame(data)

app = dash.Dash(__name__)

app.layout = dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in df.columns],
    data=df.to_dict('records'),
)

if __name__ == '__main__':
    app.run_server(debug=True)