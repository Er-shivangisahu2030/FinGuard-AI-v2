from app.ml.preprocessor import clean_text

def test_clean_text():
    out=clean_text("I was asked for my OTP!!!")
    assert "otp" in out
