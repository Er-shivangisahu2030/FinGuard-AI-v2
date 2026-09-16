ROUTING={"UPI_FRAUD":"Fraud Investigation Team","OTP_SCAM":"Fraud Investigation Team","FAKE_KYC":"Fraud Investigation Team","PHISHING":"Cybersecurity / Fraud Team","CARD_FRAUD":"Card Security Team","UNAUTHORIZED_TRANSACTION":"Fraud Investigation Team","REFUND_ISSUE":"Payments Support Team","PAYMENT_FAILURE":"Payments Support Team","ACCOUNT_ISSUE":"Account Support Team","OTHER":"General Support Team"}

def route_complaint(category,risk_level="LOW",unauthorized_transaction=0,indicators=None,payment_method=None):
    indicators=indicators or []; level=str(risk_level).upper(); team=ROUTING.get(str(category).upper(),"General Support Team")
    escalation=level in {"HIGH","CRITICAL"} or int(unauthorized_transaction or 0)==1 or len(set(indicators))>=3
    if escalation: team="Fraud Investigation Team"
    return {"assigned_team":team,"priority":"URGENT" if level=="CRITICAL" else "HIGH" if level=="HIGH" else "NORMAL" if level=="MEDIUM" else "LOW","escalation_required":escalation,"category":category,"risk_level":level,"payment_method":payment_method,"reasons":[f"Category {category} routed to {team}."] + ([f"Risk level is {level}, requiring priority handling."] if level in {"HIGH","CRITICAL"} else []) + (["Unauthorized transaction was reported."] if int(unauthorized_transaction or 0)==1 else [])}
