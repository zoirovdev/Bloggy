from django.db import models

from users.models import User

class Essay(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField()
    image = models.ImageField(upload_to='essay_photos/', null=True, blank=True)
    author = models.ForeignKey(User, related_name='essays', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title