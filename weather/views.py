# from django.http import JsonResponse
# import requests


# def get_weather(request):
#     YOUR_ACCESS_KEY = "3582989a79ba60577dfce823e5099df4"  # Replace with your actual key
#     CITY = request.GET.get("city", "Abuja")  # Allows dynamic city input
#     URL = (
#         f"http://api.weatherstack.com/current?access_key={YOUR_ACCESS_KEY}&query={CITY}"
#     )

#     response = requests.get(URL)
#     data = response.json()

#     return JsonResponse(data)

from django.http import JsonResponse
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Weather


class WeatherAPIView(APIView):
    """
    Retrieves current weather data for a specified city and saves it to the database.
    """

    def get(self, request):
        YOUR_ACCESS_KEY = (
            "3582989a79ba60577dfce823e5099df4"  # Replace with your actual key
        )
        CITY = request.GET.get(
            "city", "New York"
        )  # Defaults to New York if no city is provided
        URL = f"http://api.weatherstack.com/current?access_key={YOUR_ACCESS_KEY}&query={CITY}"

        response = requests.get(URL)
        data = response.json()

        if "current" in data:
            weather_info = data["current"]

            # Save to database
            weather_entry, created = Weather.objects.update_or_create(
                city=CITY,
                defaults={
                    "temperature": weather_info["temperature"],
                    "description": weather_info["weather_descriptions"][0],
                    "wind_speed": weather_info["wind_speed"],
                    "humidity": weather_info["humidity"],
                },
            )

            return Response(
                {
                    "city": CITY,
                    "temperature": weather_info["temperature"],
                    "description": weather_info["weather_descriptions"][0],
                    "wind_speed": weather_info["wind_speed"],
                    "humidity": weather_info["humidity"],
                    "message": "Weather data successfully fetched and saved!",
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {"error": "Could not fetch weather data"},
            status=status.HTTP_400_BAD_REQUEST,
        )
