import sys
from datetime import datetime

import requests

URL = "https://api.open-meteo.com/v1/forecast"
OUT_FILE = "weather_log.txt"
WAIT = 8
CITY_LAT = 18.5204
CITY_LON = 73.8567

CONDITIONS = {
    0: "Clear sky",
    1: "Mostly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    51: "Light drizzle",
    61: "Rain",
    80: "Rain showers",
    95: "Thunderstorm",
}


def read_location():
    if len(sys.argv) == 3:
        try:
            return float(sys.argv[1]), float(sys.argv[2])
        except ValueError:
            print("Those coordinates are not numbers, using the default city.")
    return CITY_LAT, CITY_LON


def get_data(lat, lon):
    query = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": "true",
        "timezone": "auto",
    }
    try:
        reply = requests.get(URL, params=query, timeout=WAIT)
        if reply.status_code != 200:
            print("Server answered with status", reply.status_code)
            return None
        return reply.json()
    except requests.exceptions.Timeout:
        print("The request timed out.")
    except requests.exceptions.ConnectionError:
        print("Could not connect. Check your internet.")
    except requests.exceptions.RequestException as err:
        print("Request failed:", err)
    except ValueError:
        print("Reply was not valid JSON.")
    return None


def pick_fields(data):
    try:
        now = data["current_weather"]
        return {
            "temp": now["temperature"],
            "wind": now["windspeed"],
            "code": now["weathercode"],
            "zone": data["timezone"],
        }
    except (KeyError, TypeError):
        print("Some expected fields were missing from the reply.")
        return None


def make_text(info, lat, lon):
    stamp = datetime.now().strftime("%d-%m-%Y %H:%M")
    label = CONDITIONS.get(info["code"], "Unknown")
    rows = [
        "-" * 38,
        "Checked at  : " + stamp,
        "Position    : {:.4f}, {:.4f}".format(lat, lon),
        "Time zone   : " + info["zone"],
        "Temperature : {} C".format(info["temp"]),
        "Wind        : {} km/h".format(info["wind"]),
        "Condition   : {} ({})".format(label, info["code"]),
        "",
    ]
    return "\n".join(rows)


def append_to_file(text):
    try:
        with open(OUT_FILE, "a", encoding="utf-8") as f:
            f.write(text + "\n")
        return True
    except OSError as err:
        print("Could not save the log:", err)
        return False


def main():
    lat, lon = read_location()
    data = get_data(lat, lon)
    if data is None:
        return
    info = pick_fields(data)
    if info is None:
        return
    text = make_text(info, lat, lon)
    print(text)
    if append_to_file(text):
        print("Saved to", OUT_FILE)


if __name__ == "__main__":
    main()
