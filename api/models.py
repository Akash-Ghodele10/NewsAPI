from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User

class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

class NewsArticle(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    url = models.URLField()
    date_published = models.DateTimeField()
    search_history = models.ForeignKey(SearchHistory, on_delete=models.CASCADE)
