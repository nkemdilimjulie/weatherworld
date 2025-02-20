**Start**

 With my API Key , I surf current weather info from http://api.weatherstack.com/ successfully.
 I got weatherstack website from GitHub public APIs: https://github.com/public-apis/public-apis/?tab=readme-ov-file

 views.py:
 ```
 from django.http import JsonResponse
import requests


def get_weather(request):
    YOUR_ACCESS_KEY = "3582989a79ba60577dfce823e5099df4"  # Replace with your actual key
    CITY = request.GET.get("city", "Abuja")  # Allows dynamic city input
    URL = (
        f"http://api.weatherstack.com/current?access_key={YOUR_ACCESS_KEY}&query={CITY}"
    )

    response = requests.get(URL)
    data = response.json()

    return JsonResponse(data)
```

 ## **Transfer this to my project's database:**

 Modify views.py to Save and Fetch Weather Data

 ```
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
        YOUR_ACCESS_KEY = "3582989a79ba60577dfce823e5099df4"  # Replace with your actual key
        CITY = request.GET.get("city", "New York")  # Defaults to New York if no city is provided
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

            return Response({
                "city": CITY,
                "temperature": weather_info["temperature"],
                "description": weather_info["weather_descriptions"][0],
                "wind_speed": weather_info["wind_speed"],
                "humidity": weather_info["humidity"],
                "message": "Weather data successfully fetched and saved!",
            }, status=status.HTTP_200_OK)

        return Response({"error": "Could not fetch weather data"}, status=status.HTTP_400_BAD_REQUEST)

 ```
**`Explanation:`**

📌 Changes & Features:

+ Fetches weather data from the API.
+ Saves it into the database (updates existing records).
+ Returns JSON response with weather info.
+ Allows users to specify a city dynamically using ?city=London.
**Why Use a Class-Based View (CBV)?**

✅ Better Structure: Keeps related methods inside a single class.

✅ Extensibility: You can easily add methods like post, put, or delete.

✅ DRF Integration: Works well with Django REST framework for building APIs.



models.py

```
from django.db import models

class Weather(models.Model):
    city = models.CharField(max_length=100)
    temperature = models.FloatField()
    description = models.CharField(max_length=255)
    wind_speed = models.FloatField()
    humidity = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.city} - {self.temperature}°C"

```


📌 Explanation:

+ **city**: Name of the city.
+ **temperature**: Stores the current temperature.
+ **description**: Weather description (e.g., "Cloudy").
+ **wind_speed**: Wind speed.
+ **humidity**: Percentage humidity.
+ **last_update**d: Timestamp when the weather data was last updated.


`**Enable Django know of the changes in database structure**`

```
python manage.py makemigrations
python manage.py migrate
```

`**Test Your API**`


```
python manage.py runserver
```

 
 
 
 
 