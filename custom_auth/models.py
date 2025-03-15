from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class AuthModel(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=30)

    def savePassword(self, raw_password):
        self.password = make_password(raw_password)

    def checkPassword(self, raw_password):
        return check_password(raw_password, self.password)