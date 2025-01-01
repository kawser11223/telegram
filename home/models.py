from django.db import models

class User(models.Model):
    chat_id = models.CharField(max_length=50, unique=True)
    username = models.CharField(max_length=100)
    signup_date = models.DateTimeField(auto_now_add=True)
    welcome_sent = models.BooleanField(default=False)  # New field to track message status

    def __str__(self):
        return self.username
