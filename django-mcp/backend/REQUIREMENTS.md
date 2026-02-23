# COMBINED REQUIREMENT & UI DOCUMENTATION

### Time Tracker — Calendar Entries (Day View)

> **Source:** Figma file `02.1 Time Tracker — Nexus` · Node `12568:210659`
> **Status:** Ready to Review · 11 June 2025 · Hardik

---

## 1. Overview

This screen is the **Calendar tab** of the Time Tracking module. It shows the current user's time entries for a selected day laid out on a vertical hour-by-hour grid. Alongside the calendar, a **Project Tasks** panel lists all projects and tasks allocated to the user, from which time entries can be created by dragging tasks onto the calendar.

**Purpose (user perspective):**

- See all time entries for a day — logged, mentioned, and integrated calendar events
- Log new time entries by dragging a project task onto the calendar and filling in the "Add Entry" form
- Control which types of entries are visible on the calendar

---

## 2. Functional Requirements

### 2.1 Entry Behavior

**How the user reaches this screen:**

- The user navigates to the **"Time tracking"** section from the left navigation bar
- The user clicks the **"Calendar"** tab (toggling away from the "Logged" tab) in the page header

**What is visible on first load (Day view, default):**

- Page header with:
  - Title **"Time tracking"**
  - Two tabs: **"Logged"** and **"Calendar"** (Calendar is active)
  - Weekly log total — e.g. **"Week's log: 32:30 hrs"**
  - Day-of-week strip: **S M T W T S S** with current day highlighted
  - Date picker showing the currently selected date — e.g. **"19 May 2025"**
- Calendar content area with:
  - Sub-header showing **"Today"**, a Day/Week toggle, and total hours for the selected day — e.g. **"08:24 hrs"**
  - A vertical time grid starting from **09:00** to at least **22:00**, in hourly rows
  - All visible time entries overlaid on the grid at their respective times
- **Project Tasks** panel on the right — list of projects as collapsible accordions, each with a colored left-border indicator
- **"My Calendars"** legend section at the bottom of the Project Tasks panel with three toggle checkboxes

---

### 2.2 Core User Actions

#### Action 1 — Switch between Day and Week view

- User clicks **"Day"** or **"Week"** toggle in the calendar sub-header
- The calendar grid switches between single-day and seven-day layout
- Both Day and Week flows are present in this Figma section

#### Action 2 — Navigate to a different day

- User clicks the **left/right arrow chevrons** beside the day-of-week strip, or clicks a specific day letter (S/M/T/W/T/S/S)
- The calendar updates to show entries for the selected day
- The selected day letter becomes highlighted

#### Action 3 — Select a date using the date picker

- User clicks the date display (e.g. **"19 May 2025"**) on the right side of the header
- A date picker opens
- The user selects a date; the calendar navigates to that date

#### Action 4 — Expand a project in the Project Tasks panel

- User clicks a project row (e.g. **"Nexus"**) in the Project Tasks panel
- The accordion expands to reveal the list of tasks under that project (e.g. **"Connect", "Plan", "Design", "Reduce"**)
- A chevron icon indicates expanded (↑) vs collapsed (↓) state
- A pin icon is visible next to the expanded project's chevron

#### Action 5 — Drag a task onto the calendar to create a new time entry

1. User hovers over an expanded project task item → item enters a **hover state**
2. User presses/holds on a task item → item enters a **pressed state**; a floating task preview card appears near the cursor in the calendar area showing **"Project Name : Task Name"** with a grab-hand cursor icon
3. User drags the task card to the desired time slot on the calendar grid
4. User releases the card on the calendar → the calendar area becomes **dimmed/overlaid** and the **"Add Entry" sidecar panel** slides in from the right
5. The calendar grid behind the sidecar shows a grayed-out overlay

#### Action 6 — Fill in and submit the "Add Entry" form

- The sidecar is pre-populated with the dragged task's **Project : Task** value
- User fills in:
  - **Description** (free text)
  - **Feature** (dropdown selection)
  - **Billable** toggle (on/off)
  - **Time** range (start time – end time; duration field)
  - **Select Date** (date picker)
- User clicks **"Add"** (active/blue when fields are populated) → entry is saved
- Sidecar closes; a success toast **"Entry Added"** (green checkmark) appears at the bottom right
- The new entry appears on the calendar at the corresponding time, **colored by project color**
- The **"Add"** button remains grayed out (disabled) when required fields are empty

