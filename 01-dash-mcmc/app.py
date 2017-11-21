import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import plotly as py
import plotly.graph_objs as go
import pymc3 as pm
import matplotlib.pyplot as plt
import pickle
import pandas as pd
import json

# load the posterior object saved as a pickle object
with open('posterior_lm.pkl', 'rb') as f:
    posterior = pickle.load(f)

# create traceplot object
tp = pm.traceplot(posterior)
fig1 = plt.gcf()
plotly_fig1 = py.tools.mpl_to_plotly(fig1)

#create energy plot object
ep = pm.energyplot(posterior)
fig2 = plt.gcf()
plotly_fig2 = py.tools.mpl_to_plotly(fig2)

# create foresplot for beta
fp1 = pm.forestplot(posterior, varnames = ["beta"])
fig3 = plt.gcf()
plotly_fig3 = py.tools.mpl_to_plotly(fig3)

# create foresplot for alpha
fp2 = pm.forestplot(posterior, varnames = ["alpha"])
fig4 = plt.gcf()
plotly_fig4 = py.tools.mpl_to_plotly(fig4)

# create foresplot for sigma
fp3 = pm.forestplot(posterior, varnames = ["sigma"])
fig5 = plt.gcf()
plotly_fig5 = py.tools.mpl_to_plotly(fig5)

# create posteriorplot object
pp = pm.plot_posterior(posterior)
fig6 = plt.gcf()
plotly_fig6 = py.tools.mpl_to_plotly(fig6)

# create dataframe of posterior summaries
posterior_df = pm.df_summary(posterior)
posterior_df = posterior_df.reset_index()

app = dash.Dash()

app.layout = html.Div(children = [
        html.H1(children = "Visualize Posterior Distributions of Parameters", style = {"align" : "justify"}),
        html.Div(children = [
                html.H2(children = "Traceplots"),
                dcc.Graph(
                        id = "traceplot-graph",
                        figure = plotly_fig1
                        )
            ], style={'width': '100%',
               'display': 'inline-block'}),
        html.Div(children = [
                html.H2(children = "Energy plot"),
                dcc.Graph(
                        id = "enerygplot-graph",
                        figure = plotly_fig2
                        )
            ], style={'width': '40%',
               'display': 'inline-block'}),
        html.Div(children = [
                html.H2(children = "Forestplot for beta"),
                dcc.Graph(
                        id = "forestplot-beta",
                        figure = plotly_fig3
                        )
            ], style={'width': '50%',
               'display': 'inline-block'}),
        html.Div(children = [
                html.H2(children = "Forestplot for alpha"),
                dcc.Graph(
                        id = "forestplot-alpha",
                        figure = plotly_fig4
                        )
            ], style={'width': '50%',
               'display': 'inline-block'}),
        html.Div(children = [
                html.H2(children = "Forestplot for sigma"),
                dcc.Graph(
                        id = "forestplot-sigma",
                        figure = plotly_fig5
                        )
            ], style={'width': '50%',
               'display': 'inline-block'}),
        html.Div(children = [
                html.H2(children = "Posterior"),
                dcc.Graph(
                        id = "posterior-graph",
                        figure = plotly_fig6
                        )
            ], style={'width': '100%',
               'display': 'inline-block'}),
        html.Div(children = [
                html.H2(children = "Summary table"),
                dt.DataTable(
                        rows = posterior_df.to_dict('records'),
                        row_selectable=True,
                        filterable=True,
                        editable=True,
                        sortable=True,
                        selected_row_indices=[],
                        id='datatable-posterior'
                        )
            ], style={'width': '100%',
               'display': 'inline-block'})
    ], style = {"margin-top": '20',
                "margin-left": '200',
                "margin-right": '20'})

if __name__ == '__main__':
    app.run_server(debug=True)
