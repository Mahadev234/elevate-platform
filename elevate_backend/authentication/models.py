from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # Basic Info
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True)
    profile_picture = models.ImageField(upload_to="profile_pictures/", blank=True)
    bio = models.TextField(blank=True)

    # Role and Status
    ROLE_CHOICES = [
        ("ADMIN", "Admin"),
        ("EMPLOYEE", "Employee"),
        ("CLIENT", "Client"),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="EMPLOYEE")
    is_2fa_enabled = models.BooleanField(default=False)

    # Professional Info
    company_name = models.CharField(max_length=100, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    skills = models.JSONField(default=list, blank=True)
    hourly_rate = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    # Preferences
    timezone = models.CharField(max_length=50, blank=True)
    language = models.CharField(max_length=10, default="en")
    notification_preferences = models.JSONField(default=dict, blank=True)

    # Social Links
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    portfolio_url = models.URLField(blank=True)

    # Required fields
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name", "role"]
