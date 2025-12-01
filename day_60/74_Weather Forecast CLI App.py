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