#### Action 7 — Reset the "Add Entry" form

- User clicks **"Reset"** inside the sidecar
- All filled-in fields are cleared back to their placeholder/empty state

#### Action 8 — Close the "Add Entry" sidecar without saving

- User clicks the **"×"** icon at the top right of the sidecar
- The sidecar closes; no entry is created; the calendar returns to its normal (non-dimmed) state

#### Action 9 — Toggle entry type visibility

In the **"My Calendars"** legend, user checks or unchecks one of the three checkboxes:

| Checkbox | Checked | Unchecked |
|---|---|---|
| **Mentioned Entries** | Dashed-border entries appear on calendar | Hidden |
| **Integrated Calendar Entries** | Integrated calendar events appear | Hidden |
| **Logged Entries** | Solid colored entry blocks appear | Hidden |

- The calendar **immediately** reflects the change by showing or hiding the corresponding entry type

---

### 2.3 Ownership Rules

> **NEED CLARIFICATION:** It is not visible from Figma whether other users' entries are shown on the calendar, or whether the "Project Tasks" panel shows tasks allocated only to the current user.

- The page header shows a weekly log total that appears to represent the **current user's** total logged hours.

---

### 2.4 Edit Rules

> **NEED CLARIFICATION:** The flow for editing an existing calendar entry is not shown in this Figma section. No click-on-entry interaction is depicted for editing.

---

### 2.5 Delete Rules

> **NEED CLARIFICATION:** No deletion flow for calendar entries is shown in this Figma section.

---

### 2.6 Conversion Rules

**Mentioned → Logged:**

- A "Mentioned Entry" is a time entry that has been referenced but not yet formally logged
- When the user drags a task and submits the "Add Entry" form, the result appears as a **Logged Entry** on the calendar (solid colored block) with the project's color

> **NEED CLARIFICATION:** Whether an existing "Mentioned Entry" card on the calendar can be directly converted to a "Logged Entry" from this screen is not shown.

---

### 2.7 Visibility Rules

**Entry types and their visual treatment:**

| Entry Type | Visual Style | Content Shown | Notes |
|---|---|---|---|
| **Logged Entries** | Solid filled block, project-colored | Title + duration (e.g. "Daily Scrum / 00:45 hrs") | Some show an avatar icon and a "+" icon |
| **Mentioned Entries** | Dashed border, thin horizontal bar | Title only (e.g. "Quick Sync") | Lighter/muted appearance |
| **Integrated Calendar Entries** | Gray/neutral block | Title + duration (e.g. "Review meeting / 01:00 hrs") | Can overlap each other |

- Visibility of all three types is controlled independently via the **"My Calendars"** checkboxes (see Action 9)

**Tooltip on "Logged Entries":**

- A small info icon **(ⓘ)** is visible next to the "Logged Entries" label in the legend
- Hovering it shows a tooltip: **"The color of logged entries will depend on the project color."**

---

### 2.8 Constraints & Limitations

- The **"Add"** button in the "Add Entry" sidecar is disabled (grayed out) when not sufficiently populated; it becomes active (blue) when the required fields are filled
- Time display format in the grid: **HH:MM** (24-hour clock — e.g. `09:00`, `10:00` … `22:00`)
- Date display format in the "Add Entry" form: **DD-Month-YYYY** (placeholder shown as `DD-Month-YYYY`; filled example: `15-02-2025`)
- Duration is shown alongside entries in the format: **HH:MM hrs** (e.g. `00:45 hrs`, `02:00 hrs`)

---

## 3. UI Documentation — Visual & Interaction

### 3.1 Screen Identification

| Property | Value |
|---|---|
| **Figma Node Name** | Calendar Entries: 13th june |
| **Node ID** | `12568:210659` |
| **Figma File** | 02.1 Time Tracker — Nexus |

**Key sub-frames documented:**

