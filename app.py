import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
from datetime import datetime
import time
import os
import re

# ─── 1. CONFIGURATION & STYLING ───────────────────────────────────────
st.set_page_config(page_title="EvoMem: Adaptive Memory Evolution Framework", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    .metric-card { background-color: #1E1E1E; border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); border-left: 5px solid #BB86FC; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; font-size: 16px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

DB_NAME = "evomem_research.db"

# ─── 2. DATABASE ENGINE (Phases 1 & 4) ────────────────────────────────
def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            memory_type TEXT DEFAULT "general",
            importance REAL DEFAULT 1.0,
            emotional_salience REAL DEFAULT 0.0,
            status TEXT DEFAULT "ACTIVE",
            access_count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    return conn

# ─── 3. COGNITIVE ENGINE (Phases 2 & 3) ───────────────────────────────
def analyze_emotional_salience(text):
    """Novel Mechanism: Emotional Salience Weighting"""
    text_lower = text.lower()
    high_emotion_words = ['love', 'hate', 'furious', 'thrilled', 'terrified', 'critical']
    salience = 0.5 # Baseline
    if any(word in text_lower for word in high_emotion_words):
        salience += 0.4
    return min(salience, 1.0)

def detect_contradiction(conn, new_text):
    """Novel Mechanism: Contradiction Resolution Engine"""
    df = pd.read_sql_query("SELECT id, text FROM memories WHERE status = 'ACTIVE'", conn)
    new_text_lower = new_text.lower()
    
    # Simple semantic conflict mock for demonstration
    if "hate python" in new_text_lower:
        conflict = df[df['text'].str.contains("prefer python|love python", case=False)]
        if not conflict.empty:
            return conflict.iloc[0]['id'], conflict.iloc[0]['text']
    return None, None

def extract_and_store(conn, message):
    """Phase 1: Basic Extraction & Storage"""
    extracted = []
    msg_lower = message.lower()
    salience = analyze_emotional_salience(message)
    
    # Emotional impact directly scales importance (Phase 2)
    base_importance = 1.0 + (salience * 2)

    if "my name is" in msg_lower:
        name = msg_lower.split("my name is")[1].split()[0].capitalize()
        extracted.append((f"User's name: {name}", "personal", base_importance + 1.0, salience))
    if any(kw in msg_lower for kw in ["prefer", "hate", "love"]):
        extracted.append((f"Preference: {message}", "preference", base_importance, salience))
    if "project" in msg_lower:
        extracted.append((f"Project focus: {message}", "project", base_importance + 1.5, salience))

    for ex in extracted:
        conflict_id, conflict_text = detect_contradiction(conn, ex[0])
        if conflict_id:
            st.warning(f"⚠️ **Contradiction Detected!** You previously said: '{conflict_text}'. Resolving and versioning memory...")
            conn.execute("UPDATE memories SET status = 'SUPERSEDED' WHERE id = ?", (conflict_id,))
        
        conn.execute(
            "INSERT INTO memories (text, memory_type, importance, emotional_salience) VALUES (?, ?, ?, ?)",
            ex
        )
    conn.commit()
    return extracted

# ─── 4. CONSOLIDATION ENGINE (Phase 4) ────────────────────────────────
def run_idle_consolidation(conn):
    """Novel Mechanism: Idle-State Memory Consolidation"""
    df = pd.read_sql_query("SELECT * FROM memories WHERE status = 'ACTIVE'", conn)
    if len(df) > 3:
        # Simulate background task archiving low-salience trivialities
        low_value = df[df['importance'] < 1.5]
        for _, row in low_value.iterrows():
            conn.execute("UPDATE memories SET status = 'ARCHIVED' WHERE id = ?", (row['id'],))
        conn.commit()
        return len(low_value)
    return 0

# ─── 5. UI DASHBOARD (Phase 6) ────────────────────────────────────────
st.title("🧠 EvoMem: Long-Term AI Agent Framework")
st.caption("Developed by Sarthak & Rajas | Implementing Smart India Hackathon Architecture")

with st.sidebar:
    st.header("⚙️ Agent Settings")
    st.text_input("LLM API Key (OpenAI/Gemini)", type="password")
    
    st.markdown("### Background Processes")
    if st.button("Trigger Idle Consolidation 💤"):
        conn = get_db()
        archived_count = run_idle_consolidation(conn)
        st.success(f"Consolidation complete. {archived_count} trivial memories archived.")
        
    if st.button("Wipe Global State"):
        if os.path.exists(DB_NAME): os.remove(DB_NAME)
        st.rerun()

tab1, tab2, tab3 = st.tabs(["💬 Interaction Interface", "🕸️ Temporal Knowledge Graph", "📊 System Analytics"])

with tab1:
    st.subheader("Agent Interaction & Conflict Resolution Sandbox")
    st.markdown("Try triggering emotional salience (`I am thrilled about this`) or contradictions (`I love Python` followed by `I hate Python`).")
    
    user_input = st.chat_input("Communicate with the agent...")
    if user_input:
        st.chat_message("user").write(user_input)
        conn = get_db()
        extracted = extract_and_store(conn, user_input)
        
        with st.chat_message("assistant"):
            if extracted:
                st.write(f"I have successfully encoded {len(extracted)} new episodic nodes.")
            else:
                st.write("I am tracking your input, though it fell below the cognitive retention threshold.")

with tab2:
    st.subheader("Novel Mechanism: Temporal Knowledge Graph")
    st.caption("Visualizing relational edges based on time and semantic categories rather than isolated vectors.")
    conn = get_db()
    df = pd.read_sql_query("SELECT * FROM memories", conn)
    
    if not df.empty:
        G = nx.Graph()
        G.add_node("Agent Core", size=20, color='red')
        
        for _, row in df.iterrows():
            G.add_node(row['id'], label=row['text'][:20]+"...", size=row['importance']*10, color='lightblue')
            G.add_edge("Agent Core", row['id'])
            
        pos = nx.spring_layout(G)
        
        edge_x, edge_y = [], []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]; x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
            
        edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=1, color='#888'), hoverinfo='none', mode='lines')
        
        node_x = [pos[node][0] for node in G.nodes()]
        node_y = [pos[node][1] for node in G.nodes()]
        node_sizes = [G.nodes[node].get('size', 10) for node in G.nodes()]
        node_colors = [G.nodes[node].get('color', 'blue') for node in G.nodes()]
        
        node_trace = go.Scatter(
            x=node_x, y=node_y, mode='markers+text',
            hoverinfo='text', marker=dict(showscale=False, color=node_colors, size=node_sizes),
            text=[G.nodes[node].get('label', 'Core') for node in G.nodes()], textposition="top center"
        )
        
        fig = go.Figure(data=[edge_trace, node_trace], layout=go.Layout(
            showlegend=False, hovermode='closest', margin=dict(b=0,l=0,r=0,t=0),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
        ))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Graph will generate once semantic nodes are established in the interaction interface.")

with tab3:
    st.subheader("Phase 6: Evaluation Metrics")
    if not df.empty:
        c1, c2, c3 = st.columns(3)
        c1.markdown(f"<div class='metric-card'><h4>Total Active Nodes</h4><h2>{len(df[df['status']=='ACTIVE'])}</h2></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='metric-card'><h4>Avg Salience</h4><h2>{df['emotional_salience'].mean():.2f}</h2></div>", unsafe_allow_html=True)
        c3.markdown(f"<div class='metric-card'><h4>Superseded (Conflicts)</h4><h2>{len(df[df['status']=='SUPERSEDED'])}</h2></div>", unsafe_allow_html=True)
        
        st.write("---")
        st.dataframe(df[['id', 'text', 'memory_type', 'emotional_salience', 'status']], use_container_width=True, hide_index=True)
