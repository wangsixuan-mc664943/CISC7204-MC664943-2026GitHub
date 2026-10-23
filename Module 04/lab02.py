# ---------------------------------------------------------------
# TASK 3: Create a basic Dash application and run it
# TASK 4: Add the application description (html.H1 title + html.P paragraph)
# TASK 5: Update the graph (dcc.Graph core component with a pie chart)
# ---------------------------------------------------------------
# Import required libraries
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc
# Load the airline dataset (Airline Reporting Carrier On-Time Performance)
airline_data = pd.read_csv("airline_data.csv",
    encoding="ISO-8859-1",
    dtype={'Div1Airport': str, 'Div1TailNum': str,
           'Div2Airport': str, 'Div2TailNum': str})
# Randomly sample 500 rows to keep the chart light and responsive
data = airline_data.sample(n=500, random_state=42)
# TASK 5 (part 1): Build the pie chart figure - proportion of flights by distance group
fig = px.pie(data, values='Flights', names='DistanceGroup',
             title='Distance group proportion by flights')
# Create a dash application
app = Dash(__name__)
# Get the layout of the application and adjust it.
# TASK 4: Create an outer division using html.Div and add title to the
#         dashboard using html.H1 component.
# TASK 4: Add description about the graph using HTML P (paragraph) component.
# TASK 5 (part 2): Finally, add the graph component dcc.Graph.
app.layout = html.Div(children=[
    html.H1('Airline On-time Performance Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 50}),
    html.P('Proportion of distance group (250 mile distance interval group) by flights.',
           style={'textAlign': 'center', 'color': '#F57241'}),
    dcc.Graph(figure=fig),
])
# Run the application on http://127.0.0.1:8050
if __name__ == '__main__':
    app.run(debug=True)
