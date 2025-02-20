# from django.urls import path
# from .views import get_weather

# urlpatterns = [
#     path("weather/", get_weather, name="get-weather"),

# ]

from django.urls import path
from .views import WeatherAPIView

urlpatterns = [
    path("weather/", WeatherAPIView.as_view(), name="get-weather"),
]
