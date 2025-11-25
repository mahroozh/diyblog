from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()

class Blogger(models.Model):
    # If you want authors separate from User, use OneToOneField to User.
    # I'll model a Blogger that optionally links to a User account.
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Blogger, on_delete=models.SET_NULL, null=True, related_name='posts')
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        ordering = ['-created_at']  # newest first

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        ordering = ['created_at']  # oldest -> newest

    def __str__(self):
        # truncated to 75 chars per requirement
        t = (self.text[:72] + '...') if len(self.text) > 75 else self.text
        return t

@receiver(post_save, sender=User)
def create_blogger_for_new_user(sender, instance, created, **kwargs):
    if created:
        Blogger.objects.create(user=instance, name=instance.username)