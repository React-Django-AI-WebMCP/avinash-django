"""Serializers for calendar APIs. Read-only; per Technical Document §3."""

from rest_framework import serializers

from time_tracker.models import TimeEntry


class WeekSummarySerializer(serializers.Serializer):
    """Response shape for week summary."""

    total_minutes = serializers.IntegerField(min_value=0)
    total_duration = serializers.CharField()  # "HH:MM"


class DaySummarySerializer(serializers.Serializer):
    """Response shape for day summary."""

    total_minutes = serializers.IntegerField(min_value=0)
    total_duration = serializers.CharField()  # "HH:MM"


class CalendarEntrySerializer(serializers.ModelSerializer):
    """Entry for calendar overlay. title, start_time, end_time, duration, entry_type, project_color."""

    duration = serializers.SerializerMethodField()
    project_color = serializers.SerializerMethodField()

    class Meta:
        model = TimeEntry
        fields = [
            "id",
            "title",
            "start_time",
            "end_time",
            "duration",
            "entry_type",
            "project_color",
        ]
        read_only_fields = fields

    def get_duration(self, obj: TimeEntry) -> str:
        """Format as 'HH:MM hrs' per REQUIREMENTS §2.8."""
        from time_tracker.services import minutes_to_hh_mm

        return f"{minutes_to_hh_mm(obj.duration_minutes)} hrs"

    def get_project_color(self, obj: TimeEntry) -> str | None:
        return obj.project.color if obj.project else None
