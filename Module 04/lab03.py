import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
airline_data =  pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv', 
                            encoding = "ISO-8859-1",
                            dtype={'Div1Airport': str, 'Div1TailNum': str, 'Div2Airport': str, 'Div2TailNum': str})
app = dash.Dash(__name__)
app.layout = html.Div(children=[ 
    html.H1('Airline Performance Dashboard', style={'textAlign': 'center', 'color': '#503D36','font-size': 40}),
    html.Div(["Input Year: ", dcc.Input(id='input-year', value='2010', type='number', style={'height':'50px', 'font-size': 35}),], 
              style={'font-size': 40}),
    html.Br(),html.Br(),html.Div(dcc.Graph(id='line-plot')),html.Br(),html.Div(dcc.Graph(id='bar-plot'))])
@app.callback(
    [Output('line-plot', 'figure'),
     Output('bar-plot', 'figure')],
    Input('input-year', 'value'))
def get_graph(entered_year):
    df = airline_data[airline_data['Year'] == int(entered_year)]
    line_data = df.groupby('Month')['ArrDelay'].mean().reset_index()
    fig_line = go.Figure(data=go.Scatter(x=line_data['Month'], y=line_data['ArrDelay'], mode='lines', marker=dict(color='green')))
    fig_line.update_layout(title='Month vs Average Flight Delay Time', xaxis_title='Month', yaxis_title='ArrDelay')
    bar_data = df.groupby(['DestState','Reporting_Airline'])['Flights'].sum().reset_index()
    fig_bar = go.Figure()
    for airline in bar_data['Reporting_Airline'].unique():
        df_air = bar_data[bar_data['Reporting_Airline'] == airline]
        fig_bar.add_trace(go.Bar(x=df_air['DestState'], y=df_air['Flights'], name=airline))
    fig_bar.update_layout(
        title='Total number of flights to the destination state split by reporting airline',
        xaxis_title="Destination State",
        yaxis_title="Flights",
        barmode="stack")
    return fig_line, fig_bar
if __name__ == '__main__':
    app.run()
