# Research: NFL team emotion-based image generator

Created: 2025-10-22

Purpose
-------
Resolve technical unknowns required to proceed to design (Phase 1). Each decision includes rationale and alternatives.

Decisions
---------

1) Language / Platform
   - Decision: Backend services will use Python 3.11 and FastAPI for the ingestion and analysis microservices; frontend will be a React single-page app (TypeScript).
   - Rationale: Python has rich ML/ NLP ecosystem (transformers, spaCy, Hugging Face), FastAPI is lightweight for microservices and integrates well with async HTTP requests for ingestion. React + TypeScript is standard for rapid UI development and matches many teams' skill sets.
   - Alternatives considered:
     - Node.js backend: good for I/O but weaker ML ecosystem.
     - Go/Rust: performant but increases ML integration complexity.

2) Data provider (Twitter access)
   - Decision: Target Twitter/X official API if project has access; otherwise prototype using publicly available datasets or a third-party historical tweets provider. Abstract the ingestion layer to swap providers.
   - Rationale: Official API provides structured access and metadata (verified flag). Prototyping without API allows development while credentials/plan are secured.
   - Alternatives considered:
     - Third-party paid providers: easier historical access but costlier and vendor lock-in.
     - Web scraping: not recommended (terms & legality, brittle).

3) Emotion & topic analysis approach
   - Decision: Start with off-the-shelf transformer-based sentiment/emotion models (e.g., Hugging Face emotion classification models) and an unsupervised topic extraction pipeline (RAKE/KeyBERT or embeddings+clustering). Weight verified tweets as specified in the spec.
   - Rationale: Off-the-shelf models accelerate MVP; can later replace or fine-tune with domain-specific data. Topic extraction via embeddings yields robust multi-word topics.
   - Alternatives considered:
     - Train custom models from scratch: higher accuracy potential but much higher cost/time.
     - Use commercial sentiment APIs: quick but may have cost and privacy implications.

4) Image generation approach
   - Decision: Use a controlled, template-driven image composition approach for MVP (color palettes mapped to emotions, simple graphic overlays for topics), with a medium-term plan to experiment with generative models for stylized outputs.
   - Rationale: Template composition reduces legal/ethical risk and inference cost; fulfills user need for an immediate visual summary. Generative models can be introduced later for richer visuals once safety and cost are addressed.
   - Alternatives considered:
     - Use diffusion models directly (DALL·E/StableDiffusion): rich results but higher cost, moderation needs, and deeper safety review.

5) Storage and persistence
   - Decision: Use a small relational store (PostgreSQL) for metadata (GeneratedImageRecord, AnalysisResult references) and an object store (S3-compatible) for image blobs.
   - Rationale: Simple, reliable, and common patterns supported by most cloud providers; easy to query history and maintain metadata.
   - Alternatives considered:
     - NoSQL store for metadata: viable but relational schema is simple and easier for queries.

6) Performance goals
   - Decision: Target generation latency <= 30s for 95% of requests (SC-001). Support low to moderate concurrency for initial launch (hundreds of concurrent users); profile and scale later.
   - Rationale: Matches spec success criteria and is realistic for composition-based image generation. Generative model usage will revisit SLAs.

7) Privacy & legal
   - Decision: Only use public posts; redact PII; perform legal review before any public/commercial release involving team logos or player images.
   - Rationale: Reduces compliance risk and follows spec constraints.

Research tasks generated (Phase 0)
--------------------------------
- Task: Confirm data provider access and limits (Twitter/X API plan) — owner: product/legal
- Task: Evaluate top 2 off-the-shelf emotion models for accuracy on a small sample (n=100) — owner: ML
- Task: Prototype topic extraction (KeyBERT + embeddings) on sample tweets for a few teams — owner: ML
- Task: Prototype template-driven image composer and verify visual mapping for emotions — owner: creative/ML
- Task: Confirm storage options and S3 credentials for image blobs — owner: infra

Decision log (summary)
----------------------
- Chosen stack: Python 3.11 + FastAPI backend; React + TypeScript frontend.
- Data provider: Prefer official Twitter/X API; prototype with cached datasets if unavailable.
- Analysis: Start with HF emotion classifiers and KeyBERT/embedding topic extraction.
- Image generation: Template-driven composition for MVP, evaluate generative models later.

Next steps
----------
Proceed to Phase 1: generate `data-model.md`, API contracts, and quickstart.md. Ensure the ingestion module is abstracted to swap data providers. Begin the evaluation tasks listed above in parallel to shorten integration time.
