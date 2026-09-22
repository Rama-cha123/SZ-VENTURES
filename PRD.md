# Portal Implementation PRD

## Phase 1: Database Verification & Baseline (COMPLETED)
- `[x]` Verify execution of `02_portal_schema.sql` (Verified by user. Tables: profiles, ventures, team_members, projects, documents exist with RLS and policies).
- `[x]` Verify user `team_members` assignments.

## Phase 2: Frontend Data Binding & Views
- `[ ]` Dashboard: Load aggregate venture metrics (completed mock, needs DB data).
- `[ ]` Ventures: Implement grid and detail views.
- `[ ]` Team: Implement directory view and invite mock.
- `[ ]` Projects: Implement project lists, creation forms, and status toggles.
- `[ ]` Documents: Implement file listing and dummy upload logic mapped to private bucket.
- `[ ]` Reports: Generate dynamic table from DB rows.
- `[ ]` Settings: Basic account display and logout logic.

## Phase 3: Quality Gate (CodeRabbit)
- `[ ]` Run AST check on `portal.js` and `auth.js`.
- `[ ]` Run SAST on `server.py` extensions and upload paths.
- `[ ]` Review UI integration and RLS handling edge-cases.
