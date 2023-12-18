# app.py
import pandas as pd
from dash import dcc, html, Dash
import dash_bootstrap_components as dbc
from callbacks import callback_hist_age_dist, callback_hist_service
from figures.figure_utils import fig_mean_ages_make, fig_iqr_make, fig_mean_service_make
from utils.calculations import df_strip, df_groups_make, df_age_make, df_count_dict_make, df_iqr_make, service_values
from config import MIN_CONGRESS,MAX_CONGRESS


###########################################
##          Load Data and Calculations

df = pd.read_csv('data/congress_data.csv')
df = df_strip(df) #remove unnecessary data
df_groups = df_groups_make(df) #make dictionary of groups
df_age, df_age_dict = df_age_make(df_groups) #mean ages of all groups
df_count_dict  = df_count_dict_make(df_groups) #counts service lengths all congress
df_iqr = df_iqr_make(df) #iqr for all congress per congress
df_mean_service = pd.read_csv('data/congress_mean_service.csv') #service length mean of all congress per congress
mean_service, total_members = service_values(df)


###########################################
##          Figures

# Create figures using imported functions
fig_mean_ages = fig_mean_ages_make(df_age)
fig_iqr = fig_iqr_make(df_iqr)
fig_mean_service = fig_mean_service_make(df_mean_service)


###########################################
##          Layout

external_stylesheets = [dbc.themes.COSMO]
app = Dash(__name__, external_stylesheets=external_stylesheets)

# Layout definition using imported components
# App layout
app.layout = html.Div(
    dbc.Container([

    # Head
    dbc.Row([
        html.Div('Congress Age and Service', className="text-primary text-center fs-3", style={"margin": "10px"}),
        html.P(children="We explore the aspects of age and length of service of the United States Congress from 1919 to 2023 (or Congress 66 to 118).",
               style={'text-align': 'center'}), 
    ]),

    # Average Ages vs Time Graph
    dbc.Row([
        html.Hr(),
        html.H1(children="Congress and Age"),
        dcc.Graph(figure=fig_mean_ages),
    ]),

    # Histogram for Age Distribution per Congress
    dbc.Row([
        html.Div([
            html.P(children="This is a histogram of the ages of all congresspeople per congress. Use the slider to select a congress. Note the interquartile age difference is indicated.",
                   className="card-header",
            ),
            
            # Slider for selecting congress
            html.Div([
                dcc.Slider(
                    id='congress-slider',
                    min=MIN_CONGRESS,
                    max=MAX_CONGRESS,
                    step=1,
                    value=MAX_CONGRESS,
                ),
            ], style={"margin-top": "20px"}),
            
            # Histogram plot of age distribution per congress
            dcc.Graph(id='age-histogram'),

            # Line graph of iqr per congress
            dcc.Graph(figure=fig_iqr),

            ], 
            className="card mb-3",
            style={"width": "90%",
                "margin": "auto",},
        ),
    ]),

    # Histogram of terms served
    dbc.Row([
        html.Hr(),
        html.H1(children="Congress and Length of Service",style={'margin-top':'10px'}),
        html.P(children="The histogram gives the number of congresses served for different groups of Congress. The pie chart shows the percentages of those falling above or below the average served."),
        

        html.Div([
            # Dropdown for selecting all congress, house, senate, dems, reps
            html.Div([
                dcc.Dropdown(
                    id='served-dropdown',
                    options=[
                        {'label': 'All Congress', 'value': 'All'},
                        {'label': 'House', 'value': 'House'},
                        {'label': 'Senate', 'value': 'Senate'},
                        {'label': 'Dems', 'value': 'Dems'},
                        {'label': 'Reps', 'value': 'Reps'},
                        ],
                    value='All',
                    style={'text-align': 'center', 'font-size':'20px'},  # Default value
                ),
            ], style={"margin-top": "20px"}),
            
            dbc.Row([
                # Histogram plot of terms served
                dbc.Col([
                    dcc.Graph(id='served-histogram'),
                ], width=8),  # out of 12 units,

                # Pie chart of members above and below average
                dbc.Col([
                    dcc.Graph(id='served-pie'),
                ], width=4),  # out of 12 units

            ]),
            
            ], 
            className="card mb-3",
            
            ),  
    ], style={"margin-top":"30px"}),

    # Line Graph terms served
    dbc.Row([
        html.P(children="The below line graph shows the average of congresses served of all congresspeople at the start of each congress. ",
               style={"margin-top":"30px"}),
        
        dcc.Graph(figure=fig_mean_service),
        html.P(children="*Note that due to data limitations, the Average Congresses Served graph must start at a later congress than the minimum of the dataset. It begins at 87 with the longest serving at 87 having begun in 67 to avoid including anyone that served before 66 (the start of the dataset).")
    ]),
    
    ], 
    fluid=True,
    ),
    style={"margin-left": "40px", "margin-right": "40px", "margin-bottom":"50px"},
)


###########################################
##          Callback
# Callback registration using imported callback functions
callback_hist_age_dist.update_hist_age_dist(app, df_groups['All'], df_age_dict['All'],)
callback_hist_service.update_hist_service(app, df_count_dict, mean_service, total_members,)


###########################################
##          main
if __name__ == '__main__':
    app.run_server(debug=True)
