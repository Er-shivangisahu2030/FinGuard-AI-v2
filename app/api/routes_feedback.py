from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.database import crud
from app.services.retraining_service import retrain_from_verified_feedback

router=APIRouter(prefix='/feedback',tags=['feedback'])
class FeedbackRequest(BaseModel):
    complaint_id:str
    predicted_category:str
    corrected_category:str
    reviewer_decision:str='reviewed'
    reviewer_comment:str=''
    is_used_for_training:bool=False

@router.post('')
def feedback(req:FeedbackRequest):
    try:
        crud.add_feedback(req.model_dump())
        result={'status':'saved'}
        if req.is_used_for_training:
            result['retraining']=retrain_from_verified_feedback()
        return result
    except Exception as e:
        raise HTTPException(503,str(e))
