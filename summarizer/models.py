from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Summary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original_link = models.TextField()
    body = models.TextField()
    sentiment_classification = models.CharField(max_length=20, blank=True, null=True)
    sentiment_polarity = models.FloatField(blank=True, null=True)
    sentiment_subjectivity = models.FloatField(blank=True, null=True)
    sentiment_plot = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.original_link
    
# summarizer/models.py

from django.db import models

class MyModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

