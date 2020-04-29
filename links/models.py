from django.db import models

# Create your models here.
class Link(models.Model):
  destination = models.URLField()
  short_id = models.CharField(max_length=6)

class Visit(models.Model):
  link = models.ForeignKey(Link, on_delete=models.CASCADE)
  timestamp = models.DateTimeField(auto_now_add=True)
  user_agent = models.CharField(max_length=4000)
  ip = models.CharField(max_length=45)
