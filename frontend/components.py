import streamlit as st

def risk_badge(level):
    st.metric("Risk Level", level)

def show_guidance(items):
    st.subheader("Recommended actions")
    for i,item in enumerate(items,1): st.write(f"**{i}.** {item}")
