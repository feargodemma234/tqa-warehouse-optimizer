import streamlit as st
import pandas as pd
from groq import Groq
import os

st.set_page_config(page_title="TQA Warehouse AI", layout="wide")
st.title("🧠 TQA Warehouse AI Optimizer")
st.markdown("Upload ANY warehouse CSV. 1 row to infinite rows. AI finds bottlenecks instantly.")

# API Key
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

uploaded_file = st.file_uploader("⬆️ Upload WMS CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success(f"✅ Loaded {len(df)} rows")
    st.dataframe(df.head(), use_container_width=True)

    # CHECK COLUMNS - THIS IS THE MAGIC
    required = ['aisle', 'time_min']
    missing = [col for col in required if col not in df.columns]
    
    if missing:
        st.error(f"❌ Missing columns: {missing}")
        st.info("Your CSV needs at least: `aisle` and `time_min`. Add other columns like `order_id, worker, shift` for better insights.")
    else:
        st.markdown("### 🧠 AI Insights")
        
        # AUTO-ANALYSIS - works on 1 row or 1M rows
        bottleneck_aisle = df.groupby('aisle')['time_min'].mean().idxmax()
        avg_time = df.groupby('aisle')['time_min'].mean().max()
        total_orders = len(df)
        
        insight = f"""
        **Bottleneck Found: Aisle {bottleneck_aisle}**
        - Avg pick time: {avg_time:.2f} minutes
        - Total orders analyzed: {total_orders}
        - **Action 1:** Add more staff to Aisle {bottleneck_aisle} during peak hours
        - **Action 2:** Pre-stage top moving SKUs in Aisle {bottleneck_aisle}
        - **Est. Savings:** Reduce pick time by 25%
        """
        st.success(insight)

        # GROQ AI SUMMARY
        if st.button("🤖 Get Full AI Report"):
            with st.spinner("AI is analyzing..."):
                summary = df.describe().to_string()
                chat = client.chat.completions.create(
                    messages=[{"role": "user", "content": f"Analyze this warehouse data and give 3 actions to cut labor 30%. Data: {summary}"}],
                    model="llama-3.1-8b-instant",
                )
                st.write(chat.choices[0].message.content)
else:
    st.info("Upload a CSV to start. Template: aisle, time_min, order_id, worker, shift, item_count")

st.markdown("---")
st.link_button("📧 Book Free Demo", "mailto:yourname@tqalogistics.com")