"""Calendar API views. Per Technical Document §3; auth + filter by request.user."""

from datetime import datetime
from typing import Any

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request

from core.responses import error_response, success_response
from time_tracker.models import TimeEntry
from time_tracker.serializers import CalendarEntrySerializer
from time_tracker.services import minutes_to_hh_mm, week_range_for_date


def _parse_date(date_str: str | None) -> datetime | None:
    """Parse YYYY-MM-DD; return date as datetime at midnight or None if invalid."""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str.strip(), "%Y-%m-%d")
    except ValueError:
        return None


class WeekSummaryView(APIView):
    """GET /api/time-tracking/calendar/week-summary/?date=YYYY-MM-DD"""

    def get(self, request: Request) -> Any:
        date_param = request.query_params.get("date")
        d = _parse_date(date_param)
        if d is None:
            return error_response(
                message="Invalid or missing 'date'. Use YYYY-MM-DD.",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        target_date = d.date()
        week_start, week_end = week_range_for_date(target_date)
        qs = (
            TimeEntry.objects.filter(
                user=request.user,
                date__gte=week_start,
                date__lte=week_end,
            )
        )
        total_minutes = sum(e.duration_minutes for e in qs)
        return success_response(
            data={
                "total_minutes": total_minutes,
                "total_duration": minutes_to_hh_mm(total_minutes),
            },
            message="OK",
        )


class DaySummaryView(APIView):
    """GET /api/time-tracking/calendar/day-summary/?date=YYYY-MM-DD"""

    def get(self, request: Request) -> Any:
        date_param = request.query_params.get("date")
        d = _parse_date(date_param)
        if d is None:
            return error_response(
                message="Invalid or missing 'date'. Use YYYY-MM-DD.",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        target_date = d.date()
        qs = TimeEntry.objects.filter(user=request.user, date=target_date)
        total_minutes = sum(e.duration_minutes for e in qs)
        return success_response(
            data={
                "total_minutes": total_minutes,
                "total_duration": minutes_to_hh_mm(total_minutes),
            },
            message="OK",
        )


class CalendarEntriesView(APIView):
    """GET /api/time-tracking/calendar/entries/?date=YYYY-MM-DD&view=day|week"""

    def get(self, request: Request) -> Any:
        date_param = request.query_params.get("date")
        view_param = (request.query_params.get("view") or "day").strip().lower()
        d = _parse_date(date_param)
        if d is None:
            return error_response(
                message="Invalid or missing 'date'. Use YYYY-MM-DD.",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        if view_param not in ("day", "week"):
            return error_response(
                message="Invalid 'view'. Use 'day' or 'week'.",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        target_date = d.date()
        if view_param == "day":
            qs = TimeEntry.objects.filter(user=request.user, date=target_date)
        else:
            week_start, week_end = week_range_for_date(target_date)
            qs = TimeEntry.objects.filter(
                user=request.user,
                date__gte=week_start,
                date__lte=week_end,
            )
        qs = qs.select_related("project").order_by("date", "start_time")
        serializer = CalendarEntrySerializer(qs, many=True)
        return success_response(data={"entries": serializer.data}, message="OK")
