import streamlit as st

st.set_page_config(
    page_title="Quantum R&D Tool",
    page_icon="⚛️",
    layout="wide"
)

st.title("⚛️ Quantum R&D Tool")
st.caption("RAG paper search | quantum computation | experiment logging")

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("📄 RAG Paper Search")
    st.write("Fetches papers from arXiv and answers questions with Claude")
    if st.button("Go to paper search", use_container_width=True):
        st.switch_page("pages/1_RAG_Search.py")

with col2:
    st.subheader("⚛️ Quantum Computation")
    st.write("Runs quantum chemistry calculations with the VQE algorithm")
    if st.button("Go to quantum computation", use_container_width=True):
        st.switch_page("pages/2_Quantum_Computation.py")

with col3:
    st.subheader("📊 Experiment Log")
    st.write("Shows a list of past experiment results")
    if st.button("Go to experiment log", use_container_width=True):
        st.switch_page("pages/3_Experiment_Log.py")
