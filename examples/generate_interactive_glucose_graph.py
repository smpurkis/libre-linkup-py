from libre_link_up import LibreLinkUpClient
import os
import dotenv
import plotly.graph_objects as go
import datetime

dotenv.load_dotenv()


"""
We will do the following:
- Create a new `LibreLinkUpClient` instance
- Log in
- Get the graph readings
- Plot an interactive graph using `plotly`
"""

if __name__ == "__main__":
    client = LibreLinkUpClient(
        username=os.environ["LIBRE_LINK_UP_USERNAME"],
        password=os.environ["LIBRE_LINK_UP_PASSWORD"],
        url=os.environ["LIBRE_LINK_UP_URL"],
        version="4.7.0",
    )
    client.login()

    graph_reading = client.get_graph_readings()
    x = [
        datetime.datetime.fromtimestamp(reading.unix_timestamp)
        for reading in graph_reading
    ]
    y = [reading.value for reading in graph_reading]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode="lines+markers", hoverinfo="x+y"))
    fig.update_layout(
        title="Glucose readings",
        xaxis_title="Time",
        yaxis_title="Glucose value",
        hovermode="x",
        template="plotly_dark",
    )
    fig.show()
