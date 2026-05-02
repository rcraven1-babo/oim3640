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
MBTA_API_KEY = os.getenv("MBTA_API_KEY", "")


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
    url = "https://api-v3.mbta.com/stops"
    params = {
        "filter[latitude]": lat,
        "filter[longitude]": lon,
        "sort": "distance",
        "page[limit]": 1,
        "include": "routes",
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

    routes_by_id = {}
    for item in data.get("included", []):
        if item.get("type") == "route":
            attrs = item.get("attributes", {})
            route_name = attrs.get("short_name") or attrs.get("long_name")
            routes_by_id[item.get("id")] = route_name

    route_names = []
    for route_ref in stop.get("relationships", {}).get("route", {}).get("data", []):
        route_name = routes_by_id.get(route_ref.get("id"))
        if route_name and route_name not in route_names:
            route_names.append(route_name)

    return {
        "name": stop_name,
        "description": stop_desc,
        "latitude": stop_lat,
        "longitude": stop_lon,
        "distance_km": round(distance_km, 2),
        "routes": route_names,
    }


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/locate", methods=["POST"])
def locate():
    query = request.form.get("place", "").strip()
    if not query:
        return render_template("index.html", error="Please enter a place name or address.")

    try:
        location = geocode_address(query)
    except requests.RequestException:
        return render_template("index.html", error="Unable to contact the geocoding service. Try again later.")

    if not location:
        return render_template("index.html", error="Could not find that location. Try a different address.")

    try:
        stop = find_nearest_mbta(location["latitude"], location["longitude"])
    except requests.RequestException:
        return render_template("index.html", error="Unable to contact the MBTA service. Try again later.")

    if not stop:
        return render_template("index.html", error="No nearby MBTA stops were found.")

    return render_template(
        "result.html",
        query=query,
        user_lat=location["latitude"],
        user_lon=location["longitude"],
        place_name=location["place_name"],
        stop=stop,
        mapbox_token=MAPBOX_TOKEN,
    )


if __name__ == "__main__":
    app.run(debug=True)
