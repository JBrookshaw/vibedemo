from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
from uuid import uuid4
from datetime import datetime
import random
import os

from PIL import Image, ImageDraw, ImageFont

app = FastAPI()

# Development CORS: allow requests from local frontend/dev origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory stores for PoC
ANALYSES: Dict[str, dict] = {}
IMAGES: Dict[str, dict] = {}


class IngestRequest(BaseModel):
    team_id: str
    timeframe: Optional[str] = "24h"
    use_verified_weighting: Optional[bool] = True


class GenerateRequest(BaseModel):
    analysis_id: str


def mock_fetch_tweets(team_id: str, timeframe: str) -> List[dict]:
    # Return mocked tweet dicts with simple text and verified flag
    sample_texts = [
        f"Great game for {team_id} fans!",
        f"Disappointed with the referee calls affecting {team_id}.",
        f"{team_id} player had an amazing play!",
        f"Concerned about injury reports for {team_id} players.",
        f"Love the new coaching moves for {team_id}!",
    ]
    tweets = []
    for i in range(20):
        tweets.append({
            "tweet_id": f"{team_id}-{i}",
            "text": random.choice(sample_texts),
            "created_at": datetime.utcnow().isoformat(),
            "author_handle": f"user{i}",
            "verified": random.random() < 0.2,
        })
    return tweets


def simple_emotion_analysis(texts: List[str], verified_flags: List[bool], weight_verified: bool):
    # Very naive emotion scoring: count positive/negative words
    positive = ["great", "amazing", "love"]
    negative = ["disappointed", "concerned", "injury"]
    scores = {"joy": 0.0, "anger": 0.0, "sadness": 0.0, "neutral": 0.0}
    for t, v in zip(texts, verified_flags):
        tlow = t.lower()
        score = 1.0
        if any(p in tlow for p in positive):
            scores["joy"] += 1.0 * (2.0 if (v and weight_verified) else 1.0)
        elif any(n in tlow for n in negative):
            scores["sadness"] += 1.0 * (2.0 if (v and weight_verified) else 1.0)
        else:
            scores["neutral"] += 1.0
    total = sum(scores.values())
    if total == 0:
        return {k: 0.0 for k in scores}
    return {k: round(v / total, 2) for k, v in scores.items()}


def compose_image(team_id: str, emotions: Dict[str, float], topics: List[str]) -> str:
    # Create a simple PNG that uses color to reflect dominant emotion
    dominant = max(emotions.items(), key=lambda x: x[1])[0] if emotions else "neutral"
    color_map = {"joy": (255, 223, 0), "sadness": (30, 60, 150), "anger": (200, 30, 30), "neutral": (200, 200, 200)}
    color = color_map.get(dominant, (180, 180, 180))
    img = Image.new("RGB", (800, 600), color)
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("/Library/Fonts/Arial.ttf", 32)
    except Exception:
        font = ImageFont.load_default()
    draw.text((20, 20), f"{team_id} - {dominant}", fill=(0, 0, 0), font=font)
    draw.text((20, 70), f"Topics: {', '.join(topics[:3])}", fill=(0, 0, 0), font=font)
    out_dir = os.path.join(os.getcwd(), "backend", "_poc_images")
    os.makedirs(out_dir, exist_ok=True)
    image_id = str(uuid4())
    path = os.path.join(out_dir, f"{image_id}.png")
    img.save(path)
    return path


@app.post("/ingest")
def ingest(req: IngestRequest):
    tweets = mock_fetch_tweets(req.team_id, req.timeframe)
    texts = [t["text"] for t in tweets]
    verified = [t["verified"] for t in tweets]
    emotions = simple_emotion_analysis(texts, verified, req.use_verified_weighting)
    top_topics = ["game", "coaching", "player"]
    analysis_id = str(uuid4())
    analysis = {
        "analysis_id": analysis_id,
        "team_id": req.team_id,
        "timestamp": datetime.utcnow().isoformat(),
        "timeframe": req.timeframe,
        "emotion_breakdown": emotions,
        "top_topics": top_topics,
        "sample_tweets": tweets[:5],
    }
    ANALYSES[analysis_id] = analysis
    return {"analysis_id": analysis_id, "status": "completed"}


@app.get("/analysis/{analysis_id}")
def get_analysis(analysis_id: str):
    if analysis_id not in ANALYSES:
        raise HTTPException(status_code=404, detail="analysis not found")
    return ANALYSES[analysis_id]


@app.post("/generate")
def generate(req: GenerateRequest):
    if req.analysis_id not in ANALYSES:
        raise HTTPException(status_code=404, detail="analysis not found")
    analysis = ANALYSES[req.analysis_id]
    path = compose_image(analysis["team_id"], analysis["emotion_breakdown"], analysis["top_topics"])
    image_id = str(uuid4())
    IMAGES[image_id] = {"image_id": image_id, "path": path, "created_at": datetime.utcnow().isoformat()}
    return {"image_id": image_id, "image_path": path}
