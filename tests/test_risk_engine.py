from app.services.risk_engine import calculate_risk

def test_risk():
    result=calculate_risk("OTP_SCAM", {"indicator_score":45,"indicators":["OTP_REQUEST","UPI_PIN_REQUEST"],"evidence":[]}, 1, 4, 15000)
    assert result["risk_score"] > 50
    assert result["risk_level"] in {"HIGH","CRITICAL"}
