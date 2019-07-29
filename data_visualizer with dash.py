import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
from collections import deque
import pandas as pd
import pyodbc


def connectSQLServer(driver, server, db):
    connSQLServer = pyodbc.connect(
        r'DRIVER={' + driver + '};'
        r'SERVER=' + server + ';'
        r'DATABASE=' + db + ';'
        r'Trusted_Connection=yes;',
        autocommit=True
    )
    return connSQLServer 


name_title = 'Stats from SQL Server'
app = dash.Dash(__name__)

app.layout = html.Div(children=[
        
    html.H1(children='Read Id Number and Number From MS SQL Server',style={'textAlign': "center"}),
     dcc.Graph(
        id='example-graph',animate=True),dcc.Interval(id='graph-update',interval=1*2000, n_intervals=0)])

    
@app.callback(Output('example-graph', 'figure'), 
              [Input('graph-update', 'n_intervals')])


def update_graph_scatter(data):

    dataSQL = [] #set an empty list
    X=deque(maxlen=20)    
    Y=deque(maxlen=20)

    sql_conn = connectSQLServer('ODBC Driver 13 for SQL Server', 'F8-CRUSADER-M18', 'test') 
    cursor = sql_conn.cursor()
    cursor.execute("SELECT Num,ID FROM dbo.number")
    rows = cursor.fetchall()
    for row in rows:
        dataSQL.append(list(row))
        labels = ['Num','ID']
        df = pd.DataFrame.from_records(dataSQL, columns=labels)
        X = df['ID']
        Y = df['Num']
        

    data = plotly.graph_objs.Scatter(
            x=list(X),
            y=list(Y),
            name='Scatter',
            mode= 'lines'
            )

    return {'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(X),max(X)],title = 'ID NUMBER'),
                                                yaxis=dict(range=[min(Y),max(Y)],title = 'Number'),)}

if __name__ == "__main__":
    app.run_server(debug=True)