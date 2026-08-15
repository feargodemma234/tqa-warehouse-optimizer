
        

       import streamlit as st
import pandas as pd
from groq import Groq
import os

st.set_page_config(page_title="TQA Warehouse AI", layout="wide")
st.title("🧠 TQA Warehouse AI Optimizer")
st.markdown("Upload ANY warehouse CSV. Uses ALL columns to find insights.")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

uploaded_file = st.file_uploader("⬆️ Upload WMS CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success(f"✅ Loaded {len(df)} rows with {len(df.columns)} columns")
    st.dataframe(df.head(), use_container_width=True)

    st.markdown("### 🧠 AI Insights Using ALL Your Data")
    
    # AUTO-FIND TIME AND LOCATION COLUMNS
    time_cols = [c for c in df.columns if 'time' in c.lower() or 'min' in c.lower() or 'duration' in c.lower()]
    location_cols = [c for c in df.columns if 'aisle' in c.lower() or 'zone' in c.lower() or 'location' in c.lower() or 'area' in c.lower()]
    
    if len(time_cols) > 0 and len(location_cols) > 0:
        time_col = time_cols[0]
        loc_col = location_cols[0]
        
        bottleneck = df.groupby(loc_col)[time_col].mean().idxmax()
        avg_time = df.groupby(loc_col)[time_col].mean().max()
        
        st.success(f"**Bottleneck: {loc_col} = {bottleneck}**")
        st.info(f"**Avg Time:** {avg_time:.2f} minutes")
    
    # USE ALL OTHER COLUMNS FOR AI
    if st.button("🤖 Get Full AI Report Using All Data"):
        with st.spinner("AI is reading all columns..."):
            all_data = df.to_string()
            chat = client.chat.completions.create(
                messages=[{"role": "user", "content": f"You are a warehouse consultant. Analyze ALL columns in this data and give 3 specific actions to cut labor 30%. Data: {all_data[:4000]}"}],
                model="llama-3.1-8b-instant",
            )
            st.write(chat.choices[0].message.content)
else:
    st.info("Upload any CSV. More columns = smarter AI insights")

