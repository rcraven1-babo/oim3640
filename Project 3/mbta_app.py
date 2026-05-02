import os
import math
import requests
from urllib.parse import quote_plus
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

MAPBOX_TOKEN = os.getenv(
    "MAPBOX_TOKEN",
    "pk.eyJ1IjoicmNyYXZlbiIsImEiOiJjbW8xbHMxbzIwa3BtMnNvZ3V6Z3czc203In0.NW0QYn40eV4fAMPK1Mco_g"
)
MBTA_API_KEY = os.getenv("MBTA_API_KEY", "1be9a3cc48394870a69f15774a620665")


def haversine(lat1, lon1, lat2, lon2):
    radius = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return radius * c


def geocode_address(query):
    url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{quote_plus(query)}.json"
    params = {"access_token": MAPBOX_TOKEN, "limit": 1}
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    features = data.get("features", [])
    if not features:
        return None

    feature = features[0]
    lon, lat = feature["center"]
    return {
        "place_name": feature.get("place_name", query),
        "latitude": lat,
        "longitude": lon,
    }


def find_nearest_mbta(lat, lon):
    # Find nearest stop
    url = "https://api-v3.mbta.com/stops"
    params = {
        "filter[latitude]": lat,
        "filter[longitude]": lon,
        "sort": "distance",
        "page[limit]": 1,
    }
    if MBTA_API_KEY:
        params["api_key"] = MBTA_API_KEY

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    stops = data.get("data", [])
    if not stops:
        return None

    stop = stops[0]
    stop_attrs = stop.get("attributes", {})
    stop_lat = stop_attrs.get("latitude")
    stop_lon = stop_attrs.get("longitude")
    distance_km = haversine(lat, lon, stop_lat, stop_lon)

    stop_name = stop_attrs.get("name", "Unknown stop")
    stop_desc = stop_attrs.get("description")

    # Get routes serving this stop
    route_names = []
    try:
        stop_id = stop.get("id")
        if stop_id:
            routes_resp = requests.get(
                "https://api-v3.mbta.com/routes",
                params={"filter[stop]": stop_id, "api_key": MBTA_API_KEY},
                timeout=8
            )
            routes_resp.raise_for_status()
            for r in routes_resp.json().get