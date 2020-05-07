import streamlit as st
import numpy as np
import pandas as pd
import pydeck as pdk

from api.velib import get_station_info, get_station_statuses


st.title("Velo 🚴🏻‍♂️")
st.write("Check the availabity of docked bike in your city !")
st.markdown("_(if your city is Paris)_")


@st.cache
def get_live_station_information():
    info = get_station_info()
    statuses = get_station_statuses()
    return info.merge(statuses)


show_capacity = st.sidebar.checkbox("Show capacity", True)
show_availability = st.sidebar.checkbox("Show availability", False)
show_non_availability = st.sidebar.checkbox("Show non-availability", False)

map_data = get_live_station_information()
st.pydeck_chart(
    pdk.Deck(
        map_style="mapbox://styles/mapbox/dark-v9",
        initial_view_state=pdk.ViewState(
            latitude=map_data["lat"].mean(),
            longitude=map_data["lon"].mean(),
            zoom=11,
            pitch=20,
        ),
        layers=[
            show_capacity
            and pdk.Layer(
                "HeatmapLayer",
                data=map_data,
                opacity=0.1,
                get_position="[lon, lat]",
                get_weight="capacity",
            ),
            show_availability
            and pdk.Layer(
                "HeatmapLayer",
                data=map_data,
                opacity=0.1,
                get_position="[lon, lat]",
                get_weight="num_bikes_available / capacity",
            ),
            show_non_availability
            and pdk.Layer(
                "HeatmapLayer",
                data=map_data,
                opacity=0.1,
                get_position="[lon, lat]",
                get_weight="1 - num_bikes_available / capacity",
            ),
        ],
    )
)
