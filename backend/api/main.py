from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes.combined import router as combined_router
from .routes.bot import router as bot_router
from .routes.toxic import router as toxic_router

app = FastAPI(
    title="Toxic Comment & Bot Detection API",
    description="API for Toxic Comment Detection, Bot Detection, and Combined Analysis",
    version="1.0.0"
)

# -------------------- CORS CONFIG --------------------
# Allows React frontend (localhost:3000) to call FastAPI (localhost:8000)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- ROUTES --------------------

app.include_router(
    toxic_router,
    prefix="/toxic",
    tags=["Toxic Comment"]
)

app.include_router(
    bot_router,
    prefix="/bot",
    tags=["Bot Detection"]
)

app.include_router(
    combined_router,
    prefix="/analysis",
    tags=["Combined Analysis"]
)

# -------------------- HEALTH CHECK --------------------

@app.get("/")
def health_check():
    return {"status": "API running successfully"}
