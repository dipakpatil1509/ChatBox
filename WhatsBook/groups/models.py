from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.utils.text import slugify


user = get_user_model()

class Group(models.Model):
    owner = models.CharField(max_length=256,unique=False, default='')
    name = models.CharField(max_length=256, unique=False)
    slug = models.SlugField(allow_unicode=True, unique=False)
    description = models.TextField(blank=True, default='')
    dp = models.ImageField(default='gallery/unnamed.png', upload_to ='gallery')
    members = models.ManyToManyField(User, through='GroupMember')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('groups:group_details', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['name']


class GroupMember(models.Model):
    groups = models.ForeignKey(Group ,related_name='membership', on_delete=models.CASCADE)
    user = models.ForeignKey(user, related_name='users', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ('groups','user')