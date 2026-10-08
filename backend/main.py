from pathlib import Path
from typing import Any

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, field_validator

# Detect base path whether running locally or on hosting providers
BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent / "frontend" if (BASE_DIR.parent / "frontend").exists() else BASE_DIR / "frontend"

app = FastAPI(title="MargHQ", version="1.0.0")

# Enable CORS for all incoming frontend domains (Vercel, GitHub Pages, Localhost)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")
    app.mount("/frontend", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")


@app.get("/")
def home():
    if FRONTEND_DIR.exists() and (FRONTEND_DIR / "index.html").exists():
        return FileResponse(FRONTEND_DIR / "index.html")
    return {"status": "ok", "message": "MargHQ API is running"}


class AssessmentInput(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    frustration_tolerance: int = Field(ge=1, le=5)
    immersion: int = Field(ge=1, le=5)
    failure_resilience: int = Field(ge=1, le=5)
    energy_level: int = Field(ge=1, le=5)
    social_energy: int = Field(ge=1, le=5)
    preference_for_structure: int = Field(ge=1, le=5)
    creative_drive: int = Field(ge=1, le=5)
    problem_solving_drive: int = Field(ge=1, le=5)


class CareerRequest(BaseModel):
    interests: list[str]
    strengths: list[str]
    personality: str
    work_style: str
    risk_tolerance: str


class JobRequest(BaseModel):
    targetJob: str = Field(min_length=1, max_length=120)

    @field_validator("targetJob")
    @classmethod
    def target_job_must_not_be_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Enter a target career.")
        return value


PROJECTS = {
    "engineering": [
        {"title": "Mini calculator app", "duration": "1 week"},
        {"title": "Task manager with login", "duration": "2 weeks"},
        {"title": "Portfolio website", "duration": "3 weeks"},
    ],
    "design": [
        {"title": "UX case study redesign", "duration": "1 week"},
        {"title": "Landing page redesign", "duration": "2 weeks"},
        {"title": "App interface mockup", "duration": "3 weeks"},
    ],
    "product": [
        {"title": "Problem statement notebook", "duration": "1 week"},
        {"title": "Feature prioritization board", "duration": "2 weeks"},
        {"title": "Product idea pitch deck", "duration": "3 weeks"},
    ],
    "research": [
        {"title": "Career comparison research", "duration": "1 week"},
        {"title": "Data-driven trend analysis", "duration": "2 weeks"},
        {"title": "Interview summary dashboard", "duration": "3 weeks"},
    ],
    "teaching": [
        {"title": "Short workshop lesson plan", "duration": "1 week"},
        {"title": "Mentor guide document", "duration": "2 weeks"},
        {"title": "Learning module design", "duration": "3 weeks"},
    ],
    "business": [
        {"title": "Startup idea sketch", "duration": "1 week"},
        {"title": "Mini market research report", "duration": "2 weeks"},
        {"title": "Business pitch presentation", "duration": "3 weeks"},
    ],
}


def score_profile(data: AssessmentInput) -> dict[str, Any]:
    scores = {
        "engineering": data.frustration_tolerance + data.immersion + data.failure_resilience + (6 - data.preference_for_structure) + data.problem_solving_drive,
        "design": data.immersion + data.creative_drive,
        "product": data.failure_resilience + data.energy_level + data.social_energy + data.creative_drive + data.problem_solving_drive,
        "research": data.frustration_tolerance + data.immersion + (6 - data.preference_for_structure) + data.problem_solving_drive,
        "teaching": data.energy_level + data.social_energy,
        "business": data.failure_resilience + data.energy_level + data.social_energy + data.creative_drive,
    }
    ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    best_path = ranked[0][0]
    summary = {
        "frustration_tolerance": data.frustration_tolerance,
        "immersion": data.immersion,
        "failure_resilience": data.failure_resilience,
        "energy_level": data.energy_level,
        "social_energy": data.social_energy,
    }
    return {
        "name": data.name.strip(),
        "best_path": best_path,
        "alternative_paths": [path for path, _ in ranked[1:3]],
        "scores": scores,
        "summary": summary,
        "projects": PROJECTS[best_path],
        "message": f"Your answers point toward {best_path} as a promising direction to explore.",
    }


CAREER_PROFILES = [
    {"name": "Software Engineer", "keywords": ["coding", "technology", "problem solving", "logic", "systems", "ai", "data"], "personality": ["analytical", "curious", "structured"], "work_style": ["independent", "focused"], "risk_tolerance": ["medium", "high"]},
    {"name": "Product Manager", "keywords": ["strategy", "planning", "business", "research", "people", "communication", "decision making"], "personality": ["leadership", "social", "strategic"], "work_style": ["team", "collaborative"], "risk_tolerance": ["medium", "high"]},
    {"name": "UX Designer", "keywords": ["design", "creativity", "user", "visual", "art", "experience", "storytelling"], "personality": ["creative", "empathetic", "visual"], "work_style": ["team", "creative", "collaborative"], "risk_tolerance": ["low", "medium"]},
    {"name": "Data Analyst", "keywords": ["data", "analysis", "numbers", "research", "patterns", "insight", "statistics"], "personality": ["analytical", "detail-oriented", "curious"], "work_style": ["independent", "focused"], "risk_tolerance": ["low", "medium"]},
    {"name": "Teacher", "keywords": ["teaching", "mentoring", "learning", "communication", "helping", "guidance"], "personality": ["social", "empathetic", "supportive"], "work_style": ["team", "collaborative", "people-first"], "risk_tolerance": ["low", "medium"]},
    {"name": "Entrepreneur", "keywords": ["business", "building", "leadership", "risk", "innovation", "growth", "ideas"], "personality": ["leadership", "bold", "visionary"], "work_style": ["flexible", "independent", "fast-paced"], "risk_tolerance": ["high"]},
]


def normalize(value: str) -> str:
    return value.strip().lower()


@app.get("/health")
def health():
    return {"status": "ok", "message": "MargHQ is ready"}


# Accepts requests under both /assess and /api/assess
@app.post("/assess")
@app.post("/api/assess")
def assess(data: AssessmentInput):
    return score_profile(data)


# Accepts requests under both /find-career and /api/find-career
@app.post("/find-career")
@app.post("/api/find-career")
def find_career(request: CareerRequest):
    labels = [normalize(value) for value in [*request.interests, *request.strengths]]
    scored = []
    for profile in CAREER_PROFILES:
        keywords = [normalize(value) for value in profile["keywords"]]
        personality = [normalize(value) for value in profile["personality"]]
        work_styles = [normalize(value) for value in profile["work_style"]]
        risk_levels = [normalize(value) for value in profile["risk_tolerance"]]
        matched = [label for label in labels if label in keywords]
        score = len(matched) * 2
        reasons = [f"Matches interest or strength: {label}" for label in matched]
        if normalize(request.personality) in personality:
            score += 3
            reasons.append(f"Matches personality: {request.personality}")
        if normalize(request.work_style) in work_styles:
            score += 2
            reasons.append(f"Matches work style: {request.work_style}")
        if normalize(request.risk_tolerance) in risk_levels:
            score += 2
            reasons.append(f"Matches risk tolerance: {request.risk_tolerance}")
        scored.append({"career": profile["name"], "score": score, "reasons": reasons})
    top_matches = sorted(scored, key=lambda item: item["score"], reverse=True)[:3]
    return {"best_match": top_matches[0], "alternatives": top_matches[1:], "input": request.model_dump()}


# Accepts requests under both /generate-roadmap and /api/generate-roadmap
@app.post("/generate-roadmap")
@app.post("/api/generate-roadmap")
def generate_roadmap(req: JobRequest):
    job = req.targetJob
    stages = [
        ("1", 0, "Learn the foundations", "Study the core concepts and tools used in this field. Choose one beginner-friendly course and set a weekly learning rhythm.", "Weeks 1-4"),
        ("2", 140, "Build a practical project", f"Apply the basics to a small, real-world {job} project. Document your decisions, iterations, and what you learned.", "Weeks 5-8"),
        ("3", 280, "Create your portfolio and apply", f"Present your project as a clear case study, ask for feedback, and prepare targeted applications for {job} opportunities.", "Weeks 9-12"),
    ]
    return {
        "nodes": [
            {
                "id": node_id,
                "type": "default",
                "position": {"x": 250, "y": y},
                "data": {"label": f"{int(node_id)}. {title}", "description": description, "duration": duration},
            }
            for node_id, y, title, description, duration in stages
        ],
        "edges": [
            {"id": "e1-2", "source": "1", "target": "2", "animated": True},
            {"id": "e2-3", "source": "2", "target": "3", "animated": True},
        ],
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)