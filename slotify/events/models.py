from django.db import models
from groups.models import Group
from django.db.models import F, Q

from common.constants import EVENT_MAX_TITLE_LENGTH, EVENT_MAX_LOCATION_LENGTH

# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length=EVENT_MAX_TITLE_LENGTH)
    description = models.TextField(blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()
    location = models.CharField(max_length=EVENT_MAX_LOCATION_LENGTH)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(start_date_time__lt=F("end_date_time")),
                name="start_date_time_lt_end_date_time",
            )
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.group} | {self.title} | {self.start_date_time} - {self.end_date_time}"