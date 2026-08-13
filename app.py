import streamlit as st

st.set_page_config(
    page_title="量子研究開発ツール",
    page_icon="⚛️",
    layout="wide"
)

st.title("⚛️ 量子研究開発ツール")
st.caption("RAG論文検索 × 量子計算 × 実験ログ管理")

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("📄 RAG論文検索")
    st.write("arXivから論文を取得しClaudeが回答します")
    if st.button("論文検索へ", use_container_width=True):
        st.switch_page("pages/1_RAG_Search.py")

with col2:
    st.subheader("⚛️ 量子計算")
    st.write("VQEアルゴリズムで量子化学計算を実行します")
    if st.button("量子計算へ", use_container_width=True):
        st.switch_page("pages/2_Quantum_Computation.py")

with col3:
    st.subheader("📊 実験ログ")
    st.write("過去の実験結果を一覧で確認できます")
    if st.button("実験ログへ", use_container_width=True):
        st.switch_page("pages/3_Experiment_Log.py")