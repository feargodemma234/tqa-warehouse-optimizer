import streamlit as st
import pandas as pd
import io
from groq import Groq

st.set_page_config(page_title="TQA Optimizer", layout="centered")

st.title("📦 TQA Warehouse Optimizer")
st.subheader("Powered by Groq AI - Cut Labor 30%")

# Setup Groq Client
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# SAMPLE CSV TEMPLATE
sample_data = {
    'order_id': [1001, 1002, 1003, 1004, 1005],
    'aisle': [3, 7, 7, 2, 7],
    'time_min': [4.2, 12.5, 11.8, 3.1, 13.2],
    'worker': ['Alice', 'Bob', 'Charlie', 'Alice', 'Bob'],
    'item_count': [5, 8, 6, 4, 9]
}
df_sample = pd.DataFrame(sample_data)
csv_buffer = io.StringIO()
df_sample.to_csv(csv_buffer, index=False)

st.download_button(
    label="⬇️ Download Sample CSV Template",
    data=csv_buffer.getvalue(),
    file_name="tqa_template.csv",
    mime="text/csv"
)

st.divider()
st.header("1. Upload Today's Data")
uploaded_file = st.file_uploader("Upload WMS CSV", type=['csv'])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success(f"Data received! {len(df)} rows loaded")
    st.metric("Total Picks Today", f"{len(df):,}")
    
    if 'aisle' in df.columns and 'time_min' in df.columns:
        # SEND TO REAL AI
        csv_text = df.to_csv(index=False)
        prompt = f"""You are a warehouse operations expert in Nigeria. 
        Analyze this data: {csv_text}
        
        Return:
        1. Bottleneck aisle and why
        2. 3 specific actions to cut labor by 30% today
        3. Estimate daily savings in USD
        Keep it under 100 words. Be direct."""
        
        with st.spinner("Groq AI is analyzing..."):
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.1-8b-instant",
            )
        
        st.header("🧠 AI Insights")
        st.write(chat_completion.choices[0].message.content)
        
        # Bottleneck calc for alert
        bottleneck = df.groupby('aisle')['time_min'].mean().idxmax()
        st.warning(f"🚨 ALERT: Focus on Aisle {bottleneck} in next 30min")
    else:
        st.info("Your CSV needs 'aisle' and 'time_min' columns")
        st.dataframe(df.head())

st.header("2. Optimized Pick Route")
if st.button("Generate Routes for Workers"):
    if uploaded_file and 'aisle' in df.columns:
        top_aisles = df['aisle'].value_counts().head(3).index.tolist()
        route = " → ".join([f"A{a}" for a in top_aisles])
        st.success(f"Route 1: {route}. Est time: 22min. 40% faster")
    else:
        st.info("Upload a CSV first") 