| Frame Name | Node ID | Purpose |
|---|---|---|
| Customise ✅ | `8484:104358` | Calendar view default states + visibility toggle states |
| Calendar: Day view (State 1) | `13516:172354` | Default — all logged + integrated entries visible |
| Calendar: Day view (State 2) | `12942:76486` | Tooltip state on "Logged Entries" info icon |
| Calendar: Day view (State 3) | `12942:76221` | Mentioned Entries unchecked, Logged Entries unchecked |
| Calendar: Day view (State 4) | `12942:76397` | Mentioned Entries checked, Logged Entries unchecked |
| Adding entries through dragging | `10755:194860` | Full drag-to-log flow (Day + Week view) |
| Day view — Default (empty) | `10755:194864` | Calendar with no entries; Project Tasks open |
| Day view — Task Hover | `12860:167464` | Project task expanded, hover state |
| Day view — Task Pressed/Dragging | `12860:177089` | Drag in progress, floating task card |
| Day view — Add Entry (empty) | `10755:195196` | "Add Entry" sidecar, empty form |
| Day view — Add Entry (filled) | `13461:79628` | "Add Entry" sidecar, Feature dropdown open |
| Day view — Add Entry (confirm) | `13580:84514` | "Add Entry" sidecar, all fields filled, Add active |
| Day view — Entry Added | `10755:195451` | Post-add state, "Entry Added" toast shown |

---

### 3.2 UI Behavior References (Visual Only)

| Element | Reference |
|---|---|
| Calendar grid | FullCalendar (day view layout) |
| Date picker | React DatePicker |
| Sidecar/Drawer | Right-side panel that slides in over the calendar |

---

### 3.3 Layout Description

```
┌──────┬──────────────────────────────────────────────┬───────────────────┐
│      │  Page Header                                 │                   │
│      │  (Time tracking | Logged | Calendar |        │                   │
│ Nav  │   Week's log | Day strip | Date picker)      │  Project Tasks    │
│      ├──────────────────────────────────────────────│  Panel            │
│      │  Calendar Sub-header                         │                   │
│      │  (Today | Day ○ Week | 08:24 hrs)            │  - Project list   │
│      ├──────────────┬───────────────────────────────│    (accordions)   │
│      │ Time labels  │ Calendar grid                 │                   │
│      │ (09:00–22:00)│ (overlaid entry blocks)       │  - My Calendars   │
│      │              │                               │    legend         │
└──────┴──────────────┴───────────────────────────────┴───────────────────┘
```

| Region | Width | Description |
|---|---|---|
| Left navigation bar | 60px | Icon-only vertical nav; Time tracking icon highlighted |
| Page header | full width, 100px tall | Title, tabs, weekly log, day strip, date picker |
| Calendar content | ~1039px | Time labels column (48px) + event grid (991px) |
| Project Tasks panel | 293px | Accordion list + "My Calendars" legend at bottom |

---

### 3.4 Visible UI Elements

#### Page Header

| Element | Content |
|---|---|
| Title | "Time tracking" (bold, large) |
| Tabs | "Logged" \| **"Calendar"** (Calendar = active, filled state) |
| Weekly log | "Week's log: **32:30 hrs**" |
| Day strip | S · M · T · **W** · T · S · S with left/right chevron arrows; current day highlighted with a circle |
| Date display | Calendar icon + "19 May 2025" (clickable → opens date picker) |

#### Calendar Sub-header

| Element | Content |
|---|---|
| Label | "Today" (left-aligned) |
| View toggle | "Day" \| pill switch \| "Week" |
| Day total | "08:24 hrs" (right-aligned) |

#### Time Grid

- Hourly labels: `09:00`, `10:00`, `11:00`, `12:00`, `13:00`, `14:00`, `15:00`, `16:00`, `17:00`, `18:00`, `19:00`, `20:00`, `21:00`, `22:00`
- Horizontal divider lines at each hour
- Vertical scrollbar on the right edge of the calendar area

#### Calendar Entries — Logged Entries (solid blocks)

| Entry Title | Fill Color | Duration | Extra |
|---|---|---|---|
| "Daily Scrum" | Blue/teal | 00:45 hrs | — |
| "Design System planning" | Purple/lavender | 02:00 hrs | — |
| "Feedback Session" | Teal | 00:30 hrs | Avatar icon + "+" icon |
| "Project Planning Call" | Blue | 00:45 hrs | Avatar icon + "+" icon |
| "Day End Scrum" | Blue | 00:30 hrs | Avatar icon + "+" icon |

#### Calendar Entries — Mentioned Entries (dashed/thin)

| Entry Title | Appearance |
|---|---|
| "Quick Sync" | Thin yellow/gold dashed horizontal bar, single-line title |
| "Review call" | Thin dashed horizontal bar (appears below Quick Sync at same time) |

#### Calendar Entries — Integrated Calendar Entries (neutral)

