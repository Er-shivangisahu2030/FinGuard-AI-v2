from fastapi import APIRouter, HTTPException
from app.database.connection import get_db_connection
router=APIRouter(prefix="/analytics",tags=["analytics"])
@router.get("/summary")
def summary():
    try:
        c=get_db_connection(); cur=c.cursor(dictionary=True)
        cur.execute("SELECT COUNT(*) total, COALESCE(AVG(risk_score),0) avg_risk, SUM(risk_level='CRITICAL') critical, SUM(risk_level='HIGH') high, SUM(risk_level='MEDIUM') medium, SUM(risk_level='LOW') low FROM complaints")
        overall=cur.fetchone(); cur.execute("SELECT category,COUNT(*) count FROM complaints GROUP BY category ORDER BY count DESC"); cats=cur.fetchall(); cur.close(); c.close(); return {"overall":overall,"categories":cats}
    except Exception as e: raise HTTPException(503,str(e))
