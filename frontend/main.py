from pathlib import Path
from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI(title="MargHQ", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static frontend files
app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

@app.get("/")
def home():
    return FileResponse(FRONTEND_DIR / "index.html")


class CareerRequest(BaseModel):
    interests: List[str] = Field(..., description="User interests")
    strengths: List[str] = Field(..., description="User strengths")
    personality: str = Field(..., description="analytical, creative, social, leadership")
    work_style: str = Field(..., description="independent, team, flexible")
    risk_tolerance: str = Field(..., description="low, medium, high")


career_profiles = [
    {
        "name": "Software Engineer",
        "keywords": ["coding", "technology", "problem solving", "logic", "systems", "ai", "data"],
        "personality": ["analytical", "curious", "structured"],
        "work_style": ["independent", "focused"],
        "risk_tolerance": ["medium", "high"],
    },
    {
        "name": "Product Manager",
        "keywords": ["strategy", "planning", "business", "research", "people", "communication", "decision making"],
        "personality": ["leadership", "social", "strategic"],
        "work_style": ["team", "collaborative"],
        "risk_tolerance": ["medium", "high"],
    },
    {
        "name": "UX Designer",
        "keywords": ["design", "creativity", "user", "visual", "art", "experience", "storytelling"],
        "personality": ["creative", "empathetic", "visual"],
        "work_style": ["team", "creative", "collaborative"],
        "risk_tolerance": ["low", "medium"],
    },
    {
        "name": "Data Analyst",
        "keywords": ["data", "analysis", "numbers", "research", "patterns", "insight", "statistics"],
        "personality": ["analytical", "detail-oriented", "curious"],
        "work_style": ["independent", "focused"],
        "risk_tolerance": ["low", "medium"],
    },
    {
        "name": "Teacher",
        "keywords": ["teaching", "mentoring", "learning", "communication", "helping", "guidance"],
        "personality": ["social", "empathetic", "supportive"],
        "work_style": ["team", "collaborative", "people-first"],
        "risk_tolerance": ["low", "medium"],
    },
    {
        "name": "Entrepreneur",
        "keywords": ["business", "building", "leadership", "risk", "innovation", "growth", "ideas"],
        "personality": ["leadership", "bold", "visionary"],
        "work_style": ["flexible", "independent", "fast-paced"],
        "risk_tolerance": ["high"],
    },
]


def normalize(value: str) -> str:
    return value.lower().strip()


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "MargHQ backend is running"}


@app.post("/api/find-career")
def find_career(request: CareerRequest):
    labels = [*request.interests, *request.strengths]
    normalized_labels = [normalize(item) for item in labels]

    scored = []

    for profile in career_profiles:
        score = 0
        reasons = []

        for label in normalized_labels:
            if label in [normalize(item) for item in profile["keywords"]]:
                score += 2
                reasons.append(f"Matches interest/strength: {label}")

        if normalize(request.personality) in [normalize(item) for item in profile["personality"]]:
            score += 3
            reasons.append(f"Matches personality: {request.personality}")

        if normalize(request.work_style) in [normalize(item) for item in profile["work_style"]]:
            score += 2
            reasons.append(f"Matches work style: {request.work_style}")

        if normalize(request.risk_tolerance) in [normalize(item) for item in profile["risk_tolerance"]]:
            score += 2
            reasons.append(f"Matches risk tolerance: {request.risk_tolerance}")

        scored.append({
            "career": profile["name"],
            "score": score,
            "reasons": reasons,
        })

    top_matches = sorted(scored, key=lambda item: item["score"], reverse=True)[:3]
    best = top_matches[0] if top_matches else {"career": "No clear match", "score": 0, "reasons": []}

    return {
        "best_match": best,
        "alternatives": top_matches[1:],
        "input": request.dict(),
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
