````markdown
# Implementation Plan: NFL team emotion-based image generator

**Branch**: `001-nfl-team-emotion-image` | **Date**: 2025-10-22 | **Spec**: `spec.md`
**Input**: Feature specification from `/Users/jeff/Documents/git/vibedemo/specs/001-nfl-team-emotion-image/spec.md`

## Summary

Build a web application where users select an NFL team by logo, the system fetches recent public posts (default 24h) about the team, performs emotion and topic analysis (verified accounts weighted), and generates an image that visually reflects aggregated emotions and topics. The MVP will use Python/FastAPI backend microservices, React + TypeScript frontend, and template-driven image composition for safety and speed.

## Technical Context

**Language/Version**: Python 3.11 (backend), TypeScript + React (frontend)
**Primary Dependencies**: FastAPI, HTTPX, Hugging Face transformers, KeyBERT/embedding libraries, React, Vite or Next.js (frontend)  
**Storage**: PostgreSQL for metadata; S3-compatible object store for images
**Testing**: pytest (backend), Jest/React Testing Library (frontend)
**Target Platform**: Linux servers (cloud), modern browsers (desktop + mobile)
**Project Type**: Web application (frontend + backend microservices)
**Performance Goals**: Image generation latency <= 30s for 95% of requests; initial concurrency target: modest (hundreds of concurrent users), scale later
**Constraints**: Use only public posts; redact PII; respect provider terms; default timeframe 24h (user-selectable)
**Scale/Scope**: MVP focused on single-tenant or low-scale public demo; plan for horizontal scaling later

## Constitution Check

Gates derived from `.specify/memory/constitution.md` are placeholders in the repo. No blocking constitution violations were detected for Phase 0. The plan will adhere to core principles once the project's constitution content is ratified.

## Project Structure

### Documentation (this feature)

```text
specs/001-nfl-team-emotion-image/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── ingestion-openapi.yaml
   └── analysis-openapi.yaml
└── checklists/
    └── requirements.md
```

### Source Code (recommended layout)

```text
backend/
├── ingestion-service/       # fetches posts, caching, rate-limit handling
├── analysis-service/        # emotion & topic analysis
├── generation-service/      # image composition and storage
└── common/                  # shared models, utils, auth

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/            # API clients
└── tests/

infrastructure/
├── helm/ or terraform/      # infra templates (optional)
└── scripts/

tests/
├── integration/
└── contract/
```

**Structure Decision**: Web application with separate backend services for clear separation of concerns and independent scaling.

## Complexity Tracking

No constitution gate violations detected. If later the constitution specifies mandatory TDD or library-first rules, we will ensure tests and modular libraries are added before PRs are merged.

## Phase 0: Research output

Artifacts created:
- `research.md` — decisions & rationale
- `data-model.md` — entity definitions and validation rules
- `contracts/` — ingestion and analysis OpenAPI stubs
- `quickstart.md` — local dev notes and mocked data

Next: Phase 1 — design & contracts (data-model and /contracts already created). Follow-up tasks: create implementation tasks, flesh out OpenAPI details, and begin prototype work for ingestion and emotion model evaluation.

