import plotly.express as px

# create line graph of mean ages of each congress for each group
def fig_mean_ages_make(df_age):
    fig = px.line(df_age, x='year', y='age_years', color='group', title='Average Age Over Time')
    fig.update_layout(
        legend_title_text='Groups'
        )
    fig.add_annotation(
        x=.99,
        xref='paper',
        y=.1,
        yref='paper',
        text='Select groups from legend to compare groups',
        showarrow=False,
        font=dict(color='black'), 
        bgcolor='white',
    )
    return fig

# create line graph of interquartile range of each congress
def fig_iqr_make(df_iqr):
    fig = px.line(df_iqr, x='year', y='iqr', line_shape='spline')
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Age Difference",
        title="Age Difference of the Interquartile per Congress",
    )
    return fig

# line graph of mean terms served per congress start for all
def fig_mean_service_make(df_mean_service):
    fig = px.line(df_mean_service, x='Year', y='Terms Served Mean', line_shape='spline')
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Average Congresses Served",
        title='Average Congresses Served for All Congress Over Time',
    )
    return fig

