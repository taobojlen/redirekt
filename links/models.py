from django.db import models

# Create your models here.
class Link(models.Model):
  short_id = models.CharField(max_length=6)
  created_at = models.DateTimeField(auto_now_add=True)
  destination = models.URLField()

  def __str__(self):
    return "{} ({})".format(self.short_id, self.destination)

  def get_absolute_url(self):
      from django.urls import reverse
      return reverse('link-detail', kwargs={'pk': self.pk})


class Visit(models.Model):
  link = models.ForeignKey(Link, on_delete=models.CASCADE)
  timestamp = models.DateTimeField(auto_now_add=True)
  user_agent = models.CharField(max_length=4000)
  ip = models.CharField(max_length=45)
