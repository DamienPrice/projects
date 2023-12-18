from dash.dependencies import Input, Output
import numpy as np
import plotly.express as px
from config import Q1_VAL,Q2_VAL


# ===============
# callback for average
def update_hist_age_dist(app, df, df_age):
    @app.callback(
        Output('age-histogram', 'figure'),
        [Input('congress-slider', 'value')]
    )
    def update_histogram_age_dist(selected_congress,):
        #get year and df for selected_congress
        year = df.loc[(df['congress'] == selected_congress), 'year'].values[0]     
        selected_df = df[df['congress'] == selected_congress]

        ##########
        # Histogram of age distribution
        fig = px.histogram(selected_df, x='age_years', nbins=30,
                        title=f'Age Distribution - All Congress {selected_congress} - Year {year}',
                        labels={'age_years': 'Age', 'count': 'Frequency'})
        
        #####
        # histogram settings
        # set y max
        f = fig.full_figure_for_development(warn=False)
        xbins = f.data[0].xbins
        plotbins = list(np.arange(start=xbins['start'], stop=xbins['end']+xbins['size'], step=xbins['size']))
        counts, bins = np.histogram(list(f.data[0].x), bins=plotbins)
        max_y = max(counts)+3

        # Set the x domain, y range
        fig.update_xaxes(range=[20, 100])
        fig.update_yaxes(range=[0, max_y])

        fig.update_layout(
            xaxis_title="Age",
            yaxis_title="Frequency",
        )

        ##########
        # line of mean
        mean_age_selected = df_age.loc[df_age['congress'] == selected_congress, 'age_years'].values[0]
        fig.add_vline(x=mean_age_selected, line_dash='dash', line_color='firebrick')
        fig.add_annotation(
            x=mean_age_selected,
            y=max_y,
            text=f'Average: {mean_age_selected:.2f}',
            showarrow=False,
            arrowhead=4,
            ax=0,
            ay=-40
        )

        ##########
        # IQR Display
        # get list of age_years for the interquartile 
        age_selected_data = selected_df['age_years'].tolist()
        
        # Calculate Q1, Q3, and IQR
        q1 = np.percentile(age_selected_data, Q1_VAL*100)
        q3 = np.percentile(age_selected_data, Q2_VAL*100)
        iqr = q3 - q1
        
        # Add vertical lines for Q1, Q3, and horizontal line for IQR
        fig.add_shape(type='line', x0=q1, x1=q1, y0=0, y1=10, line=dict(color='red', width=2)) #vert line 1
        fig.add_shape(type='line', x0=q3, x1=q3, y0=0, y1=10, line=dict(color='red', width=2)) #vert line 2
        fig.add_shape(type='line', x0=q1, x1=q3, y0=5, y1=5, line=dict(color='red', width=2)) #hori line
        fig.add_annotation(
            x=iqr/2+q1,
            y=5.1,
            text=f'{iqr:.2f} years',
            showarrow=False,
            font=dict(color='black'), 
            bgcolor='white', 
        )
        return fig