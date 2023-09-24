import plotly.graph_objects as go
import plotly.express as px

def bar_plot(df):
    fig = px.line(df, 't', 'o')
    return fig