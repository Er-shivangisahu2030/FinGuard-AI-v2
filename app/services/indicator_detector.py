import re

RULES = {
    "OTP_REQUEST": ("OTP Request", 20, ["otp", "one time password", "verification code"]),
    "UPI_PIN_REQUEST": ("UPI PIN Request", 25, ["upi pin", "share your pin", "enter your pin", "pin number"]),
    "KYC_REQUEST": ("KYC Update Request", 15, ["kyc", "update kyc", "kyc expired", "verify kyc"]),
    "REMOTE_ACCESS_REQUEST": ("Remote Access Request", 25, ["anydesk", "teamviewer", "remote access", "screen sharing", "share your screen"]),
    "SUSPICIOUS_LINK": ("Suspicious Link", 20, ["click this link", "click the link", "verification link", "http://", "https://", "www."]),
    "URGENT_THREAT": ("Urgency or Threat", 15, ["urgent", "immediately", "act now", "account will be blocked", "last warning"]),
    "FAKE_SUPPORT": ("Fake Customer Support", 20, ["customer care called", "customer support called", "bank representative", "support agent", "representative called"]),
    "PAYMENT_REQUEST": ("Suspicious Payment Request", 20, ["send money", "pay first", "pay to receive", "processing fee", "verification fee"]),
    "REWARD_PRIZE_SCAM": ("Reward or Prize Scam", 15, ["you won", "lottery", "prize", "reward", "cash prize", "claim your reward"]),
    "IMPERSONATION": ("Impersonation", 20, ["pretending to be bank", "pretending to be support", "bank officer", "police officer", "government officer"]),
    "CARD_DETAILS_REQUEST": ("Card Details Request", 20, ["card number", "cvv", "expiry date", "card details", "share card details"]),
    "BANK_DETAILS_REQUEST": ("Bank Details Request", 20, ["bank account number", "account number", "bank details", "share bank details", "ifsc"]),
}

def detect_indicators(text: str) -> dict:
    text = re.sub(r"\s+", " ", str(text or "").lower()).strip()
    indicators, evidence, score = [], [], 0
    for code, (name, weight, keywords) in RULES.items():
        matches = [k for k in keywords if k in text]
        if matches:
            indicators.append(code)
            score += weight
            evidence.append({"indicator": code, "name": name, "matched_keywords": matches, "score": weight})
    urls = re.findall(r"https?://\S+|www\.\S+", text)
    phones = re.findall(r"\b(?:\+91[\s-]?)?[6-9]\d{9}\b", text)
    money = re.findall(r"(?:₹|rs\.?|inr)\s?\d+(?:,\d+)*(?:\.\d+)?", text, flags=re.I)
    return {"indicator_count": len(indicators), "indicators": list(dict.fromkeys(indicators)), "indicator_score": min(score, 60), "evidence": evidence, "urls_detected": urls, "phone_numbers_detected": phones, "money_references": money}
