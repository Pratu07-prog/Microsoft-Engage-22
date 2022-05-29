from django.db import models


class movies(models.Model):
    Title = models.CharField(("Title"), max_length=300)
    Genres = models.TextField(("Genres"))
    Actor = models.TextField(("Actor"))
    Actress = models.TextField(("Actress"))
    Rating_average = models.FloatField(("Rating_average"))
    Rating_Count = models.BigIntegerField(("Rating_Count"))
    Production_companies = models.TextField(("Production_companies"))
    img = models.TextField(max_length=300)
    url = models.URLField(max_length=300)

