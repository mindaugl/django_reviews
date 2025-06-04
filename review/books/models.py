from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_date = models.DateField()
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f"'{self.title}' by '{self.author}', published on the '{self.publication_date}'"