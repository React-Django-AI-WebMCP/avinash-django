"""Calendar aggregation and date-range helpers. Timezone: UTC (per Technical Document §5)."""

from datetime import date, timedelta


def week_range_for_date(d: date) -> tuple[date, date]:
    """Return (monday, sunday) for the week containing d. Week = Monday–Sunday."""
    # weekday(): Monday=0, Sunday=6
    monday = d - timedelta(days=d.weekday())
    sunday = monday + timedelta(days=6)
    return monday, sunday


def minutes_to_hh_mm(total_minutes: int) -> str:
    """Format total minutes as 'HH:MM' per REQUIREMENTS §2.8."""
    h, m = divmod(max(0, total_minutes), 60)
    return f"{h:02d}:{m:02d}"
