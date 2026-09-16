CATEGORY_SCORE = {"UPI_FRAUD":20,"OTP_SCAM":20,"FAKE_KYC":15,"PHISHING":20,"CARD_FRAUD":20,"UNAUTHORIZED_TRANSACTION":25,"REFUND_ISSUE":5,"PAYMENT_FAILURE":5,"ACCOUNT_ISSUE":5,"OTHER":0}
SEVERITY_SCORE = {1:0,2:5,3:10,4:20}

def amount_score(amount):
    try: amount=float(amount)
    except: amount=0
    if amount<=0:return 0
    if amount<1000:return 2
    if amount<5000:return 5
    if amount<10000:return 8
    if amount<50000:return 12
    return 15

def combination_bonus(indicators):
    s=set(indicators or []); b=0
    pairs=[("OTP_REQUEST","UPI_PIN_REQUEST"),("KYC_REQUEST","SUSPICIOUS_LINK"),("FAKE_SUPPORT","OTP_REQUEST"),("REMOTE_ACCESS_REQUEST","FAKE_SUPPORT"),("PAYMENT_REQUEST","REWARD_PRIZE_SCAM")]
    for a,c in pairs:
        if a in s and c in s:b+=10
    if len(s)>=4:b+=10
    elif len(s)>=3:b+=5
    return min(b,25)

def calculate_risk(category, indicator_result=None, unauthorized_transaction=0, severity=1, transaction_amount=0):
    indicator_result=indicator_result or {}; indicators=indicator_result.get("indicators",[])
    try: unauth=int(unauthorized_transaction)
    except: unauth=0
    try: sev=int(severity)
    except: sev=1
    breakdown={"category_score":CATEGORY_SCORE.get(str(category).upper(),0),"indicator_score":min(int(indicator_result.get("indicator_score",0)),60),"unauthorized_transaction_score":25 if unauth==1 else 0,"severity_score":SEVERITY_SCORE.get(sev,0),"transaction_amount_score":amount_score(transaction_amount),"combination_bonus":combination_bonus(indicators)}
    score=min(sum(breakdown.values()),100)
    level="CRITICAL" if score>=80 else "HIGH" if score>=60 else "MEDIUM" if score>=30 else "LOW"
    reasons=[]
    if breakdown["category_score"]: reasons.append(f"Complaint classified as {category}.")
    for e in indicator_result.get("evidence",[]): reasons.append(f"Detected indicator: {e['name']}.")
    if unauth==1: reasons.append("Customer reported an unauthorized transaction.")
    if sev>=3: reasons.append(f"Complaint severity is {sev}/4.")
    if float(transaction_amount or 0)>=10000: reasons.append("Complaint involves a relatively high transaction amount.")
    if not reasons: reasons=["No major risk signals were identified."]
    return {"risk_score":score,"risk_level":level,"priority":"URGENT" if level=="CRITICAL" else "HIGH" if level=="HIGH" else "NORMAL" if level=="MEDIUM" else "LOW","score_breakdown":breakdown,"indicators":indicators,"reasons":list(dict.fromkeys(reasons)),"human_review_required":level in {"HIGH","CRITICAL"}}
