import streamlit as st
import pandas as pd
import joblib
import numpy as np
import time
import plotly.express as px
import plotly.graph_objects as go

# --- PAGE CONFIG ---
st.set_page_config(page_title="SOC: IoT Botnet Hunter", layout="wide", page_icon="🛡️")

# --- CUSTOM CSS FOR "HACKER MODE" DARK THEME ---
st.markdown("""
<style>
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    .metric-card {
        background-color: #262730;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #4F4F4F;
    }
</style>
""", unsafe_allow_html=True)

st.title("🛡️ SOC: IoT Botnet Hunter")
st.markdown("### Neural Network Telemetry Stream")

# --- INITIALIZE SESSION STATE FOR HISTORY GRAPHS ---
if 'history_volume' not in st.session_state:
    st.session_state['history_volume'] = []
if 'history_threat' not in st.session_state:
    st.session_state['history_threat'] = []

# --- LOAD RESOURCES ---
@st.cache_resource
def load_resources():
    model = joblib.load('universal_model.pkl') 
    try:
        # Load samples
        d_benign = pd.read_csv('data//benign_traffic.csv', nrows=200)
        d_mirai = pd.read_csv('data/thermostat_udp.csv', nrows=200)
        d_bashlite = pd.read_csv('data/doorbell_udp.csv', nrows=200)
        d_scan = pd.read_csv('data/scan.csv', nrows=200)
    except FileNotFoundError:
        st.error("Critical Error: Data files not found.")
        st.stop()
    return model, d_benign, d_mirai, d_bashlite, d_scan

try:
    model, d_benign, d_mirai, d_bashlite, d_scan = load_resources()
except Exception as e:
    st.error(f"Error: {e}")
    st.stop()

# --- DASHBOARD RENDERER ---
# FIX: Added 'key_suffix' to make every chart unique
def render_dashboard(input_df, model, key_suffix):
    # 1. PREDICT
    prediction_idx = model.predict(input_df)[0]
    probs = model.predict_proba(input_df)[0]
    
    labels = {0: "SAFE", 1: "MIRAI FLOOD", 2: "BASHLITE FLOOD", 3: "RECON SCAN"}
    label_color = {0: "#00FF00", 1: "#FF0000", 2: "#FF4500", 3: "#FFA500"}
    
    current_label = labels[prediction_idx]
    current_color = label_color[prediction_idx]
    confidence = np.max(probs) * 100
    
    # Update History for Charts
    packet_weight = input_df['MI_dir_L5_weight'].values[0]
    
    # Keep only last 50 points
    if len(st.session_state['history_volume']) > 50:
        st.session_state['history_volume'].pop(0)
        st.session_state['history_threat'].pop(0)
        
    st.session_state['history_volume'].append(packet_weight)
    st.session_state['history_threat'].append(confidence if prediction_idx != 0 else 0)

    # --- ROW 1: HEADS UP DISPLAY (KPIs) ---
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    with kpi1:
        st.markdown(f"<div class='metric-card'><h2 style='color:{current_color}'>{current_label}</h2><p>Threat Status</p></div>", unsafe_allow_html=True)
    with kpi2:
        st.metric("Model Confidence", f"{confidence:.1f}%", delta_color="off")
    with kpi3:
        st.metric("Packet Volume (L5)", f"{packet_weight:.2f}")
    with kpi4:
        # Simple Logic: High variance often means irregular/human traffic, Low variance means bot
        jitter = input_df['HH_jit_L5_mean'].values[0]
        st.metric("Jitter (Variance)", f"{jitter:.9f}")

    # --- ROW 2: LIVE GRAPHS ---
    st.divider()
    g1, g2 = st.columns([2, 1])

    with g1:
        st.subheader("📡 Network Traffic Pulse (Real-Time)")
        # Plotly Line Chart
        fig_vol = go.Figure()
        fig_vol.add_trace(go.Scatter(y=st.session_state['history_volume'], mode='lines', name='Packet Volume', line=dict(color='#00CCFF')))
        fig_vol.update_layout(height=300, margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        
        # FIX: Added unique key
        st.plotly_chart(fig_vol, use_container_width=True, key=f"vol_chart_{key_suffix}")

    with g2:
        st.subheader("🎯 Threat Probability")
        # Plotly Bar Chart
        class_names = ['Benign', 'Mirai', 'Bashlite', 'Scan']
        fig_bar = px.bar(x=class_names, y=probs, color=class_names, 
                         color_discrete_map={'Benign': 'green', 'Mirai': 'red', 'Bashlite': 'orange', 'Scan': 'yellow'})
        fig_bar.update_layout(height=300, showlegend=False, margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        
        # FIX: Added unique key
        st.plotly_chart(fig_bar, use_container_width=True, key=f"bar_chart_{key_suffix}")

    # --- ROW 3: DEEP DIVE ---
    with st.expander("🔍 Inspect Packet Features (Forensics)"):
        st.dataframe(input_df)


# --- SIDEBAR CONTROL ---
st.sidebar.header("🕹️ Simulation Control")
mode = st.sidebar.radio("Mode", ["Manual Analysis", "Auto-Pilot (Live)"])

if mode == "Manual Analysis":
    t_type = st.sidebar.selectbox("Inject Traffic", ["Normal", "Mirai", "Bashlite", "Scan"])
    idx = st.sidebar.slider("Packet Index", 0, 199, 0)
    
    if t_type == "Normal": data = d_benign.iloc[[idx]]
    elif t_type == "Mirai": data = d_mirai.iloc[[idx]]
    elif t_type == "Bashlite": data = d_bashlite.iloc[[idx]]
    else: data = d_scan.iloc[[idx]]
    
    # Pass a static key for manual mode
    render_dashboard(data, model, "manual")

else: # LIVE MODE
    st.sidebar.write("---")
    speed = st.sidebar.slider("Refresh Speed (s)", 0.1, 2.0, 0.2)
    
    if st.sidebar.button("▶️ START MONITORING"):
        # Create a randomized stream
        stream_pool = pd.concat([d_benign.head(50), d_mirai.head(50), d_scan.head(50)]).sample(frac=1).reset_index(drop=True)
        placeholder = st.empty()
        
        for i in range(len(stream_pool)):
            with placeholder.container():
                # FIX: Pass 'i' (loop index) as the unique key suffix
                render_dashboard(stream_pool.iloc[[i]], model, i)
                time.sleep(speed)