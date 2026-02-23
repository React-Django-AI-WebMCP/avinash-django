from django.conf import settings
from django.db import models

from core.models import BaseModel


class Project(BaseModel):
    """Minimal project for calendar entry display (name + color)."""

    name = models.CharField(max_length=255)
    color = models.CharField(max_length=7, default="#6b7280")  # hex, e.g. #6b7280

    class Meta:
        db_table = "time_tracker_project"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class TimeEntry(BaseModel):
    """Calendar time entry per user. Per Technical Document §4 (US-1)."""

    class EntryType(models.TextChoices):
        LOGGED = "logged", "Logged"
        MENTIONED = "mentioned", "Mentioned"
        INTEGRATED = "integrated", "Integrated"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="time_entries",
        db_index=True,
    )
    date = models.DateField(db_index=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    title = models.CharField(max_length=255)
    entry_type = models.CharField(
        max_length=20,
        choices=EntryType.choices,
        default=EntryType.LOGGED,
        db_index=True,
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="time_entries",
    )

    class Meta:
        db_table = "time_tracker_time_entry"
        ordering = ["date", "start_time"]
        indexes = [
            models.Index(fields=["user", "date"]),
        ]

    def __str__(self) -> str:
        return f"{self.title} ({self.date})"

    @property
    def duration_minutes(self) -> int:
        """Duration in minutes (for aggregation). Assumes same-day start/end."""
        from datetime import datetime

        start = datetime.combine(self.date, self.start_time)
        end = datetime.combine(self.date, self.end_time)
        delta = end - start
        return int(delta.total_seconds() / 60)
