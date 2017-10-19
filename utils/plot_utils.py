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