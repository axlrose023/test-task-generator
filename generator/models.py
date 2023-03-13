from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User
import datetime


class DataSchema(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    column_separator = models.CharField(max_length=200)
    string_character = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Column(models.Model):
    schema = models.ForeignKey(DataSchema, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    data_type = models.CharField(max_length=255)
    order = models.IntegerField(null=True, blank=True)
    extra_args = models.CharField(max_length=255, blank=True, null=True)
    range_min = models.IntegerField(null=True, blank=True)
    range_max = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class CsvFile(models.Model):
    file = models.FileField(upload_to='media/')
