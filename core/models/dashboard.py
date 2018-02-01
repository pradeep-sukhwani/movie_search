from django.contrib.auth.models import User
from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=512)


class MovieDetail(models.Model):
    name = models.CharField(max_length=512)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    score = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
    director = models.CharField(max_length=512, null=True, blank=True)
    popularity = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    genre = models.ManyToManyField(Genre, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
