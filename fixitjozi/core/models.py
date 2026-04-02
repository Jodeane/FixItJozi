from django.db import models


class Report(models.Model):
    ISSUE_TYPES = [
        ('electricity', 'Electricity'),
        ('gas', 'Gas'),
        ('parks', 'Parks'),
        ('roads', 'Roads'),
        ('traffic', 'Traffic Lights'),
        ('transport', 'Transport'),
        ('waste', 'Waste & Refuse'),
        ('water', 'Water & Sanitation'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    # Claude AI improvement: added reference_number so users can track their own report.
    # Previously the Track page showed a single hardcoded report (JHB12345) for all users,
    # failing the HCI utility goal entirely. Now each report gets a unique reference number
    # that is shown to the user after submission and can be looked up on the Track page.
    STATUS_CHOICES = [
        ('logged', 'Logged'),
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]

    issue_type = models.CharField(max_length=50, choices=ISSUE_TYPES)
    description = models.TextField()
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='low')
    reference_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='logged')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.reference_number or 'No ref'} — {self.issue_type}"