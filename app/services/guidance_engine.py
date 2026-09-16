GUIDANCE={
"UPI_FRAUD":["Contact your bank or payment provider through an official support channel.","Report the unauthorized UPI transaction immediately.","Do not approve unexpected UPI collect requests.","Do not share your UPI PIN."],
"OTP_SCAM":["Never share an OTP or verification code with a caller.","Contact your bank through an official support channel.","Report any unauthorized transaction immediately."],
"FAKE_KYC":["Do not provide information through an unexpected KYC request.","Verify KYC status directly through the official app or website.","Do not click unsolicited KYC links."],
"PHISHING":["Do not click suspicious links.","Do not enter banking credentials through unsolicited links.","Use the official banking app or manually enter the official website."],
"CARD_FRAUD":["Contact your card issuer through an official channel.","Block or temporarily disable the affected card if necessary.","Report unauthorized card transactions immediately."],
"UNAUTHORIZED_TRANSACTION":["Report the unauthorized transaction immediately.","Review recent transactions in the official banking app.","Preserve transaction details and relevant messages."],
"REFUND_ISSUE":["Check refund status through the official app.","Keep the transaction reference number available.","Do not pay an unexpected fee to receive a refund."],
"PAYMENT_FAILURE":["Check transaction status before retrying.","Keep the transaction reference number available.","Contact the provider if money was debited but the payment failed."],
"ACCOUNT_ISSUE":["Use the official app to check account status.","Do not share passwords or verification codes.","Contact official support if access remains unavailable."],
"OTHER":["Use the official support channel for assistance.","Do not share sensitive financial credentials.","Keep relevant transaction details available."]}
INDICATOR_GUIDANCE={"OTP_REQUEST":"Do not share any OTP or verification code.","UPI_PIN_REQUEST":"Never share your UPI PIN.","KYC_REQUEST":"Verify KYC requests directly through the official app.","REMOTE_ACCESS_REQUEST":"Do not install remote-access software at another person's request.","SUSPICIOUS_LINK":"Do not click suspicious links or enter credentials through them.","URGENT_THREAT":"Do not act under pressure; verify through an official channel.","FAKE_SUPPORT":"Use the official support number instead of an unexpected caller.","PAYMENT_REQUEST":"Do not make unexpected payments or fees to receive a refund or reward.","REWARD_PRIZE_SCAM":"Do not pay a fee to claim an unexpected prize.","IMPERSONATION":"Verify the identity of anyone claiming to represent a bank or authority.","CARD_DETAILS_REQUEST":"Do not share card details, CVV, PIN, or OTP.","BANK_DETAILS_REQUEST":"Do not share sensitive bank-account information with unverified individuals."}

def generate_guidance(category,risk_level="LOW",indicators=None,unauthorized_transaction=0):
    indicators=indicators or []; items=list(GUIDANCE.get(str(category).upper(),GUIDANCE["OTHER"]))
    for i in indicators:
        if i in INDICATOR_GUIDANCE and INDICATOR_GUIDANCE[i] not in items:items.append(INDICATOR_GUIDANCE[i])
    if risk_level in {"HIGH","CRITICAL"}: items += ["Preserve screenshots, transaction references, messages, and other evidence.","Human investigation is recommended."]
    if risk_level=="CRITICAL": items += ["Treat this complaint as urgent.","Contact the relevant financial institution immediately through an official channel."]
    if int(unauthorized_transaction or 0)==1: items.append("Contact the relevant financial institution immediately through an official channel.")
    items=list(dict.fromkeys(items))[:12]
    return {"headline":"Urgent attention recommended." if risk_level=="CRITICAL" else "Immediate attention is recommended." if risk_level=="HIGH" else "Please review the following precautions." if risk_level=="MEDIUM" else "Here are some recommended next steps.","category":category,"risk_level":risk_level,"guidance":items,"indicator_count":len(indicators),"human_review_recommended":risk_level in {"HIGH","CRITICAL"}}
