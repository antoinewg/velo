import requests as re
import pandas as pd


BASE_VELIB_URL = "https://velib-metropole-opendata.smoove.pro/opendata/Velib_Metropole/"
STATION_STATUS_URL = BASE_VELIB_URL + "station_status.json"
STATION_INFORMATION_URL = BASE_VELIB_URL + "station_information.json"


def get_station_info():
    information = re.get(STATION_INFORMATION_URL).json()
    records = information.get("data", {}).get("stations", [])
    return pd.DataFrame.from_records(
        [
            {
                "station_id": record["station_id"],
                "name": record["name"],
                "lat": record["lat"],
                "lon": record["lon"],
                "capacity": record["capacity"],
            }
            for record in records
        ]
    )


def get_station_statuses():
    statuses = re.get(STATION_STATUS_URL).json()
    records = statuses.get("data", {}).get("stations", [])
    return pd.DataFrame.from_records(
        [
            {
                "station_id": record["station_id"],
                "num_bikes_available": record["num_bikes_available"],
                # "num_bikes_available_mechanical": record["num_bikes_available_types"][
                #     "mechanical"
                # ],
                # "num_bikes_available_ebike": record["num_bikes_available_types"][
                #     "ebike"
                # ],
                "num_docks_available": record["num_docks_available"],
                "last_reported": record["last_reported"],
            }
            for record in records
        ]
    )
