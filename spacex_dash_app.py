# Import required libraries
from dash.development.base_component import Component
from numpy.typing import _16Bit
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

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown', options=[{'label' : 'All Sites', 'value' : 'ALL'},
                                                                          {'label' : 'CCAFS LC-40', 'value' : 'CCAFS LC-40'},
                                                                          {'label' : 'VAFB SLC-4E', 'value' : 'VAFB SLC-4E'},
                                                                          {'label' : 'KSC LC-39A', 'value' : 'KSC LC-39A'}
                                                                         ], 
                                            value='ALL', placeholder='Select a Lunch Site Here',
                                            searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider', min=0, max=10_000, step=1_000, value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        valcounts = filtered_df.groupby('Launch Site', as_index=False).sum()
        fig = px.pie(valcounts, values='class', names='Launch Site', title='Total success launches by site')
        return fig
    else:
        df_site     = spacex_df[spacex_df["Launch Site"] == entered_site]
        valcounts   = df_site['class'].value_counts().to_frame()
        fig = px.pie(valcounts, values='class', names=valcounts.index, title=f'total success launches for site {entered_site}')
        return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
    Input(component_id='payload-slider', component_property='value')]
)
def get_scatter(entered_site, entered_payload_range):
    low = entered_payload_range[0]
    high = entered_payload_range[1]
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)]
    if entered_site == 'ALL':
        fig = px.scatter(data_frame=filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category')
        return fig
    else:
        booster_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.scatter(data_frame=booster_df, x='Payload Mass (kg)', y='class', color='Booster Version Category')
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
