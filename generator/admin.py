from django.contrib import admin
from .models import DataSchema, Column

# Register your models here.
admin.site.register(Column)
admin.site.register(DataSchema)
