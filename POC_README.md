# PoC: NFL team emotion-based image generator

Backend (FastAPI) and a minimal static frontend.

Run backend (from repo root):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.app:app --reload
```

Open `frontend/index.html` in a browser (file:// or serve with a static server). Click a team and Generate. The backend uses mocked tweets and saves images under `backend/_poc_images/`.
