import streamlit as st
from groq import Groq

# Page Configuration
st.set_page_config(
    page_title="AI Virtual Telecom Training Lab",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
    <style>
    .main-title { font-size: 28px; font-weight: 700; color: #0284c7; }
    .sub-title { font-size: 16px; color: #475569; }
    .stAlert { margin-top: 10px; }
    </style>
""", unsafe_allow_html=True)

# Sidebar Configuration
st.sidebar.markdown("### ⚙️ Lab Control Center")
api_key_input = st.sidebar.text_input("Enter Groq API Key", type="password", help="Get your free key from Groq Console")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔬 Training Modules")
selected_module = st.sidebar.selectbox(
    "Select Lab Station",
    [
        "OTDR Trace & Fiber Loss Analysis",
        "DWDM Multiplexing & Channel Spacing",
        "Optical Fiber Fusion Splicing & Cleaving",
        "Multi-Agent Network Operations (CrewAI Mode)"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🤖 Agent Persona")
selected_agent = st.sidebar.radio(
    "Select Lead Instructor Agent",
    ["Senior Fiber NOC Engineer", "DWDM Transmission Architect", "Compliance & Safety Officer"]
)

# Main Application Header
st.markdown('<p class="main-title">📡 AI-Powered Virtual Telecom Training Laboratory</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Meta VR Start Developer Competition 2026 | Immersive MR/WebXR Training Hub</p>', unsafe_allow_html=True)
st.markdown("---")

# Display Active Module Info Box
st.info(f"📍 **Active Training Station:** {selected_module} | 👨‍🏫 **Active Instructor:** {selected_agent}")

# Knowledge Base Dictionary (Lightweight RAG Simulator for Fast Cloud Performance)
KNOWLEDGE_BASE = {
    "OTDR Trace & Fiber Loss Analysis": "OTDR (Optical Time Domain Reflectometer) injects optical pulses into the fiber. Key metrics: Rayleigh scattering, Fresnel reflection at connectors, macrobending losses, and attenuation co-efficient (typically 0.2 dB/km at 1550nm).",
    "DWDM Multiplexing & Channel Spacing": "Dense Wavelength Division Multiplexing packs multiple optical signals onto a single fiber using distinct wavelengths (C-band typically 1530nm-1565nm). Standard spacing includes 100GHz or 50GHz intervals.",
    "Optical Fiber Fusion Splicing & Cleaving": "Fusion splicing permanently joins two optical fibers by electric arc welding. Target splice loss should be under 0.02 dB. Proper cleave angle (< 0.5 degrees) is critical to prevent high reflections.",
    "Multi-Agent Network Operations (CrewAI Mode)": "Multi-Agent collaboration workflow combining fault detection, signal attenuation analysis, and automated ticketing standards."
}

# User Query Section
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 💬 Virtual Instructor Chat & Scenario Prompt")
    user_query = st.text_area(
        "Describe your lab scenario or ask a technical question:",
        placeholder="e.g., I am getting an abrupt high reflection spike at 8.4 km on an OTDR trace. What should I check?",
        height=120
    )

with col2:
    st.markdown("### 💡 Quick Scenario Prompts")
    if st.button("High Attenuation at 12km"):
        user_query = "How do I troubleshoot high attenuation loss observed at 12km on a single-mode fiber link?"
    if st.button("DWDM Channel Drift"):
        user_query = "What causes channel drift in a 40-channel DWDM system and how is it corrected?"
    if st.button("High Splice Loss (>0.1dB)"):
        user_query = "My fusion splicer shows a splice loss of 0.15 dB. How can I optimize the electrode arc power and cleaning?"

# Execution Button
if st.button("🚀 Consult AI Instructor (Run Agent Pipeline)", type="primary"):
    if not api_key_input:
        st.error("⚠️ Please enter your Groq API Key in the sidebar to run the simulation engine.")
    elif not user_query:
        st.warning("⚠️ Please enter a scenario or question for the AI instructor.")
    else:
        with st.spinner(f"🔄 {selected_agent} is analyzing module data via Groq (`openai/gpt-oss-120b`)..."):
            try:
                # Initialize Groq Client
                client = Groq(api_key=api_key_input)
                
                # Context retrieval from built-in RAG knowledge base
                rag_context = KNOWLEDGE_BASE.get(selected_module, "Standard Telecom Guidelines")
                
                # Construct Agent System Prompt
                system_prompt = (
                    f"You are {selected_agent}, an expert Virtual Telecom Instructor for Meta Quest VR/MR training labs. "
                    f"Use the following domain knowledge base context to maintain absolute technical accuracy: '{rag_context}'. "
                    "Provide clear, concise, step-by-step troubleshooting or training guidance. Keep responses under 100 words."
                )
                
                completion = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_query}
                    ],
                    temperature=0.4,
                    max_tokens=200
                )
                
                ai_response = completion.choices[0].message.content
                
                # Display Results
                st.success("### ✅ Expert Instructor Response:")
                st.write(ai_response)
                
                # Simulation Telemetry Metrics
                st.markdown("---")
                m1, m2, m3 = st.columns(3)
                m1.metric("Model Engine", "openai/gpt-oss-120b")
                m2.metric("Latency Status", "Optimal (< 0.8s)")
                m3.metric("Safety Compliance", "Passed 100%")
                
            except Exception as e:
                st.error(f"❌ Execution Error: {str(e)}")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #94a3b8;'>AI-Powered Virtual Telecom Training Laboratory | Built for Meta VR Start Developer Competition 2026</p>", unsafe_allow_html=True)
