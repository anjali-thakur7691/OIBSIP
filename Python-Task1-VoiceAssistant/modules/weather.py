"""
===========================================
        Weather Module
===========================================
Author      : Anjali Thakur
Project     : AI Voice Assistant
Internship  : OASIS INFOBYTE
===========================================
"""

import requests

from config import WEATHER_API_KEY, CITY


def get_weather():
    """
    Fetch current weather information.
    """

    if not WEATHER_API_KEY:
        return "Weather API Key is not configured."

    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?q={CITY}"
        f"&appid={WEATHER_API_KEY}"
        "&units=metric"
    )

    try:

        response = requests.get(url, timeout=10)

        response.raise_for_status()

        data = response.json()

        city = data["name"]

        country = data["sys"]["country"]

        temperature = data["main"]["temp"]

        feels_like = data["main"]["feels_like"]

        humidity = data["main"]["humidity"]

        description = data["weather"][0]["description"].title()

        return (
            f"Current weather in {city}, {country}. "
            f"Temperature is {temperature}°C. "
            f"Feels like {feels_like}°C. "
            f"Humidity is {humidity} percent. "
            f"Condition: {description}."
        )

    except requests.exceptions.Timeout:

        return "Weather server is taking too long to respond."

    except requests.exceptions.ConnectionError:

        return "No internet connection."

    except requests.exceptions.HTTPError:

        return "Invalid Weather API Key or City Name."

    except Exception as e:

        return f"Weather Error: {e}"