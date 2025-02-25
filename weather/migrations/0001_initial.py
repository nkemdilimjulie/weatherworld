# Generated by Django 4.2.19 on 2025-02-20 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Weather',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=100)),
                ('temperature', models.FloatField()),
                ('description', models.CharField(max_length=255)),
                ('wind_speed', models.FloatField()),
                ('humidity', models.IntegerField()),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
