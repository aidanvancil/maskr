from django.contrib import admin
from .models import Images

class ImagesAdmin(admin.ModelAdmin):
    pass

admin.site.register(Images, ImagesAdmin)
