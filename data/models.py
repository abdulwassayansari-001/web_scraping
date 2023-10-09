from django.db import models


class DataScrap(models.Model):
    name = models.CharField(max_length=255, null=True)
    dep = models.CharField(max_length=255, blank=True, null=True)
    designation = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    link = models.CharField(max_length=255, blank=True, null=True)
    hierarchy = models.CharField(max_length=255, blank=True, null=True)
    validation = models.BooleanField(default=False, null=True)

class CSVFiles(models.Model):
    file_name = models.CharField(max_length=255, null=True)

class DataScrapImages(models.Model):
    image = models.ImageField(upload_to='images/')