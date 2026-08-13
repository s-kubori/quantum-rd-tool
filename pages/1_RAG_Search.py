import streamlit as st
from utils.rag import fetch_and_store_papers, search_and_answer

st.title("📄 RAG Paper Search")
st.caption("Fetches papers from arXiv and answers questions with Claude")

st.divider()

# Paper retrieval section
st.subheader("1. Fetch papers")
query = st.text_input("Search keywords", value="quantum computing")
max_results = st.slider("Number of papers", min_value=1, max_value=10, value=5)

if st.button("Fetch papers", use_container_width=True):
    with st.spinner("Fetching from arXiv..."):
        papers = fetch_and_store_papers(query, max_results)
    st.success(f"Fetched {len(papers)} papers.")
    for title in papers:
        st.write(f"- {title}")

st.divider()

# Question section
st.subheader("2. Ask a question")
question = st.text_input("Question", value="What is quantum computing?")

if st.button("Ask Claude", use_container_width=True):
    with st.spinner("Waiting for Claude..."):
        result = search_and_answer(question)

    if isinstance(result, str):
        st.warning(result)
    else:
        st.subheader("Answer")
        st.write(result["answer"])
        st.subheader("Sources")
        for title in result["sources"]:
            st.write(f"- {title}")
