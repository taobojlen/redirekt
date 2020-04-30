from django.db import models

# Create your models here.
class Link(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    short_id = models.CharField(max_length=6)
    destination = models.URLField()

    def __str__(self):
        return "{} ({})".format(self.short_id, self.destination)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("link-detail", kwargs={"pk": self.pk})

    def get_redirect_url(self):
        from django.urls import reverse
        return reverse('redirect', kwargs={'short_id': self.short_id})


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    link = models.ForeignKey(Link, on_delete=models.CASCADE)
    user_agent = models.CharField(max_length=4000)
    ip = models.CharField(max_length=45)
