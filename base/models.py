from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.utils.text import slugify
import random
import string
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class UserProfile(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    bio = models.TextField(null=True, blank=True)

    pfp = models.ImageField(upload_to='images/',
                            default='/images/guest.webp')
    pfp_crop = ImageSpecField(source='pfp', processors=[
                              ResizeToFill(64, 64)], format='PNG', options={'quality': 60})

    def __str__(self):
        return self.email


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, unique=True)
    participants = models.ManyToManyField(
        User, related_name='participants', blank=True)
    description = models.TextField(blank=True, null=True)
    private = models.BooleanField(default=False)

    invite_code = models.CharField(unique=True, max_length=6)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)  # Add a SlugField

    def save(self, *args, **kwargs):
        # Generate a unique invite code
        if not self.invite_code:
            unique_code = self.generate_unique_invite_code()
            self.invite_code = unique_code

        # Generate and set the slug based on the name field
        if not self.slug:
            self.slug = slugify(self.name)

        super(Room, self).save(*args, **kwargs)

    def generate_unique_invite_code(self):
        # Generate a unique invite code
        while True:
            invite_code = ''.join(random.choice(
                string.ascii_letters + string.digits) for _ in range(6))
            if not Room.objects.filter(invite_code=invite_code).exists():
                return invite_code

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    body = models.TextField()
    edited = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.body)[0:50]
