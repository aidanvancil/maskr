from django.db import models

class saved_images(models.Model):
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    title = models.TextField(max_length=40)
    class Meta:
        pass
