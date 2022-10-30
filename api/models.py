from django.db import models
from PIL import Image
from colorthief import ColorThief


class Photo(models.Model):
    url = models.FilePathField(
        path='C:/Users/Marcel/Programowanie/Zadania_rekrutacyjne/Friendly_Solutions/rest_api/media/'
    )
    title = models.CharField(max_length=64)
    album_id = models.PositiveIntegerField()
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    dominant_color = models.CharField(max_length=7)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Find the and set the size of the image
        photo = Image.open(self.url)
        self.width = photo.width
        self.height = photo.height

        # Find, convert and set the dominant color of the image
        color_thief = ColorThief(self.url)
        dominant_color = color_thief.get_color(quality=1)
        self.dominant_color = '#%02x%02x%02x' % dominant_color

        super().save(*args, **kwargs)
