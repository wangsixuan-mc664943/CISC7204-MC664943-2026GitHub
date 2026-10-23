import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
# TASK 1.2
df = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/'
                 'IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/'
                 'Data%20Files/Historical_Wildfires.csv')
# Derive Year and Month columns from the Date column
df['Year'] = pd.to_datetime(df['Date']).dt.year
df['Month'] = pd.to_datetime(df['Date']).dt.month_name()
# TASK 1.3
app = dash.Dash(__name__)
# TASK 2.1 - 2.3
app.layout = html.Div(children=[
    # TASK 2.1
    html.H1('Australia Wildfire Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    # TASK 2.2 
    html.Div([
        html.H2('Select Region:', style={'margin-right': '2em'}),
        dcc.RadioItems(['NSW', 'QL', 'SA', 'TA', 'VI', 'WA'], 'NSW',id='region', inline=True),]),
    # TASK 2.2 
    html.Div([html.H2('Select Year:', style={'margin-right': '2em'}),
        dcc.Dropdown(df.Year.unique(), value=2005, id='year'),]),
    # TASK 2.3
    html.Div([], id='plot1'),
    html.Div([], id='plot2')])
# TASK 2.4 + 2.5
@app.callback([Output(component_id='plot1', component_property='children'),
               Output(component_id='plot2', component_property='children')],
              [Input(component_id='region', component_property='value'),
               Input(component_id='year', component_property='value')])
def reg_year_display(input_region, input_year):
    region_data = df[df['Region'] == input_region]
    y_r_data = region_data[region_data['Year'] == input_year]
    est_data = y_r_data.groupby('Month')['Estimated_fire_area'].mean().reset_index()
    fig1 = px.pie(est_data, values='Estimated_fire_area', names='Month',
                  title='{} : Monthly Average Estimated Fire Area in year {}'.format(input_region, input_year))
    veg_data = y_r_data.groupby('Month')['Count'].mean().reset_index()
    fig2 = px.bar(veg_data, x='Month', y='Count',
                  title='{} : Average Count of Pixels for Presumed Vegetation Fires in year {}'.format(input_region, input_year))
    return [dcc.Graph(figure=fig1),
            dcc.Graph(figure=fig2)]
if __name__ == '__main__':
    app.run(debug=True)
