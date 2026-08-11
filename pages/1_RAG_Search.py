import streamlit as st
from utils.rag import fetch_and_store_papers, search_and_answer

st.title("📄 RAG論文検索")
st.caption("arXivから論文を取得してClaudeが回答します")

st.divider()

# 論文取得セクション
st.subheader("① 論文を取得する")
query = st.text_input("検索キーワード（英語）", value="quantum computing")
max_results = st.slider("取得件数", min_value=1, max_value=10, value=5)

if st.button("論文を取得", use_container_width=True):
    with st.spinner("arXivから取得中..."):
        papers = fetch_and_store_papers(query, max_results)
    st.success(f"{len(papers)}件取得しました！")
    for title in papers:
        st.write(f"・{title}")

st.divider()

# 質問セクション
st.subheader("② 質問する")
question = st.text_input("質問（日本語OK）", value="量子コンピューティングとは何ですか？")

if st.button("AIに質問", use_container_width=True):
    with st.spinner("Claudeが回答中..."):
        result = search_and_answer(question)

    if isinstance(result, str):
        st.warning(result)
    else:
        st.subheader("回答")
        st.write(result["answer"])
        st.subheader("参照論文")
        for title in result["sources"]:
            st.write(f"・{title}")