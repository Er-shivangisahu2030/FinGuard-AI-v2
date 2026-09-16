import uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.api.routes_analysis import AnalysisRequest
from app.database import crud

router=APIRouter(prefix="/complaints",tags=["complaints"])
class ComplaintRequest(AnalysisRequest): pass

@router.post("")
def create(req:ComplaintRequest):
    from app.api.routes_analysis import analyze
    result=analyze(req)
    cid="CMP-"+uuid.uuid4().hex[:10].upper()
    row={"complaint_id":cid,"complaint_text":req.complaint_text,"category":result["prediction"]["category"],"transaction_amount":req.transaction_amount,"payment_method":req.payment_method,"unauthorized_transaction":req.unauthorized_transaction,"severity":req.severity,"sentiment":req.sentiment,"risk_score":result["risk"]["risk_score"],"risk_level":result["risk"]["risk_level"],"priority":result["risk"]["priority"],"assigned_team":result["routing"]["assigned_team"],"escalation_required":result["routing"]["escalation_required"],"human_review_required":result["risk"]["human_review_required"]}
    try:
        crud.create_complaint(row); crud.add_indicators(cid,result["indicators"]["evidence"]); crud.add_guidance(cid,result["guidance"]["guidance"])
    except Exception as e:
        raise HTTPException(503,f"Analysis succeeded but database save failed: {e}")
    return {"complaint_id":cid,**result}

@router.get("")
def list_complaints(limit:int=100):
    try:return crud.get_all_complaints(limit)
    except Exception as e: raise HTTPException(503,str(e))

@router.get("/priority")
def priority(limit:int=100):
    try:return crud.get_priority_complaints(limit)
    except Exception as e: raise HTTPException(503,str(e))

@router.get("/{complaint_id}")
def get(complaint_id:str):
    try:r=crud.get_complaint(complaint_id)
    except Exception as e: raise HTTPException(503,str(e))
    if not r: raise HTTPException(404,"Complaint not found")
    return r
