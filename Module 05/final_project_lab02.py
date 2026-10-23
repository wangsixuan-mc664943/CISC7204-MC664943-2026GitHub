# Final Assignment Part 2: Automobile Sales Statistics Dashboard
# -*- coding: utf-8 -*-
# ---------------- TASK 1: imports ----------------
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
# Read the automobile sales data (downloaded once, stored locally beside this file)
data = pd.read_csv('historical_automobile_sales.csv')
# List of years used in the Year dropdown (1980 to 2023)
year_list = [i for i in range(1980, 2024, 1)]
# ---------------- TASK 2.1: create the app and the title ----------------
app = dash.Dash(__name__)
app.layout = html.Div(children=[
    # Title: centered, color #503D36, font-size 24
    html.H1('Automobile Sales Statistics Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 24}),
    # ---------------- TASK 2.2: dropdown 1 - report type ----------------
    html.Div([
        html.H2('Select Statistics:', style={'margin-right': '2em'}),
        dcc.Dropdown(id='dropdown-statistics',options=[
                {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}],
            value='Select Statistics',placeholder='Select Statistics',
            style={'width': '80%', 'padding': '3px', 'font-size': '20px',
                   'text-align-last': 'center'})]),
    # ---------------- TASK 2.2: dropdown 2 - year ----------------
    html.Div([html.H2('Select Year:', style={'margin-right': '2em'}),dcc.Dropdown(
            id='select-year',options=[{'label': i, 'value': i} for i in year_list],
            value='Select Year',placeholder='select-year',
            style={'width': '80%', 'padding': '3px', 'font-size': '20px',
                   'text-align-last': 'center'})]),
    # ---------------- TASK 2.3: output container ----------------
    html.Div(id='output-container', className='chart-grid', style={'display': 'flex'})])
# ---------------- TASK 2.4a: enable/disable the year dropdown ----------------
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value'))
def update_input_container(selected_statistics):
    # The year dropdown only matters for Yearly Statistics reports.
    if selected_statistics == 'Yearly Statistics':
        return False          # enabled
    else:
        return True           # disabled (greyed out)
# ---------------- TASK 2.4b / 2.5 / 2.6: build the report charts ----------------
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value'),
     Input(component_id='select-year', component_property='value')])
def update_output_container(selected_statistics, input_year):
    if selected_statistics == 'Recession Period Statistics':
        # TASK 2.5: recession report - filter only recession periods
        recession_data = data[data['Recession'] == 1]
        # Plot 1: average automobile sales fluctuation per year (line chart)
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(yearly_rec, x='Year', y='Automobile_Sales',
                           title="Automobile Sales fluctuation per Year during Recession"))
        # Plot 2: average number of vehicles sold by vehicle type (bar chart)
        avg_sold = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.bar(avg_sold, x='Vehicle_Type', y='Automobile_Sales',
                          title='Average Vehicles Sold by Vehicle Type during Recession'))
        # Plot 3: total advertising expenditure share by vehicle type (pie chart)
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum()
        R_chart3 = dcc.Graph(
            figure=px.pie(values=exp_rec.values, names=exp_rec.index,
                          title='Total Advertisement Expenditure Share by Vehicle Type during Recession'))
        # Plot 4: effect of unemployment rate on vehicle type and sales (bar chart)
        unemp_rec = recession_data.groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        R_chart4 = dcc.Graph(
            figure=px.bar(unemp_rec, x='unemployment_rate', y='Automobile_Sales',
                          color='Vehicle_Type',
                          labels={'unemployment_rate': 'Unemployment Rate',
                                  'Automobile_Sales': 'Average Automobile Sales'},
                          title='Effect of Unemployment Rate on Vehicle Type and Sales'))
        # Two rows of two charts each
        return [
            html.Div(className='chart-item',
                     children=[html.Div(children=R_chart1), html.Div(children=R_chart2)],
                     style={'display': 'flex'}),
            html.Div(className='chart-item',
                     children=[html.Div(children=R_chart3), html.Div(children=R_chart4)],
                     style={'display': 'flex'})
        ]
    elif (selected_statistics == 'Yearly Statistics') and (input_year in year_list):
        # TASK 2.6: yearly report - filter the selected year where needed
        # Plot 1: yearly average automobile sales (line chart, all years)
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(yas, x='Year', y='Automobile_Sales',
                           title='Yearly Average Automobile Sales'))
        # Plot 2: total automobile sales per year (line chart, all years)
        tas = data.groupby('Year')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(
            figure=px.line(tas, x='Year', y='Automobile_Sales',
                           title='Total Automobile Sales per Year'))
        # Plot 3: average vehicles sold by vehicle type in the selected year (bar chart)
        bar_chart = data[data['Year'] == input_year].groupby('Vehicle_Type')['Automobile_Sales'].mean()
        Y_chart3 = dcc.Graph(
            figure=px.bar(x=bar_chart.index, y=bar_chart.values,
                          title='Average Vehicles Sold by Vehicle Type in the year {}'.format(input_year),
                          labels={'x': 'Vehicle Type', 'y': 'Average Automobile Sales'}))
        # Plot 4: total advertising expenditure by vehicle type in the selected year (pie chart)
        exp_data = data[data['Year'] == input_year].groupby('Vehicle_Type')['Advertising_Expenditure'].sum()
        Y_chart4 = dcc.Graph(
            figure=px.pie(values=exp_data.values, names=exp_data.index,
                          title='Total Advertisement Expenditure for each Vehicle Type in the year {}'.format(input_year)))
        # Plot 5: effect of unemployment rate on automobile sales (line chart, all years)
        unemp_data = data.groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        Y_chart5 = dcc.Graph(
            figure=px.line(unemp_data, x='unemployment_rate', y='Automobile_Sales',
                           color='Vehicle_Type',
                           labels={'unemployment_rate': 'Unemployment Rate',
                                   'Automobile_Sales': 'Average Automobile Sales'},
                           title='Effect of Unemployment Rate on Automobile Sales'))
        # One row of three charts + one row of two charts
        return [html.Div(className='chart-item',
                     children=[html.Div(children=Y_chart1), html.Div(children=Y_chart2),
                               html.Div(children=Y_chart3)],
                     style={'display': 'flex'}),
            html.Div(className='chart-item',
                     children=[html.Div(children=Y_chart4), html.Div(children=Y_chart5)],
                     style={'display': 'flex'})]
    else:
        # Nothing selected yet
        return []
if __name__ == '__main__':
    app.run(debug=True)
