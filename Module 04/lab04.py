# ===================== Task 1: Import required libraries and read the dataset =====================
import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
airline_data = pd.read_csv(
    'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv',
    encoding="ISO-8859-1",
    dtype={
        'Div1Airport': str, 'Div1TailNum': str,
        'Div2Airport': str, 'Div2TailNum': str})
# ===================== Task 2: Create a dash application =====================
app = dash.Dash(__name__)
# ===================== Task 3: Create application layout =====================
app.layout = html.Div([
    html.H1('Flight Delay Time Statistics',style={'textAlign': 'center', 'color': '#503D36', 'font-size': 30}),
    html.Div(["Input Year: ",
              dcc.Input(id='input-year', value='2010', type='number',
                        style={'height':'35px', 'font-size':30}),],
             style={'font-size': 30}),
    html.Br(),
    html.Div([
        html.Div(dcc.Graph(id='carrier-plot')),
        html.Div(dcc.Graph(id='weather-plot'))
    ], style={'display': 'flex'}),
    html.Div([
        html.Div(dcc.Graph(id='nas-plot')),
        html.Div(dcc.Graph(id='security-plot'))
    ], style={'display': 'flex'}),
    html.Div(dcc.Graph(id='late-plot'), style={'width':'65%'})
])
# ===================== Task4: 定义compute_info函数，筛选年份，计算5类延误均值 =====================
def compute_info(airline_data, entered_year):
    df = airline_data[airline_data['Year'] == int(entered_year)]
    carrier_delay = df.groupby(['Month','Reporting_Airline'])['CarrierDelay'].mean().reset_index()
    weather_delay = df.groupby(['Month','Reporting_Airline'])['WeatherDelay'].mean().reset_index()
    nas_delay = df.groupby(['Month','Reporting_Airline'])['NASDelay'].mean().reset_index()
    security_delay = df.groupby(['Month','Reporting_Airline'])['SecurityDelay'].mean().reset_index()
    late_delay = df.groupby(['Month','Reporting_Airline'])['LateAircraftDelay'].mean().reset_index()
    return carrier_delay, weather_delay, nas_delay, security_delay, late_delay
# ===================== Task5: Create callback (1 Input, 5 Outputs) =====================
@app.callback(
    [Output('carrier-plot', 'figure'),
     Output('weather-plot', 'figure'),
     Output('nas-plot', 'figure'),
     Output('security-plot', 'figure'),
     Output('late-plot', 'figure')],
    Input('input-year', 'value'))
def get_graph(entered_year):
    carrier, weather, nas, security, late = compute_info(airline_data, entered_year)
    fig_carrier = px.line(carrier, x='Month', y='CarrierDelay', color='Reporting_Airline',
                          title='Average carrier delay time (minutes) by airline')
    fig_weather = px.line(weather, x='Month', y='WeatherDelay', color='Reporting_Airline',
                          title='Average weather delay time (minutes) by airline')
    fig_nas = px.line(nas, x='Month', y='NASDelay', color='Reporting_Airline',
                      title='Average NAS delay time (minutes) by airline')
    fig_security = px.line(security, x='Month', y='SecurityDelay', color='Reporting_Airline',
                           title='Average security delay time (minutes) by airline')
    fig_late = px.line(late, x='Month', y='LateAircraftDelay', color='Reporting_Airline',
                       title='Average late aircraft delay time (minutes) by airline')
    return [fig_carrier, fig_weather, fig_nas, fig_security, fig_late]
# ===================== Task6: Run the app =====================
if __name__ == '__main__':
    app.run()
