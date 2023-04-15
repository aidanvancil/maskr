from django.db import models

class Images(models.Model):
    image_file = models.ImageField(upload_to='images/')
    name = models.CharField(max_length=255)
    class Meta:
        pass
