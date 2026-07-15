import json
import os
import urllib.parse
import urllib.request

CLIENT_ID = os.environ["STRAVA_CLIENT_ID"]
CLIENT_SECRET = os.environ["STRAVA_CLIENT_SECRET"]
REFRESH_TOKEN = os.environ["STRAVA_REFRESH_TOKEN"]


def post(url, data):
    body = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(url, data=body, method="POST")
    with urllib.request.urlopen(req) as resp:
        return json.load(resp)


def get(url, token):
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req) as resp:
        return json.load(resp)


token_data = post(
    "https://www.strava.com/oauth/token",
    {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN,
    },
)
access_token = token_data["access_token"]

activities = get(
    "https://www.strava.com/api/v3/athlete/activities?per_page=1", access_token
)
activity = activities[0] if activities else {}

out = {
    "name": activity.get("name"),
    "type": activity.get("type"),
    "distance_m": activity.get("distance"),
    "moving_time_s": activity.get("moving_time"),
    "total_elevation_gain_m": activity.get("total_elevation_gain"),
    "start_date": activity.get("start_date_local"),
    "id": activity.get("id"),
    "map_polyline": (activity.get("map") or {}).get("summary_polyline"),
}

with open("strava-latest.json", "w") as f:
    json.dump(out, f, indent=2)
    f.write("\n")
