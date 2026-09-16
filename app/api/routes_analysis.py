from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.ml.predictor import predict_category
from app.services.indicator_detector import detect_indicators
from app.services.risk_engine import calculate_risk
from app.services.guidance_engine import generate_guidance
from app.services.routing_engine import route_complaint

router=APIRouter(prefix="/analysis",tags=["analysis"])
class AnalysisRequest(BaseModel):
    complaint_text:str=Field(min_length=5,max_length=5000)
    transaction_amount:float=0
    payment_method:str="UNKNOWN"
    unauthorized_transaction:int=0
    severity:int=1
    sentiment:str="neutral"

@router.post("/analyze")
def analyze(req:AnalysisRequest):
    try:
        prediction=predict_category(req.complaint_text)
    except Exception as e:
        raise HTTPException(500,str(e))
    indicators=detect_indicators(req.complaint_text)
    risk=calculate_risk(prediction["category"],indicators,req.unauthorized_transaction,req.severity,req.transaction_amount)
    guidance=generate_guidance(prediction["category"],risk["risk_level"],indicators["indicators"],req.unauthorized_transaction)
    routing=route_complaint(prediction["category"],risk["risk_level"],req.unauthorized_transaction,indicators["indicators"],req.payment_method)
    return {"prediction":prediction,"indicators":indicators,"risk":risk,"guidance":guidance,"routing":routing}
