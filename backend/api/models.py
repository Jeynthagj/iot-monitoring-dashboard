from django.db import models

class Device(models.Model):
    name = models.CharField(max_length=100)
    temperature = models.FloatField()
    humidity = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name