from app.database.connection import get_db_connection

def create_complaint(data):
    c=get_db_connection(); cur=c.cursor()
    q="""INSERT INTO complaints(complaint_id,complaint_text,category,transaction_amount,payment_method,unauthorized_transaction,severity,sentiment,risk_score,risk_level,priority,assigned_team,escalation_required,human_review_required) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    vals=(data["complaint_id"],data["complaint_text"],data.get("category"),data.get("transaction_amount",0),data.get("payment_method"),data.get("unauthorized_transaction",0),data.get("severity",1),data.get("sentiment"),data.get("risk_score"),data.get("risk_level"),data.get("priority"),data.get("assigned_team"),data.get("escalation_required",False),data.get("human_review_required",False))
    cur.execute(q,vals); c.commit(); cur.close(); c.close()

def add_indicators(complaint_id,evidence):
    c=get_db_connection(); cur=c.cursor(); q="INSERT INTO scam_indicators(complaint_id,indicator_code,indicator_name,matched_keywords,indicator_score) VALUES(%s,%s,%s,%s,%s)"
    for e in evidence: cur.execute(q,(complaint_id,e["indicator"],e["name"],", ".join(e.get("matched_keywords",[])),e.get("score",0)))
    c.commit(); cur.close(); c.close()

def add_guidance(complaint_id,items):
    c=get_db_connection(); cur=c.cursor(); q="INSERT INTO complaint_guidance(complaint_id,guidance_text,guidance_order) VALUES(%s,%s,%s)"
    for i,item in enumerate(items,1): cur.execute(q,(complaint_id,item,i))
    c.commit(); cur.close(); c.close()

def get_complaint(complaint_id):
    c=get_db_connection(); cur=c.cursor(dictionary=True); cur.execute("SELECT * FROM complaints WHERE complaint_id=%s",(complaint_id,)); r=cur.fetchone(); cur.close(); c.close(); return r

def get_all_complaints(limit=100):
    limit=max(1,min(int(limit),1000)); c=get_db_connection(); cur=c.cursor(dictionary=True); cur.execute(f"SELECT * FROM complaints ORDER BY created_at DESC LIMIT {limit}"); r=cur.fetchall(); cur.close(); c.close(); return r

def get_priority_complaints(limit=100):
    limit=max(1,min(int(limit),1000)); c=get_db_connection(); cur=c.cursor(dictionary=True); cur.execute(f"SELECT * FROM complaints WHERE risk_level IN ('HIGH','CRITICAL') ORDER BY risk_score DESC, created_at ASC LIMIT {limit}"); r=cur.fetchall(); cur.close(); c.close(); return r

def add_feedback(data):
    c=get_db_connection(); cur=c.cursor(); q="INSERT INTO feedback(complaint_id,predicted_category,corrected_category,reviewer_decision,reviewer_comment,is_used_for_training) VALUES(%s,%s,%s,%s,%s,%s)"; cur.execute(q,(data["complaint_id"],data.get("predicted_category"),data.get("corrected_category"),data.get("reviewer_decision"),data.get("reviewer_comment",""),data.get("is_used_for_training",False))); c.commit(); cur.close(); c.close()
