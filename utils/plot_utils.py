from datetime import date
import sqlalchemy as sa
import pandas as pd
from plotly.offline import download_plotlyjs, init_notebook_mode, iplot
from plotly.graph_objs import Scatter, Figure, Layout, Histogram, Heatmap
from plotly import tools
init_notebook_mode(connected=True)


# Some nice defaults for plotting in plotly
def plot(data, title='', show_legend=True, hover_info=True, zoom=True, interactive=False, size=(800, 600)):
    if not interactive:
        hover_info = False
        zoom = False

    if not hover_info:
        for d in data:
            try:
                d.hoverinfo = 'skip'
            except:
                pass

    layout = Layout(title=title, legend=dict(orientation="h"))
    layout.xaxis.fixedrange = not zoom
    layout.yaxis.fixedrange = not zoom
    fig = Figure(data=data, layout=layout)
    config = dict(displayModeBar=False)
    iplot(fig, show_link=False, config=config, image_width=size[0], image_height=size[1])


def plot_subplot(data, titles, main_title, rows, cols, show_legend=True,
                 hover_info=True, zoom=True, interactive=True):
    # Plot subplots. Order of plots are along each row one at a time.
    # For example:
    #     1 2 3 4
    #     5 6 7 8
    # According to source code we can make figure last
    # https://github.com/plotly/plotly.py/blob/master/plotly/tools.py
    assert rows * cols == len(data)

    if not interactive:
        hover_info = False
        zoom = False

    fig = tools.make_subplots(rows=rows, cols=cols, subplot_titles=titles)
    for i, d in enumerate(data):
        n = i + 1
        if type(d) != str:
            d.xaxis = 'x{}'.format(n)
            d.yaxis = 'y{}'.format(n)
        fig['layout']['xaxis{}'.format(n)].update(fixedrange=not zoom)
        fig['layout']['yaxis{}'.format(n)].update(fixedrange=not zoom)
        if not hover_info:
            d.hoverinfo = 'skip'

    fig['data'] = data
    fig['layout'].update(showlegend=show_legend,
                         title=main_title,
                         legend=dict(orientation="h"))
    config = dict(displayModeBar=False)
    iplot(fig, show_link=False, config=config)


# Create a database file using sqlite
engine = sa.create_engine('sqlite:///cl_basic_data_analysis.db')


# Make it easier to download data by making a generatic function
def data_from_table(table_name, index_col=None):
    return pd.read_sql_query('SELECT * FROM {}'.format(table_name),
                             con=engine, index_col=index_col)


# We will probably want to use a datetime field for plotting so we will do that now
def gen_datetime_col(df, year_col, month_col, day_col):
    # Takes in 3 series: year, month and day, and converts to a new series of type date
    return df[[year_col, month_col, day_col]].apply(lambda x: date(x[0], x[1], x[2]), axis=1)