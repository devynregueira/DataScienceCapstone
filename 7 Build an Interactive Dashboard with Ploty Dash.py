# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
launchSites = set(spacex_df["Launch Site"].to_list())
drop_options = [{'label': x, 'value': x} for x in launchSites]
drop_options.insert(0,{'label': 'All Sites', 'value': 'ALL'})

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',options=drop_options, value="ALL",placeholder="Select a Launch Site Here",searchable=True),
                                #dcc.Dropdown(df.Year.unique(), value = 2005,id='year')
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',min=0, max=10000, step=1000, marks={0: '0',100: '100'},value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback( 
    Output(component_id="success-pie-chart", component_property = "figure"), 
    Input(component_id="site-dropdown", component_property = "value")
)

def createPieChart(site):
    if site == "ALL":
        pie_data = spacex_df.groupby('Launch Site')["class"].sum().reset_index()
        fig = px.pie(pie_data, values='class', names='Launch Site', title='Total Successful Launches by Site')
        return fig
    else:
        pie_data = spacex_df[spacex_df["Launch Site"] == site]["class"].value_counts().reset_index()
        pie_data.columns = ["class","count"]
        fig = px.pie(pie_data, values='count', names='class', title='Total Successful For Site ' + site)
        return fig

    
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback( 
    Output(component_id="success-payload-scatter-chart", component_property = "figure"), 
    [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")]
)

def createScatterPlot(site,pl_rng):
    pl = 'Payload Mass (kg)'
    scatter_data = spacex_df[spacex_df[pl] >= pl_rng[0]]
    scatter_data = scatter_data[spacex_df[pl] <= pl_rng[1]]
    scatter_data = scatter_data if site == "ALL" else scatter_data[scatter_data["Launch Site"] == site]
    
    fig = px.scatter(scatter_data, x='Payload Mass (kg)', y='class', title='Launch Outcome by Payload Mass', color="Booster Version Category")
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
