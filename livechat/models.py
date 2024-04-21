from django.db import models

class ChatMessage(models.Model):
    message = models.TextField()
    username = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username}: {self.message}"