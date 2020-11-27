from django.db import models
from accounts.models import User
from ckeditor.fields import RichTextField
# Create your models here.


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000, null=True, blank=True)
    image = models.ImageField(
        default='blog-default.jpg', upload_to='blog_pics')
    description = RichTextField(blank=True, null=True)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)
