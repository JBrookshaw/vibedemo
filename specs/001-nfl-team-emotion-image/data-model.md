# Data Model: NFL team emotion-based image generator

Entities
--------

- Team
  - team_id: string (canonical slug)
  - name: string
  - official_colors: array[string]
  - logo_ref: string (URL or asset id)

- TweetSample
  - tweet_id: string
  - text: string (redacted if sensitive)
  - created_at: datetime
  - author_handle: string
  - verified: boolean
  - relevance_score: float

- AnalysisResult
  - analysis_id: uuid
  - team_id: string
  - timestamp: datetime
  - timeframe: string (e.g., "24h", "7d", "30d")
  - emotion_breakdown: map[string -> float]
  - top_topics: array[string]
  - sample_tweets: array[TweetSample] (store limited excerpts)
  - verification_weighting: boolean

- GeneratedImageRecord
  - image_id: uuid
  - analysis_id: uuid
  - team_id: string
  - created_at: datetime
  - image_url: string
  - summary_text: string

Relationships
-------------
- Team 1..* AnalysisResult
- AnalysisResult 1..1 GeneratedImageRecord

Validation rules
----------------
- tweet_id, team_id, analysis_id, image_id must be unique.
- emotion_breakdown values must sum approximately to 1.0 (or 100% if percentages used).
- timeframe must be one of ["24h","7d","30d"].

State transitions
-----------------
- AnalysisResult: created -> completed -> archived
- GeneratedImageRecord: created -> available
