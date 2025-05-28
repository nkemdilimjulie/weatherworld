import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .models import Weather
from decouple import config


class WeatherAPIView(APIView):
    """
    Retrieves current weather data for a specified city and saves it to the database.
    """

    def get(self, request):
        YOUR_ACCESS_KEY = config('WEATHER_API_KEY')
        CITY = request.GET.get("city", "New York")  # Defaults to New York if no city is provided
        URL = f"http://api.weatherstack.com/current?access_key={YOUR_ACCESS_KEY}&query={CITY}"

        response = requests.get(URL)
        data = response.json()

        if "current" in data and "location" in data:
            weather_info = data["current"]
            location_info = data["location"]

            # 🔹 Save or update the database entry
            weather_entry, created = Weather.objects.update_or_create(
                city=CITY,
                defaults={
                    "country": location_info.get("country", "Unknown"),
                    "temperature": weather_info.get("temperature", 0),
                    "feelslike": weather_info.get("feelslike", 0),
                    "description": weather_info["weather_descriptions"][0] if weather_info.get("weather_descriptions") else "N/A",
                    "wind_speed": weather_info.get("wind_speed", 0),
                    "humidity": weather_info.get("humidity", 0),
                    "is_day": weather_info.get("is_day", "Unknown"),
                    "localtime": location_info.get("localtime", None),
                },
            )

            return Response(
                {
                    "city": CITY,
                    "country": location_info["country"],
                    "temperature": weather_info["temperature"],
                    "feelslike": weather_info["feelslike"],
                    "description": weather_info["weather_descriptions"][0] if weather_info.get("weather_descriptions") else "N/A",
                    "wind_speed": weather_info["wind_speed"],
                    "humidity": weather_info["humidity"],
                    "is_day": weather_info["is_day"],
                    "localtime": location_info["localtime"],
                    "last_updated": weather_entry.last_updated,
                    "message": "Weather data successfully fetched and saved!",
                },
                status=status.HTTP_200_OK,
            )

        return Response({"error": "Could not fetch weather data"}, status=status.HTTP_400_BAD_REQUEST)
