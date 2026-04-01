from django.db import models

# Create your models here.
from django.db import models

class Report(models.Model):
    ISSUE_TYPES = [
        ('pothole', 'Pothole'),
        ('water', 'Water'),
        ('electricity', 'Electricity'),
    ]

    issue_type = models.CharField(max_length=50, choices=ISSUE_TYPES)
    description = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.issue_type

PRIORITY_CHOICES = [
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
]

priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='low')
