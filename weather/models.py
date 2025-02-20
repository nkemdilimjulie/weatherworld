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
