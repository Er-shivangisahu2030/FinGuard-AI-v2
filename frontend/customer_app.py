import os
import requests
import streamlit as st
from dotenv import load_dotenv

from frontend.components import show_guidance


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

load_dotenv()

API = os.getenv(
    "API_BASE_URL",
    "http://127.0.0.1:8000"
)


# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="FinGuard AI",
    page_icon="🛡️",
    layout="wide"
)


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------

st.title("🛡️ FinGuard AI")

st.caption(
    "Digital payment complaint intelligence and risk-assessment assistant"
)


# ---------------------------------------------------------
# Complaint Form
# ---------------------------------------------------------

with st.form("complaint_form"):

    text = st.text_area(
        "Describe your complaint",
        height=180,
        placeholder=(
            "Example: Someone claiming to be from my bank "
            "asked for my OTP and sent me a link..."
        )
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        amount = st.number_input(
            "Transaction amount (₹)",
            min_value=0.0,
            value=0.0,
            step=100.0
        )

    with col2:
        method = st.selectbox(
            "Payment method",
            [
                "UNKNOWN",
                "UPI",
                "CARD",
                "NET_BANKING",
                "WALLET"
            ]
        )

    with col3:
        severity = st.selectbox(
            "Severity",
            [1, 2, 3, 4],
            index=0
        )

    unauthorized = st.checkbox(
        "I did not authorize the transaction"
    )

    sentiment = st.selectbox(
        "How would you describe the complaint tone?",
        [
            "neutral",
            "negative"
        ]
    )

    submitted = st.form_submit_button(
        "Analyze Complaint",
        type="primary"
    )


# ---------------------------------------------------------
# Process Complaint
# ---------------------------------------------------------

if submitted:

    # Validate complaint text
    if len(text.strip()) < 5:

        st.error(
            "Please provide a little more detail about your complaint."
        )

    else:

        try:

            # -------------------------------------------------
            # Send complaint to FastAPI backend
            # -------------------------------------------------

            response = requests.post(
                f"{API}/complaints",
                json={
                    "complaint_text": text,
                    "transaction_amount": amount,
                    "payment_method": method,
                    "unauthorized_transaction": int(unauthorized),
                    "severity": severity,
                    "sentiment": sentiment
                },
                timeout=30
            )

            response.raise_for_status()

            data = response.json()

            # -------------------------------------------------
            # Extract results
            # -------------------------------------------------

            complaint_id = data["complaint_id"]
            prediction = data["prediction"]
            risk = data["risk"]
            indicators = data["indicators"]
            guidance = data["guidance"]
            routing = data["routing"]


            # -------------------------------------------------
            # Success message
            # -------------------------------------------------

            st.success(
                f"Complaint created successfully: {complaint_id}"
            )


            # -------------------------------------------------
            # Main Results
            # -------------------------------------------------

            st.subheader("Analysis Result")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Category",
                    prediction["category"]
                )

            with col2:
                st.metric(
                    "Risk Score",
                    risk["risk_score"]
                )

            with col3:
                st.metric(
                    "Priority",
                    risk["priority"]
                )


            # -------------------------------------------------
            # Risk Level
            # -------------------------------------------------

            risk_level = risk["risk_level"]

            if risk_level in ["HIGH", "CRITICAL"]:

                st.warning(
                    f"Risk Level: {risk_level}"
                )

            else:

                st.info(
                    f"Risk Level: {risk_level}"
                )


            # -------------------------------------------------
            # Detected Indicators
            # -------------------------------------------------

            st.subheader("Detected Indicators")

            detected = indicators["indicators"]

            if detected:

                for indicator in detected:
                    st.write(f"• {indicator}")

            else:

                st.write(
                    "No major suspicious indicators detected."
                )


            # -------------------------------------------------
            # Recommended Guidance
            # -------------------------------------------------

            show_guidance(
                guidance["guidance"]
            )


            # -------------------------------------------------
            # Support Routing
            # -------------------------------------------------

            st.subheader("Support Routing")

            st.write(
                f"**Assigned Team:** "
                f"{routing['assigned_team']}"
            )

            if routing["escalation_required"]:

                st.warning(
                    "Escalation required: Yes"
                )

            else:

                st.info(
                    "Escalation required: No"
                )


            # -------------------------------------------------
            # Disclaimer
            # -------------------------------------------------

            st.caption(
                "FinGuard AI is a decision-support system. "
                "A high risk score does not prove fraud. "
                "Follow official financial-institution reporting "
                "processes for suspected fraud or unauthorized "
                "transactions."
            )


        # -----------------------------------------------------
        # Error Handling
        # -----------------------------------------------------

        except requests.exceptions.ConnectionError:

            st.error(
                "Could not connect to the FinGuard API. "
                "Please make sure the FastAPI backend is running."
            )

        except requests.exceptions.Timeout:

            st.error(
                "The backend took too long to respond. "
                "Please try again."
            )

        except requests.exceptions.HTTPError as e:

            st.error(
                f"The API returned an error: {e}"
            )

        except Exception as e:

            st.error(
                f"Something went wrong: {e}"
            )