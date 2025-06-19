from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField(default=-9999)
    rating = models.FloatField(default=5.0)
    reviews = models.IntegerField(default=100)

    def __str__(self):
        return f"'{self.title}' by '{self.author}', published on the '{self.publication_year}'"