| Entry Title | Appearance | Duration |
|---|---|---|
| "Review meeting" | Gray/neutral block | 01:00 hrs |
| "Internal Sync Discussion" | Gray/neutral dashed block (overlaps with Review meeting) | — |

#### Project Tasks Panel — Header

- Text: **"Project tasks"** (bold)
- Icon: filter/settings icon (top right)

#### Project Tasks Panel — Project List (Accordion rows)

Each row contains:

- Colored vertical left-border (unique color per project)
- Project name text
- Chevron: ↓ = collapsed, ↑ = expanded
- When **expanded**: task names with a drag-handle icon prefix (six-dot grid icon)
- When **expanded**: a pin icon appears next to the chevron; one task may show a filled/active pin (e.g. "Connect")

**Projects visible in Figma:** Rezio, Rappid, Stolt, Robora, Aubergine Internal, Nexus, Snowflakes, NEXUS, Alignment AI

#### Project Tasks Panel — My Calendars Legend

| Row | Swatch Icon | Label | Interactive Element |
|---|---|---|---|
| 1 | Dashed/unfilled square | "Mentioned Entries" | Checkbox |
| 2 | Blue filled square | "Integrated Calendar Entries" | Checkbox |
| 3 | Gray/outlined square | "Logged Entries" + ⓘ | Checkbox |

- **ⓘ tooltip text:** "The color of logged entries will depend on the project color."

#### Drag Floating Card (during drag)

- Appears in the calendar grid area while dragging
- Displays: **Project name** + **Task name** (e.g. "Nexus · Connect")
- Grab/hand cursor icon is visible

#### Context Menu (on project accordion item)

- Appears as a floating dropdown next to the task item
- First item: Project + Task label + grab-hand icon (e.g. "Nexus : Connect")
- Three additional menu items below

> **NEED CLARIFICATION:** What triggers this context menu — right-click, long press, or an explicit button? Labels of the three sub-items are not legible at screenshot resolution.

#### "Add Entry" Sidecar Panel

| Field | Label | Placeholder / State |
|---|---|---|
| Text input | **Description** | "Write a project description" + avatar icon (right edge) |
| Dropdown | **Project : Task** | Pre-filled from dragged task (e.g. "Nexus : Design") |
| Dropdown | **Feature** | "Select feature" — options shown: Log-in, Dashboard, Action Card, Sign-up |
| Toggle button | **Billable** | $ icon — inactive (white bg) / active (green bg) |
| Time range | **Time** | Start `00:00` — End `00:00` — Duration `00:00` |
| Date picker | **Select Date** | Calendar icon + `DD-Month-YYYY` |
| Action buttons | — | **"Reset"** (secondary) · **"Add"** (primary — grayed out when empty, blue when active) |
| Close | — | **"×"** icon top-right of panel |
| Panel title | — | **"Add Entry"** |

#### "Entry Added" Toast

- Position: bottom-right of screen
- Content: green checkmark icon + **"Entry Added"** text
- Dismiss: **"×"** icon

#### New Entry on Calendar (post-add)

- Entry block appears at the logged time slot
- Filled with the **project's color** (e.g. warm orange/peach for "Daily Scrum" after add)
- Shows **entry title + duration**

---

### 3.5 UI Interactions

Interactions explicitly visible in Figma:

| # | Interaction | Trigger | Result |
|---|---|---|---|
| 1 | Logged / Calendar tab toggle | Click "Logged" or "Calendar" tab | Switches between logged list and calendar views |
| 2 | Day/Week view toggle | Click "Day" or "Week" pill | Calendar grid changes layout |
| 3 | Day navigation | Click chevron arrows or day letter in strip | Calendar moves to selected day; letter highlights |
| 4 | Date picker open | Click date display | Calendar date picker overlay opens |
| 5 | Project accordion expand/collapse | Click project row | Reveals or hides task list; chevron reflects state |
| 6 | Task hover | Mouse over task item | Item enters hover state |
| 7 | Task press | Press/hold task item | Floating drag card appears with grab cursor |
| 8 | Task drop on calendar | Release on time slot | Calendar dims; "Add Entry" sidecar slides in from right |
| 9 | Description input | Type in Description field | Field populates |
| 10 | Feature dropdown | Click Feature field | Dropdown opens with list of features; click to select |
| 11 | Billable toggle | Click $ button | Toggles between white (inactive) and green (active) |
| 12 | Time field edit | Click/type in Time fields | Start, end, duration values update |
| 13 | Date field | Click Select Date field | Date picker opens |
| 14 | Reset form | Click "Reset" | All fields clear to placeholder state |
| 15 | Submit form | Click "Add" (active state) | Entry saved; sidecar closes; "Entry Added" toast shown |
| 16 | Dismiss sidecar | Click "×" | Sidecar closes; no entry created; calendar un-dims |
| 17 | Entry visibility toggle | Check/uncheck My Calendars checkbox | Corresponding entry type shows or hides immediately |
| 18 | Info icon hover | Hover ⓘ next to "Logged Entries" | Tooltip: "The color of logged entries will depend on the project color." |
| 19 | Calendar scroll | Drag scrollbar or scroll within grid | Scrolls time grid vertically |

