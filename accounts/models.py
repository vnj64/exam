from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    STATUS_CHOICE = (
        ('BR', 'bronze'),
        ('SL', 'silver'),
        ('GO', 'gold'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.PositiveIntegerField(null=True, blank=True, default=0)
    status = models.CharField(max_length=50, choices=STATUS_CHOICE, default='bronze')

    def __str__(self):
        return f'Profile - {self.user.username}'


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction = models.PositiveIntegerField(null=True, blank=True, default=0)
    created_at = models.DateTimeField(auto_created=True, auto_now=True)

    def __str__(self):
        return f'Transaction - {self.user.username} - {self.transaction}'
