# Quickstart: NFL team emotion-based image generator (developer)

Prerequisites
- Python 3.11
- Node.js 18+ (for frontend)
- Access credentials for chosen data provider (Twitter/X API) or local sample dataset

Local dev (fast path)

1. Backend: create virtualenv and install requirements

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Frontend

```bash
cd frontend
npm install
npm run dev
```

3. Run ingestion & analysis with mocked data (example)

```bash
export MOCK_TWEETS=1
python backend/run_pipeline.py --team "patriots" --timeframe 24h
```

4. Open the frontend at http://localhost:3000 and select a team.

Notes
- This quickstart uses mock data when `MOCK_TWEETS=1`. Replace with valid credentials and configure provider settings to test live ingestion.
