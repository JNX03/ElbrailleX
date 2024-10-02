from django.db import models

class FileUpload(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='uploads/')  # Files will be uploaded to EbrailleAssets/uploads/
    uploaded_at = models.DateTimeField(auto_now_add=True)
