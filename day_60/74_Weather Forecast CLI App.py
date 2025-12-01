"""
Project 74 — Weather Forecast CLI App
Run: python weather_cli.py --city Jaipur --key YOUR_API_KEY
"""

import requests
import argparse

API_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(city, api_key, units="metric"):
    params = {
        "q": city,
        "appid": api_key,
        "units": units
    }

    try:
        response = requests.get(API_URL, params=params, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print("Error fetching weather:", e)
        return None

    return response.json()


def show_weather(data):
    if not data:
        print("No data to show.")
        return

    name = data.get("name")
    main = data.get("main", {})
    wind = data.get("wind", {})
    weather = data.get("weather", [{}])[0]

    print(f"\nWeather Report: {name}")
    print("-" * 40)
    print(f"Temperature: {main.get('temp')} °C")
    print(f"Feels Like: {main.get('feels_like')} °C")
    print(f"Humidity: {main.get('humidity')}%")
    print(f"Condition: {weather.get('description').title()}")
    print(f"Wind Speed: {wind.get('speed')} m/s")
    print("-" * 40)


def parse_args():
    parser = argparse.ArgumentParser(description="Weather Forecast CLI App")
    parser.add_argument("--city", "-c", required=True, help="City name")
    parser.add_argument("--key", "-k", required=True, help="OpenWeather API key")
    return parser.parse_args()


def main():
    args = parse_args()
    data = get_weather(args.city, args.key)
    show_weather(data)


if __name__ == "__main__":
    main()
