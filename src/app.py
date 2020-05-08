import streamlit as st
import numpy as np
import pandas as pd
import pydeck as pdk

from api.velib import get_station_info, get_station_statuses


st.title("Velo 🚴🏻‍♂️")
st.write("Check the availabity of docked bikes in your city !")
st.markdown("_(if your city is Paris)_")


page = st.sidebar.radio("Graph", ("Number of station", "Availability Heatmaps"))


@st.cache
def get_live_station_information():
    info = get_station_info()
    statuses = get_station_statuses()
    return info.merge(statuses)


map_data = get_live_station_information()

if page == "Number of station":
    radius = st.slider("Radius ?", 50, 300, 100)
    st.pydeck_chart(
        pdk.Deck(
            map_style="mapbox://styles/mapbox/dark-v9",
            initial_view_state=pdk.ViewState(
                latitude=map_data["lat"].mean(),
                longitude=map_data["lon"].mean(),
                zoom=11,
                pitch=40,
            ),
            layers=[
                pdk.Layer(
                    "HexagonLayer",
                    data=map_data,
                    opacity=0.05,
                    get_position="[lon, lat]",
                    pickable=False,
                    radius=radius,
                ),
            ],
        ),
    )


if page == "Availability Heatmaps":
    indicator = st.sidebar.radio(
        "Show indicator", ("Capacity", "Docks Availability", "Bikes Availability")
    )

    if indicator == "Capacity":
        prop = "capacity"
    if indicator == "Docks Availability":
        prop = "num_docks_available"
    if indicator == "Bikes Availability":
        prop = "num_bikes_available"

    st.code(
        """
    def weight():
        return %s
    """
        % prop,
        language="python",
    )

    st.pydeck_chart(
        pdk.Deck(
            map_style="mapbox://styles/mapbox/dark-v9",
            initial_view_state=pdk.ViewState(
                latitude=map_data["lat"].mean(),
                longitude=map_data["lon"].mean(),
                zoom=11,
                pitch=40,
            ),
            layers=[
                pdk.Layer(
                    "HeatmapLayer",
                    map_data,
                    opacity=0.1,
                    get_position=["lon", "lat"],
                    aggregation='"MEAN"',
                    get_weight=prop,
                ),
            ],
        )
    )
