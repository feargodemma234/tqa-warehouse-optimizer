import streamlit as st
import pandas as pd

st.set_page_config(page_title="TQA Optimizer", layout="centered")

st.title("📦 TQA Warehouse Optimizer")
st.subheader("Cut Labor 30% with AI")

phone = st.text_input("Enter your phone number", placeholder="+234 80...")
if st.button("Send Login Code"):
    st.success(f"Code sent to {phone}")

st.divider()
st.header("1. Upload Today's Data")
uploaded_file = st.file_uploader("Upload WMS CSV or Take Photo", type=['csv', 'png', 'jpg'])

if uploaded_file:
    st.success("Data received! AI is analyzing...")
    st.metric("Potential Savings Today", "$3,240", "+12%")
    st.metric("Bottleneck", "Aisle 7", "Now")
    st.warning("🚨 ALERT: Move 2 people to Aisle 7 in the next 30min")

st.header("2. Optimized Pick Route")
if st.button("Generate Routes for Workers"):
    st.info("Route 1: A1 → B3 → C2. Est time: 22min. 40% faster")
    st.button("Send Routes to Workers via WhatsApp")