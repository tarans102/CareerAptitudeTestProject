from django.contrib import admin

from . import models

# Register your models here.
admin.site.register(models.Question)
admin.site.register(models.Choice)
admin.site.register(models.CareerOption)
admin.site.register(models.Response)