---

### 3.6 Component Mapping

| UI Element | Design System Component |
|---|---|
| Page header | `PageHeaderComplex - type 2` / `type 3` / `type 9` |
| Left navigation | `Navigation` |
| Calendar grid row | `TableCell` |
| Calendar sub-header | `SectionHeader - type 2` |
| Project task accordion | `_customAccordion` |
| Project task menu item | `MenuItem - simple` |
| Logged/Calendar tab buttons | `Buttons - Simple` |
| Calendar entry overlay | `ActionCardSimple` |
| Right sidecar panel | `Sidecar - 002` |
| Checkboxes | `CheckBox` |
| Mentioned Entries icon | `Component 10` |
| Integrated/Logged Entries icon | `_Component 9` |
| Tooltip | `Tooltip - Simple` |
| Context menu dropdown | `ProjectTasks 1.3` |
| Scrollbar | `Scrollbar` |

---

## 4. NEED CLARIFICATION

The following items are **ambiguous or absent** in the Figma source. They must be resolved before implementation.

| # | Topic | Gap |
|---|---|---|
| 1 | **Edit flow** | No click-on-entry interaction is shown. It is unknown whether clicking an existing entry opens an edit panel, and what fields would be editable. |
| 2 | **Delete flow** | No deletion confirmation or action is shown for any entry type in this section. |
| 3 | **"+" icon on logged entries** | Appears on Feedback Session, Project Planning Call, Day End Scrum. Its function is not shown. |
| 4 | **Avatar icon on logged entries** | Small circular avatar icon visible on some entries. Its meaning and interactivity are not shown. |
| 5 | **Context menu trigger** | The floating dropdown on project task items — not clear if it appears on right-click, long press, or a specific button click. |
| 6 | **Context menu item labels** | The three sub-items in the `ProjectTasks 1.3` dropdown are not legible at screenshot resolution. |
| 7 | **Mentioned → Logged conversion** | Whether a user can directly convert a "Mentioned Entry" into a "Logged Entry" by interacting with the calendar card is not shown. |
| 8 | **Pin icon behavior** | Pin icon appears next to an expanded project's chevron and on one task ("Connect"). Its function is not shown. |
| 9 | **"Logged" tab content** | Behavior and content of the "Logged" tab is out of scope for this Figma section. |
| 10 | **Week view parity** | The "Week view" flow is referenced but not fully documented here — confirm whether the same drag-to-add behavior applies identically. |
| 11 | **Empty calendar state** | The blank grid is shown when no entries exist, but no empty-state guidance text or CTA is visible. |
| 12 | **Filter icon in Project Tasks header** | The icon at the top right of the "Project tasks" header — its function (filter, reorder, etc.) is not shown. |
| 13 | **Ownership scope** | Not clear whether Project Tasks panel and calendar entries are scoped to the current user only, or include teammates' data. |
| 14 | **Entry type swatch icons** | `Component 10` (Mentioned Entries) differs visually from `_Component 9` (Integrated/Logged). Exact color/pattern distinction is not fully legible — confirm design system intent. |
| 15 | **Time auto-calculation** | Whether the duration field auto-calculates when start/end are set, and whether start/end are pre-filled from the drop position, is not explicitly shown. |

---

## 5. Scope Declaration

**This document defines:**

- Functional behavior of the Calendar Entries Day View screen
- UI visibility, element copy, and interactions as visible in the Figma source (`12568:210659`)

**This document explicitly excludes:**

- Backend logic, APIs, data storage, or data models
- Validation rules beyond what is visually shown in Figma
- Technical architecture, frameworks, or implementation approach
- Any screen or flow not present in node `12568:210659`
