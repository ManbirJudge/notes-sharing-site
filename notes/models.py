from django.db import models
from django.contrib.auth.models import User


class UserData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    contact = models.CharField(max_length=10, null=True)
    branch = models.CharField(max_length=30, null=False)
    role = models.CharField(max_length=30, null=False)

    def __str__(self):
        return self.user.username


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    upload_date = models.CharField(max_length=50, null=False)
    branch = models.CharField(max_length=30, null=False)
    subject = models.CharField(max_length=30, null=False)
    file = models.FileField(null=False)
    description = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=10, null=False)

    def __str__(self):
        return f'{self.user.username} - {self.status}'
