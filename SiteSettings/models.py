from django.db import models
from django.utils.safestring import mark_safe
# Create your models here.


class Setting(models.Model):
    siteTitle = models.CharField(max_length=30)
    sitePhone = models.IntegerField()
    siteLogo = models.ImageField(blank=True, upload_to='siteImages/')
    siteEmail = models.EmailField()
    siteAddress = models.CharField(max_length=250)
    siteAbout = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=False)
    contact_page_banner = models.ImageField(
        blank=True, upload_to='siteImages/contact_page_banner')

    def __str__(self):
        return str(self.id)


# class Slider(models.Model):
#     image = models.ImageField(blank=True, upload_to='siteImages/slider')
#     status = models.BooleanField(default=True)
#     title = models.CharField(max_length=150, null=True, blank=True)
#     subtitle = models.CharField(max_length=150, null=True, blank=True)

#     def __str__(self):
#         return self.title

#     def image_tag(self):
#         return mark_safe('<img src="{}" heights ="50" width="40" />'.format(self.image.url))
#     image_tag.short_description = 'Image'
