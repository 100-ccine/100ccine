from django.db import models

class CrollData(models.Model):
    title = models.CharField(max_length=200)
    link = models.CharField(max_length=500)

    def __str__(self):
       return self.title