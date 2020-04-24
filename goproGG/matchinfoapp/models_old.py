from django.db import models

# Create your models here.
class Summoner(models.Model):
    name = models.CharField(max_length=255)

    #show the actual summoner name on the dashboard
    def _str_(self):
        return self.name