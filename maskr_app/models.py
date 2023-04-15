from django.db import models

class Images(models.Model):
    image = models.ImageField(upload_to='images/')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
