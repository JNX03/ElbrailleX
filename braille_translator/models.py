from django.db import models

class Document(models.Model):
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    braille_text = models.TextField(null=True, blank=True)  # To store the Braille translation