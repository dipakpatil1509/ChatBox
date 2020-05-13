from django.db import models
from django.contrib.auth import get_user_model
from groups.models import Group
from django.urls import reverse

User = get_user_model()

class Post(models.Model):
    user = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE, unique=False)
    created_at = models.DateTimeField(auto_now=True,unique=False)
    message = models.TextField(blank=False, default="",unique=False)
    message_html = models.TextField(editable=False, unique=False)
    group = models.ForeignKey(Group,related_name="posts", null=True, blank=True,on_delete=models.CASCADE, unique=False)

    def __str__(self):
        return self.message


    def get_absolute_url(self):
        return reverse(
            "groups:group_details",
            kwargs={
                "pk": self.pk
            }
        )

    class Meta:
        ordering = ["created_at"]


