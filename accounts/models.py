from django.contrib.auth.models import AbstractUser
from django.db import models
from accounts.managers import UserManager
from PIL import Image
from django.db.models.signals import post_save
from django.dispatch import receiver


GENDER_CHOICES = (
    ('male', 'Male'),
    ('female', 'Female'))


class User(AbstractUser):
    username = None
    role = models.CharField(max_length=12, error_messages={
        'required': "Role must be provided"
    })
    gender = models.CharField(max_length=10, blank=True, null=True, default="")
    email = models.EmailField(unique=True, blank=False,
                              error_messages={
                                  'unique': "A user with that email already exists.",
                              })

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    objects = UserManager()


class UserProfileManager(models.Manager):

    def profile_update(self, image):
        profile_update_obj = self.model(image=image)


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    image = models.ImageField(blank=True, null=True,
                              default='avatar.png', upload_to='profile_pics')
    cover_img = models.ImageField(
        blank=True, null=True, default='cover.png', upload_to='cover_pics')
    about = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f'{self.user.email}'

    def save(self, *args, **kwargs):
        super(UserProfile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)
        # cover_img = Image.open(self.cover_img.path)

        if img.height > 200 or img.width > 200:
            output_size = (200, 200)
            img.thumbnail(output_size)
            img.save(self.image.path)

        # if cover_img.height > 400 or cover_img.width > 600 or cover_img.height < 400 or cover_img.width < 600:
        #     output_size = (960, 400)
        #     cover_img.thumbnail(output_size)
        #     cover_img.save(self.cover_img.path)

    objects = UserProfileManager()

# signal.py


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        post_save.connect(create_profile, sender=User)


class CV(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField()
    description = models.TextField()
    updated = models.DateField(auto_now=True)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.name)
