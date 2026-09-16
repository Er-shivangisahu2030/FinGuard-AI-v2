from fastapi import FastAPI
from app.api.routes_analysis import router as analysis_router
from app.api.routes_complaints import router as complaints_router
from app.api.routes_feedback import router as feedback_router
from app.api.routes_analytics import router as analytics_router

app=FastAPI(title="FinGuard AI",version="2.0.0",description="Explainable fintech complaint intelligence and risk assessment API")
app.include_router(analysis_router); app.include_router(complaints_router); app.include_router(feedback_router); app.include_router(analytics_router)
@app.get("/")
def root(): return {"name":"FinGuard AI","status":"running","docs":"/docs"}
@app.get("/health")
def health(): return {"status":"ok"}
