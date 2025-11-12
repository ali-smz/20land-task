from django.db import models


class MobileRecord(models.Model):
    """
    Model to store mobile numbers submitted by users.
    Each mobile number is unique to prevent duplicates.
    """
    mobile = models.CharField(max_length=20, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Mobile Record"
        verbose_name_plural = "Mobile Records"
        ordering = ["-created_at"]

    def __str__(self):
        return self.mobile