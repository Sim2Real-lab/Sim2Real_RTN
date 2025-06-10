# landing_page/models.py

from django.db import models

class Sponsor(models.Model):
    """
    Represents a sponsor of the Sim2Real Robotics Competition.
    """
    TIER_CHOICES = [
        ('Gold', 'Gold'),
        ('Platinum', 'Platinum'),
        ('Silver', 'Silver'),
        ('Bronze', 'Bronze'), # Added a Bronze tier as an example
    ]

    name = models.CharField(max_length=200, help_text="Name of the sponsoring organization.")
    tier = models.CharField(
        max_length=10,
        choices=TIER_CHOICES,
        default='Bronze',
        help_text="Sponsorship tier (e.g., Gold, Platinum, Silver)."
    )
    # Add other fields like contact_person, amount, benefits if needed
    # e.g., amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Sponsors"
        # Ordering ensures Platinum sponsors appear first, then Gold, etc.
        # You might need to adjust this based on how you want to sort.
        ordering = ['tier'] # This will sort alphabetically, consider a custom sort if needed

    def __str__(self):
        return f"{self.name} ({self.tier} Sponsor)"

class Query(models.Model):
    """
    Stores contact form submissions (queries) from potential sponsors.
    This model remains unchanged, intended for sponsor-related inquiries.
    """
    name = models.CharField(max_length=100, help_text="Name of the person submitting the query.")
    organisation = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Name of the organization (optional)."
    )
    contact_email = models.EmailField(max_length=254, help_text="Email address for contact.")
    mobile_number = models.TextField(max_length=10,help_text="Mobile number for contact.")
    message = models.TextField(help_text="The query or message submitted.")
    submitted_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp of when the query was submitted.")

    class Meta:
        verbose_name_plural = "Queries"
        ordering = ['-submitted_at'] # Order by most recent queries first

    def __str__(self):
        return f"Query from {self.name} ({self.contact_email})"

class GeneralQuery(models.Model):
    """
    Stores general contact form submissions from regular visitors.
    """
    name = models.CharField(max_length=100, help_text="Name of the person submitting the query.")
    contact_email = models.EmailField(max_length=254, help_text="Email address for contact.")
    institution_name = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Name of the institution (optional)."
    )
    message = models.TextField(help_text="The general query or message submitted.")
    submitted_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp of when the query was submitted.")

    class Meta:
        verbose_name_plural = "General Queries"
        ordering = ['-submitted_at'] # Order by most recent queries first

    def __str__(self):
        return f"General Query from {self.name} ({self.contact_email})"
