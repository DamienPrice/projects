from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# hist and pie of terms served
def update_hist_service(app, df_count_dict, mean_service, total_members,):
    # callback for served data
    @app.callback(
        [Output('served-histogram', 'figure'), Output('served-pie','figure')],
        [Input('served-dropdown', 'value')]
    )
    def update_histogram_terms_served(selected_group):
        df_bioguide_id_counts = df_count_dict[selected_group]

        ##########
        # Create a histogram of terms served
        fig_hist = px.histogram(df_bioguide_id_counts, x='count',)

        # histogram settings
        custom_tick_values = [x for x in range(0,31,1)]
        fig_hist.update_layout(
            xaxis=dict(
                tickvals=custom_tick_values,
                tickmode='array',
                range=[0,30],
            ),
            xaxis_title="Total Congresses Served",
            yaxis_title="Frequency",
            title=f"How Many Served for How Long in {selected_group}",
        )

        # mean service line
        fig_hist.add_vline(x=mean_service, line_dash = 'dash', line_color = 'firebrick')

        # annots for mean service and total members
        fig_hist.update_layout(
            annotations=[
                dict(
                    x=mean_service,
                    y=1000,
                    xref='x',
                    yref='y',
                    text=f'Average: {mean_service:.2f}',
                    showarrow=False,
                    font=dict(color='black'),
                    bgcolor='white',
                ),
                dict(
                    x=.8,
                    y=.8,
                    xref='paper',
                    yref='paper',
                    text=f'Total All Time Members for All: {total_members}',
                    showarrow=False,
                    font=dict(color='black'),
                    bgcolor='white',
                )
            ]
        )

        ##########
        # Pie Chart
        # df for occurences above and below rounded mean
        count_summary = pd.DataFrame({
            'Placement': ['Served <= Average','Served > Average'],
            'Count': [df_bioguide_id_counts['count'].loc[df_bioguide_id_counts['count'] <= 6].sum(),
                    df_bioguide_id_counts['count'].loc[df_bioguide_id_counts['count'] > 6].sum(),
                    ]
        })

        # Create a pie chart using Plotly Express
        fig_pie = px.pie(count_summary, names='Placement', values='Count',)
        fig_pie.update_layout(
            title=dict(
                text=f'Above and Below Rounded Average for {selected_group}',
                y=0.95,  
                x=0.5,   
                xanchor='center',
                yanchor='top',
                font=dict(size=16)
            ),
            
            legend=dict(orientation="h", yanchor="bottom", 
                        y=-0.2, xanchor="right", x=0.5, 
                        font=dict(size=16)),
            
            # chart size
            height=350,  
            width=350,

            font=dict(size=20)    
        )
        return fig_hist, fig_pie