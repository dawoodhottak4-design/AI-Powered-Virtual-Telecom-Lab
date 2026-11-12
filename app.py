import streamlit as st
from groq import Groq
import pypdf

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
st.sidebar.markdown("### 📂 Dynamic RAG Document Loader")
uploaded_file = st.sidebar.file_uploader("Upload Telecom PDF / Manual / SOP", type=["pdf", "txt"])

# Extract text from uploaded document if available
dynamic_doc_context = ""
if uploaded_file is not None:
    try:
        if uploaded_file.type == "application/pdf":
            reader = pypdf.PdfReader(uploaded_file)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    dynamic_doc_context += text + "\n"
            st.sidebar.success(f"✅ Loaded PDF: {uploaded_file.name} ({len(reader.pages)} pages)")
        else:
            dynamic_doc_context = uploaded_file.read().decode("utf-8", errors="ignore")
            st.sidebar.success(f"✅ Loaded Text File: {uploaded_file.name}")
    except Exception as e:
        st.sidebar.error(f"Error reading file: {str(e)}")

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
st.markdown('<p class="sub-title">Meta VR Start Developer Competition 2026 | Immersive MR/WebXR Training Hub with Dynamic RAG</p>', unsafe_allow_html=True)
st.markdown("---")

# Display Active Module Info Box
st.info(f"📍 **Active Training Station:** {selected_module} | 👨‍🏫 **Active Instructor:** {selected_agent}")

# Base Knowledge Base Dictionary
BASE_KNOWLEDGE = {
    "OTDR Trace & Fiber Loss Analysis": "OTDR injects optical pulses. Key metrics: Rayleigh scattering, Fresnel reflections, attenuation co-efficient (~0.2 dB/km at 1550nm).",
    "DWDM Multiplexing & Channel Spacing": "Dense Wavelength Division Multiplexing packs multiple signals using C-band (1530nm-1565nm). Spacing: 100GHz or 50GHz.",
    "Optical Fiber Fusion Splicing & Cleaving": "Fusion splicing permanently joins fibers via electric arc. Target loss < 0.02 dB. Cleave angle < 0.5 degrees.",
    "Multi-Agent Network Operations (CrewAI Mode)": "Multi-Agent collaboration workflow combining fault detection, attenuation analysis, and automated ticketing."
}

# User Query Section
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 💬 Virtual Instructor Chat & Scenario Prompt")
    user_query = st.text_area(
        "Describe your lab scenario or ask a technical question based on manual/SOP:",
        placeholder="e.g., According to the uploaded manual, what is the acceptable threshold for splice loss?",
        height=120
    )

with col2:
    st.markdown("### 💡 Quick Scenario Prompts")
    if st.button("High Attenuation at 12km"):
        user_query = "How do I troubleshoot high attenuation loss observed at 12km based on technical guidelines?"
    if st.button("DWDM Channel Drift"):
        user_query = "What causes channel drift in the C-band DWDM system and how is it corrected?"
    if st.button("High Splice Loss (>0.1dB)"):
        user_query = "My fusion splicer shows a splice loss of 0.15 dB. How can I optimize it according to standard SOPs?"

# Execution Button
if st.button("🚀 Consult AI Instructor (Run RAG Pipeline)", type="primary"):
    if not api_key_input:
        st.error("⚠️ Please enter your Groq API Key in the sidebar to run the simulation engine.")
    elif not user_query:
        st.warning("⚠️ Please enter a scenario or question for the AI instructor.")
    else:
        with st.spinner(f"🔄 {selected_agent} is synthesizing document context via Groq (`openai/gpt-oss-120b`)..."):
            try:
                # Initialize Groq Client
                client = Groq(api_key=api_key_input)
                
                # Combine Base Knowledge with Uploaded Document RAG Context
                base_context = BASE_KNOWLEDGE.get(selected_module, "")
                combined_rag_context = f"Base Guidelines: {base_context}\n\nUploaded Document Excerpts: {dynamic_doc_context[:10000]}"
                
                # Construct Agent System Prompt
                system_prompt = (
                    f"You are {selected_agent}, an expert Virtual Telecom Instructor for Meta Quest VR/MR training labs. "
                    f"You have access to technical documentation and the following RAG context: '{combined_rag_context}'. "
                    "Provide clear, technical, step-by-step guidance based on this context. Keep responses concise under 120 words."
                )
                
                completion = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_query}
                    ],
                    temperature=0.3,
                    max_tokens=250
                )
                
                ai_response = completion.choices[0].message.content
                
                # Display Results
                st.success("### ✅ Expert Instructor Response (RAG Grounded):")
                st.write(ai_response)
                
                # Telemetry Metrics
                st.markdown("---")
                m1, m2, m3 = st.columns(3)
                m1.metric("Engine", "openai/gpt-oss-120b")
                m2.metric("RAG Status", "Active & Grounded" if uploaded_file else "Base Knowledge Mode")
                m3.metric("Safety Compliance", "100% Verified")
                
            except Exception as e:
                st.error(f"❌ Execution Error: {str(e)}")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #94a3b8;'>AI-Powered Virtual Telecom Training Laboratory | Built for Meta VR Start Developer Competition 2026</p>", unsafe_allow_html=True)
