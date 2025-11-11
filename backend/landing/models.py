from django.db import models

# Create your models here.
class MobileRecord(models.Model):
    mobile = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    ip = models.CharField(max_length=50, null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)