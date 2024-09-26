from django.db import models

class AudioModel(models.Model):
    letter = models.CharField(max_length=1)
    audio = models.FileField(upload_to='audio_files/')

    def __str__(self):
        return f"{self.letter}: {self.audio.name}"
