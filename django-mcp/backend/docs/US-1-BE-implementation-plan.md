# Implementation Plan: [BE] US-1 Implement API & Logic

**Ticket:** [86d2284h0](https://app.clickup.com/t/86d2284h0)  
**Technical Document:** [US-1-technical-spec.md](./US-1-technical-spec.md) §3 Backend Blueprint

---

## 1. Cursor rules to apply

Before and during implementation, ensure compliance with:

| Rule | Path | Relevance |
|------|------|------------|
| **URL routing** | [.cursor/rules/django/url-routing-rules.mdc](../../.cursor/rules/django/url-routing-rules.mdc) | Resources as nouns; query params for filtering (`?date=`, `?view=`); no verbs in URLs. Base path `/api/time-tracking/calendar/` is consistent. |
| **API response** | [.cursor/rules/django/api-response-rules.mdc](../../.cursor/rules/django/api-response-rules.mdc) | Use **core.responses**: `success_response(data=..., message=...)` for success; `error_response(message=..., errors=..., status_code=...)` for errors. Project shape: `success`, `message`, `data` (and `errors` when applicable). Do not invent a different shape. |
| **Django REST API** | [.cursor/rules/django/django-rest-api-development-rules-adnan.mdc](../../.cursor/rules/django/django-rest-api-development-rules-adnan.mdc) | App structure: `time_tracker/urls.py`, `views.py`, `serializers.py`; optional `services.py` for logic. Keep views thin; use DRF APIView/CBV; RESTful methods and status codes. |
| **Error handling** | [.cursor/rules/django/error-handling-rules.mdc](../../.cursor/rules/django/error-handling-rules.mdc) | Use `core.exceptions` (e.g. `ApplicationError`, `ConflictError`) where appropriate; 400/404/401 map to `error_response`. DRF `custom_exception_handler` already normalizes to `success: false, message, errors`. |
| **Type hints** | [.cursor/rules/django/type-hints-rules.mdc](../../.cursor/rules/django/type-hints-rules.mdc) | Add type hints to view methods and serializers where the rule specifies. |
| **Code formatting** | [.cursor/rules/django/code-formatting-rules.mdc](../../.cursor/rules/django/code-formatting-rules.mdc) | Follow project formatting (e.g. Ruff/Black) and line-length. |

**Checklist before PR:** Run any project linters/formatters; confirm no rule violations in new files.

---

## 2. Prerequisites

- **[DB] US-1 Schema Implementation** ([86d2284ga](https://app.clickup.com/t/86d2284ga)) should be done: `time_tracker` in `INSTALLED_APPS`, `TimeEntry` model (and optionally `Project`) with migrations applied.
- If `time_tracker` is not yet in `INSTALLED_APPS`: add it to `LOCAL_APPS` in [config/settings/base.py](../config/settings/base.py).
- Auth: DRF default is `IsAuthenticated` + JWT; all three endpoints must require auth and filter by `request.user`.

---

## 3. Implementation steps

### 3.1 URL wiring

- **config/urls.py:** Add `path("api/time-tracking/", include("time_tracker.urls"))` (or equivalent so calendar endpoints live under `/api/time-tracking/`).
- **time_tracker/urls.py:** Define routes for:
  - `GET calendar/week-summary/` → week summary view (query param `date`)
  - `GET calendar/day-summary/` → day summary view (query param `date`)
  - `GET calendar/entries/` → entries list view (query params `date`, `view=day|week`)

Follow [url-routing-rules](../../.cursor/rules/django/url-routing-rules.mdc): plural/resources, query params for filtering.

### 3.2 Serializers

- **time_tracker/serializers.py** (or per-view serializers):
  - **WeekSummarySerializer** (or simple dict): `total_minutes` and/or `total_duration` (e.g. `"HH:MM"` per REQUIREMENTS §2.8). Technical Document allows either.
  - **DaySummarySerializer:** same shape for one day.
  - **CalendarEntrySerializer:** `title`, `start_time`, `end_time` (or `duration`), `entry_type` (logged | mentioned | integrated), `project` or `project_color`. No extra fields.

Use DRF serializers; read-only for these endpoints.

### 3.3 Views / business logic

- **time_tracker/views.py** (or split into `views/calendar.py`):
  - **WeekSummaryView:** `GET`; query param `date` (YYYY-MM-DD). Week = Monday–Sunday containing that date. Filter `TimeEntry` by `user=request.user`, `date__range=(week_start, week_end)`. Aggregate total duration; return via `success_response(data={...})`.
  - **DaySummaryView:** `GET`; query param `date`. Filter by `user`, `date`. Aggregate; return same response shape.
  - **CalendarEntriesView:** `GET`; query params `date`, `view=day|week`. If `view=day`, filter by `user` and `date`. If `view=week`, filter by `user` and `date__range=(week_start, week_end)`. Return list of entries serialized with `CalendarEntrySerializer`; return via `success_response(data={"entries": [...]})` or `data=[...]` per project convention.

Use `core.responses.success_response` for 200; use `core.responses.error_response` for 400 (e.g. invalid/missing `date`). 401 handled by DRF when not authenticated.

- **Validation:** Validate `date` (valid ISO date) and `view` (day | week); return 400 with clear message if invalid.
- **Timezone:** Document assumption (e.g. store in UTC; or use project default). Technical Document §5 NEEDS CLARIFICATION — pick one and comment in code.

### 3.4 Permissions and auth

- Rely on DRF default `IsAuthenticated` (already in [config/settings/base.py](../config/settings/base.py)). No custom permission class unless required; filter all querysets by `request.user`.

### 3.5 Exception handling

- Invalid/missing query params → `error_response(message="...", status_code=400)`.
- Use `core.exceptions` (e.g. `ApplicationError`) only if a rule fits; otherwise plain `error_response` is enough.
- Do not leak stack traces; use existing `custom_exception_handler` for unhandled exceptions.

---

## 4. Postman collection

- **No existing Postman collection** in repo; create one.
- **Location:** e.g. `backend/postman/Time-Tracker-US1.postman_collection.json` or `backend/docs/postman/Time-Tracker-US1.postman_collection.json`.
- **Contents:**
  - **Collection:** "Time Tracker — US-1 Calendar APIs".
  - **Environment (optional):** variable `base_url` (e.g. `http://localhost:8000`) and `token` for Bearer auth.
  - **Requests:**
    1. **GET Week summary** — `{{base_url}}/api/time-tracking/calendar/week-summary/?date=2025-05-19`. Auth: Bearer `{{token}}`. Document expected response: `success`, `message`, `data` with `total_minutes` and/or `total_duration`.
    2. **GET Day summary** — `{{base_url}}/api/time-tracking/calendar/day-summary/?date=2025-05-19`. Auth: Bearer `{{token}}`.
    3. **GET Calendar entries (day)** — `{{base_url}}/api/time-tracking/calendar/entries/?date=2025-05-19&view=day`. Auth: Bearer `{{token}}`.
    4. **GET Calendar entries (week)** — `{{base_url}}/api/time-tracking/calendar/entries/?date=2025-05-19&view=week`. Auth: Bearer `{{token}}`.
  - Add one request without token to confirm 401 (optional).
- **Format:** Postman Collection v2.1 JSON export so it can be imported and run.

---

## 5. Done criteria (from ticket)

- [ ] API adheres to defined path/method and response shapes (Technical Document §3).
- [ ] All three endpoints require authentication; data filtered by current user.
- [ ] Cursor rules checked (URL, API response, DRF structure, error handling).
- [ ] Postman collection added and committed with the three (or four) requests.
- [ ] No deviation from the Technical Document (no extra fields, no new endpoints).

---

## 6. File checklist

| Action | File / path |
|--------|-------------|
| Edit | `config/urls.py` — include time_tracker URLs under `api/time-tracking/` |
| Create or edit | `time_tracker/urls.py` — calendar routes |
| Create or edit | `time_tracker/views.py` — WeekSummary, DaySummary, CalendarEntries views |
| Create or edit | `time_tracker/serializers.py` — summary + entry serializers |
| Optional | `time_tracker/services.py` — week/day range and aggregation helpers |
| Create | `postman/Time-Tracker-US1.postman_collection.json` (implemented under `backend/postman/`) |
| Verify | `config/settings/base.py` — `time_tracker` in `INSTALLED_APPS` (if not already from [DB]) |
