from django.db import models

class Image(models.Model):
    p_hash = models.CharField(max_length=50)
    md5_hash = models.CharField(max_length=50)
    link = models.CharField(max_length=500, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.link) if self.link else f"Image {self.id}"