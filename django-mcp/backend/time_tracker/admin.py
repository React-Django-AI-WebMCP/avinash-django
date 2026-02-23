from django.contrib import admin
from time_tracker.models import Project, TimeEntry


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "color")
    search_fields = ("name",)


@admin.register(TimeEntry)
class TimeEntryAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "date", "start_time", "end_time", "entry_type", "project")
    list_filter = ("entry_type", "date")
    search_fields = ("title",)
    raw_id_fields = ("user", "project")
    date_hierarchy = "date"
