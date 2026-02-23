from django.urls import path

from time_tracker.views import CalendarEntriesView, DaySummaryView, WeekSummaryView

app_name = "time_tracker"

urlpatterns = [
    path("calendar/week-summary/", WeekSummaryView.as_view(), name="calendar-week-summary"),
    path("calendar/day-summary/", DaySummaryView.as_view(), name="calendar-day-summary"),
    path("calendar/entries/", CalendarEntriesView.as_view(), name="calendar-entries"),
]
