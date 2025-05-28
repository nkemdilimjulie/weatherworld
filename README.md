# `Very Important`

**To find weather situation of any city, add** **`?city=CityName`** to my weather domain: http://127.0.0.1:8000/weather/
 ### Example:
 > **`http://127.0.0.1:8000/weather/?city=Abuja`**





**Start**

 With my API Key , I surf current weather info from http://api.weatherstack.com/ successfully.
 I got weatherstack website from GitHub public APIs: https://github.com/public-apis/public-apis/?tab=readme-ov-file

 first-time views.py:
 + - enables me to surf weather info directly from the provider
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

 Modify **`views.py`** to Save and Fetch Weather Data

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
        YOUR_ACCESS_KEY = (
            "xxx"  # Replace with your actual key
        )
        CITY = request.GET.get(
            "city", "New York"
        )  # Defaults to New York if no city is provided
        URL = f"http://api.weatherstack.com/current?access_key={YOUR_ACCESS_KEY}&query={CITY}"

        response = requests.get(URL)
        data = response.json()

        if "current" in data and "location" in data:
            weather_info = data["current"]
            location_info = data["location"]

            # Save or update in the database
            weather_entry, created = Weather.objects.update_or_create(
                city=CITY,
                defaults={
                    "country": location_info["country"],
                    "temperature": weather_info["temperature"],
                    "feelslike": weather_info["feelslike"],
                    "description": weather_info["weather_descriptions"][0],
                    "wind_speed": weather_info["wind_speed"],
                    "humidity": weather_info["humidity"],
                    "is_day": weather_info["is_day"],
                    "localtime": location_info["localtime"],
                },
            )

            return Response(
                {
                    "city": CITY,
                    "country": location_info["country"],
                    "temperature": weather_info["temperature"],
                    "feelslike": weather_info["feelslike"],
                    "description": weather_info["weather_descriptions"][0],
                    "wind_speed": weather_info["wind_speed"],
                    "humidity": weather_info["humidity"],
                    "is_day": weather_info["is_day"],
                    "localtime": location_info["localtime"],
                    "last_updated": weather_entry.last_updated,
                    "message": "Weather data successfully fetched and saved!",
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {"error": "Could not fetch weather data"},
            status=status.HTTP_400_BAD_REQUEST,
        )


 ```
**`Explanation:`**

📌 Changes & Features:

+ Fetches weather data from the external API.
+ Saves it into my local database (updates existing records).
+ Returns JSON response with weather info.
+ Allows users to specify a city dynamically using **`?city=London`**.


**Why Use a Class-Based View (CBV)?**

✅ Better Structure: Keeps related methods inside a single class.

✅ Extensibility: You can easily add methods like post, put, or delete.

✅ DRF Integration: Works well with Django REST framework for building APIs.



models.py

```
from django.db import models


class Weather(models.Model):
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default="Unknown")  # Default value)
    temperature = models.FloatField()
    feelslike = models.FloatField(blank=True, null=True)
    description = models.CharField(max_length=255)
    wind_speed = models.FloatField()
    humidity = models.IntegerField()
    is_day = models.CharField(max_length=10, blank=True, null=True)
    localtime = models.DateTimeField(auto_now_add=True, blank=True, null=True)  # Set only when created
    last_updated = models.DateTimeField(auto_now=True, blank=True, null=True)  # Updates on save

    def __str__(self):
        # Format last_updated to display only date and time without seconds
        last_updated = (self.last_updated.strftime("%Y-%m-%d %H:%M") if self.last_updated else "N/A")
        return f"{self.city} - {self.temperature}°C | Last Updated: {last_updated} | Local Time: {self.localtime}"

```


📌 Explanation:

+ **city**: Name of the city.
+ **temperature**: Stores the current temperature.
+ **description**: Weather description (e.g., "Cloudy").
+ **wind_speed**: Wind speed.
+ **humidity**: Percentage humidity.
+ **last_update**d: Timestamp when the weather data was last updated.
+ `other fields` are self-explanatory


`**Enable Django know of the changes in database structure**`

```
python manage.py makemigrations
python manage.py migrate
```

`**Test Your API**`


```
python manage.py runserver
```

 
 
 ## Run pip freeze > requirements.txt after all installations

 
 📌 Best Practice:
After you’ve installed all the required packages in your virtual environment (.weathervenv), then run:

```
pip freeze > requirements.txt
```
This captures the complete and final list of packages used in your project — including versions — so anyone can reproduce your environment.

🔄 **When to re-run pip freeze:**
You should update your requirements.txt anytime you:

+ Install a new package (pip install django, djangorestframework, etc.)

+ Upgrade a package

+ Remove a package