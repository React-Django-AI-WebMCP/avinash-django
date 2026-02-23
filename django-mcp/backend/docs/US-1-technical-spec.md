# US-1 Technical Document — Navigate to Calendar and change date or view

**User story:** [86d2278vx](https://app.clickup.com/t/86d2278vx) (subtask of epic [86d2271x5](https://app.clickup.com/t/86d2271x5))  
**Requirements:** [REQUIREMENTS.md](../REQUIREMENTS.md) §2.1, §2.2 Actions 1–3, §2.7, §2.8, §3.1, §3.3, §3.4, §3.6  

**Deliverable:** Backend only. No frontend is created.

---

## 1. Scope Boundary

### Backend in scope for US-1

- APIs required so a client can render:
  - **Week's log total** (e.g. "32:30 hrs") for the week containing the selected date
  - **Day total** (e.g. "08:24 hrs") for the selected day
  - **Calendar entries** overlaid on the grid for a selected day and, for Week view, for the week containing that day
- Data scoped to the **current authenticated user** (REQUIREMENTS §2.3; ownership taken as current user for implementation)
- Support a single **date** (day total + entries for that day) and a **week** containing that date (week total + entries). Week boundary: default Monday–Sunday; see NEEDS CLARIFICATION if product needs different

### Out of scope for US-1 (backend)

- "Logged" tab API
- Project Tasks panel API (US-2)
- Create Entry API (US-3)
- Edit/delete APIs
- **Frontend: not built**

### Boundary rule

No APIs, fields, or validations beyond what support the above.

---

## 2. Frontend Blueprint

**Out of scope for this deliverable.** Only backend is implemented. Frontend will consume the APIs described in Backend Blueprint.

---

## 3. Backend Blueprint

### APIs (minimal, from story + REQUIREMENTS)

| API | Purpose | Endpoint | Response |
|-----|---------|----------|----------|
| **Week total** | Display "Week's log: 32:30 hrs" for the week containing the selected date | `GET /api/time-tracking/calendar/week-summary/?date=YYYY-MM-DD` | Total duration for that week for the current user (e.g. `total_minutes` or `total_duration` in "HH:MM" per REQUIREMENTS §2.8) |
| **Day total** | Display "08:24 hrs" for the selected day | `GET /api/time-tracking/calendar/day-summary/?date=YYYY-MM-DD` | Total duration for that day for the current user |
| **Calendar entries** | Entries to overlay on the grid (day or week view) | `GET /api/time-tracking/calendar/entries/?date=YYYY-MM-DD&view=day` or `view=week` | List of entries; each with **title**, **start_time** / **end_time** or **duration**, **entry_type** (logged \| mentioned \| integrated), **project** or **project_color** (REQUIREMENTS §2.7, §3.4). No extra fields invented |

### Authentication

- All endpoints require authenticated user
- Filter all data by that user
- Use existing project auth

### Integration

- Add `time_tracker` URLs under `api/time-tracking/` (or project convention)
- Use `core` patterns (base models, responses) where applicable

---

## 4. Data Schema

### Minimal schema to support the three APIs

- **Time entry** (or equivalent): one calendar entry per user  
  - **user** (FK to auth User)  
  - **date** (date)  
  - **start_time**, **end_time** (or **duration**)  
  - **title**  
  - **entry_type** (logged \| mentioned \| integrated)  
  - **project** (FK or id for project color)  
  - Use `core.models.BaseModel` (UUID, timestamps, soft delete) if applicable  
  - No extra fields (description, billable are US-3)

- **Project** (if needed for color/name): minimal — id, name, color — so entries can return project color. If not required for read-only display, use minimal option (e.g. project_id + color on entry).

### PostgreSQL

- Django models and migrations only
- All queries filter by request user

---

## 5. NEEDS CLARIFICATION

1. **Week boundary:** Definition of "week" (e.g. Monday–Sunday vs Sunday–Saturday) for week total and week-view entries. This document assumes one default; confirm if product needs different.
2. **Timezone:** Storage and API for dates/times (UTC vs user timezone). Document will state an assumption in implementation; clarify if product requires otherwise.
3. **Project model:** Whether a separate Project model exists or is in scope; if not, implementation will use minimal representation (e.g. project_id + color on entry or minimal Project table).
