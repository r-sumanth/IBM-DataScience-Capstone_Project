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

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                            options=[{'label':'All Sites','value':'ALL'},
                                                {'label':'CCAFS LC-40','value':'CCAFS LC-40'},
                                                {'label':'CCAFS SLC-40','value':'CCAFS SLC-40'},
                                                {'label':'VAFB SLC-4E','value':'VAFB SLC-4E'},
                                                {'label':'KSC LC-39A','value':'KSC LC-39A'}],
                                                value='ALL',
                                                placeholder='Select a Launch Site here',
                                                searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0,max=10000,step=1000,
                                                value=[0,10000],
                                                marks={x:str(x) for x in range(0,10001,1000)}
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart',component_property='figure'),
    Input(component_id='site-dropdown',component_property='value'))
def get_pie_chart(entered_site):
    if entered_site=='ALL':
        filtered_df=spacex_df.groupby('Launch Site')['class'].sum()
        fig=px.pie(filtered_df,values='class',names=spacex_df['Launch Site'].unique(),
        title='Total success launches by site')
        return fig
    else:
        filtered_df=filtered_df=spacex_df[spacex_df['Launch Site']==entered_site].value_counts('class').reset_index()
        fig=px.pie(filtered_df,values='count',names=['Success','Failure'],
        title=f'Total success launches for site {entered_site}')
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart',component_property='figure'),
    Input(component_id='site-dropdown',component_property='value'),
    Input(component_id='payload-slider',component_property='value'))
def get_scatter_plot(entered_site,payload_range):
    if entered_site=='ALL':
        filtered_df=spacex_df[spacex_df['Payload Mass (kg)']>payload_range[0]]
        filtered_df=filtered_df[filtered_df['Payload Mass (kg)']<payload_range[1]]
        fig=px.scatter(data_frame=filtered_df,x='Payload Mass (kg)',y='class',
        color='Booster Version Category',size='Payload Mass (kg)',
        title='Correlation between Payload and Success for all sites')
        return fig
    else:
        filtered_df=spacex_df[spacex_df['Launch Site']==entered_site]
        filtered_df=filtered_df[filtered_df['Payload Mass (kg)']>payload_range[0]]
        filtered_df=filtered_df[filtered_df['Payload Mass (kg)']<payload_range[1]]
        fig=px.scatter(data_frame=filtered_df,x='Payload Mass (kg)',y='class',
        color='Booster Version Category',size='Payload Mass (kg)',
        title=f'Correlation between Payload and Success for the site {entered_site}')
        return fig 

# Run the app
if __name__ == '__main__':
    app.run_server()
