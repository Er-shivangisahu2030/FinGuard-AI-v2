from app.ml.predictor import predict_category

def test_prediction():
    result=predict_category("Someone asked me for my OTP and verification code.")
    assert "category" in result
