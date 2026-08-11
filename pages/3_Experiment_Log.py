import streamlit as st
import pandas as pd
from utils.db import get_experiments

st.title("📊 実験ログ")
st.caption("過去の実験結果を一覧で確認できます")

st.divider()

# 実験ログ取得
experiments = get_experiments()

if not experiments:
    st.warning("まだ実験データがありません。量子計算ページでVQEを実行してください。")
else:
    st.subheader(f"実験数：{len(experiments)} 件")

    # テーブル表示用に整形
    rows = []
    for exp in experiments:
        result = exp["result"] or {}
        rows.append({
            "ID": exp["id"],
            "実験名": exp["name"],
            "アルゴリズム": exp["algorithm"],
            "エネルギー (Ha)": result.get("energy", "-"),
            "最適化回数": result.get("iterations", "-"),
            "収束": "✅" if result.get("converged") else "⚠️",
            "実行日時": exp["created_at"][:19].replace("T", " ")
        })

    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True)

    st.divider()

    # 詳細表示
    st.subheader("実験の詳細")
    exp_ids = [f"ID {e['id']}：{e['name']}" for e in experiments]
    selected = st.selectbox("実験を選択", exp_ids)

    selected_id = int(selected.split("：")[0].replace("ID ", ""))
    selected_exp = next(e for e in experiments if e["id"] == selected_id)

    col1, col2 = st.columns(2)
    with col1:
        st.write("**パラメータ**")
        st.json(selected_exp["parameters"])
    with col2:
        st.write("**結果**")
        st.json(selected_exp["result"])