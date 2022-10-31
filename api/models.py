from django.db import models
from django.conf import settings
from PIL import Image
from colorthief import ColorThief


class Photo(models.Model):
    # not unique because I had a problem downloading photos from external API (403 always), so I set all the URLs
    # using a mock URL linking to the same photo
    url = models.FilePathField(path=settings.PHOTOS_DIR)
    title = models.CharField(max_length=256)
    album_id = models.PositiveIntegerField()
    width = models.PositiveIntegerField(blank=True)
    height = models.PositiveIntegerField(blank=True)
    color = models.CharField(max_length=7, blank=True)

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
        self.color = '#%02x%02x%02x' % dominant_color

        super().save(*args, **kwargs)
