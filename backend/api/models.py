from django.db import models

class Zone(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Device(models.Model):
    name = models.CharField(max_length=100)
    temperature = models.FloatField()
    humidity = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Phase 10: Zones 
    zone = models.ForeignKey(Zone, on_delete=models.SET_NULL, null=True, blank=True, related_name='devices')
    
    # Phase 12: Telegram Alert thresholds
    min_temp = models.FloatField(default=0.0)
    max_temp = models.FloatField(default=50.0)

    def __str__(self):
        return self.name

class DeviceReading(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    temperature = models.FloatField()
    humidity = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.device.name} - {self.timestamp}"