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
