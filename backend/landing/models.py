from django.db import models

# Create your models here.
class MobileRecord(models.Model):
    mobile = models.CharField(max_length=20)

    def __str__(self):
        return self.mobile