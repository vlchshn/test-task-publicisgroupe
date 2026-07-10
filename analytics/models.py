from django.db import models
from django.contrib.auth.models import User


class FileUploadLog(models.Model):
    STATUS_CHOICES = (
        ("SUCCESS", "Success"),
        ("FAILED", "Failed"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="upload_logs")
    file_name = models.CharField(max_length=255)
    upload_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    error_type = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.file_name} - {self.status}"


class FactData(models.Model):
    upload_log = models.ForeignKey(
        FileUploadLog, on_delete=models.CASCADE, related_name="fact_data"
    )
    advertiser = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    ad_format = models.CharField(max_length=100)
    platform = models.CharField(max_length=100)
    impressions = models.BigIntegerField()

    def __str__(self):
        return f"{self.advertiser} - {self.brand}"
