from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
import pyotp

class CustomUser(AbstractUser):
    require_google_auth = models.BooleanField(default=False)
    google_auth_secret = models.CharField(max_length=16, blank=True, null=True)

    groups = models.ManyToManyField(
        Group,
        related_name="customuser_groups",  # Avoid conflict with Django's default User model
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions",  # Avoid conflict
        blank=True
    )

    def generate_google_secret(self):
        """Generates a new secret key for Google Authenticator."""
        self.google_auth_secret = pyotp.random_base32()
        self.save()

    def verify_google_code(self, code):
        """Verifies the entered OTP code."""
        if not self.google_auth_secret:
            return False
        totp = pyotp.TOTP(self.google_auth_secret)
        return totp.verify(code)



                                # signupmodellllllls
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    country = models.CharField(max_length=100, blank=True, null=True)
