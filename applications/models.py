from django.conf import settings
from django.db import models


class Application(models.Model):
    class Status(models.TextChoices):
        WISHLIST = "wishlist", "Wishlist"
        APPLIED = "applied", "Applied"
        INTERVIEWING = "interviewing", "Interviewing"
        OFFER = "offer", "Offer"
        REJECTED = "rejected", "Rejected"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="applications",
    )
    company = models.CharField(max_length=200)
    job_title = models.CharField(max_length=200)
    job_url = models.URLField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.APPLIED,
        db_index=True,
    )
    location = models.CharField(max_length=200, blank=True)
    applied_on = models.DateField(null=True, blank=True)
    follow_up_on = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.job_title} at {self.company}"