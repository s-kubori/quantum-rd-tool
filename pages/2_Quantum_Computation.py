import streamlit as st
import matplotlib
matplotlib.rcParams['font.family'] = 'MS Gothic'
import matplotlib.pyplot as plt
from utils.quantum import run_vqe

st.title("⚛️ 量子計算")
st.caption("VQEアルゴリズムで水素分子のエネルギーを計算します")

st.divider()

# パラメータ設定
st.subheader("① パラメータ設定")

col1, col2 = st.columns(2)

with col1:
    shots = st.slider("ショット数", min_value=100, max_value=5000, value=1000, step=100)

with col2:
    reps = st.slider("回路の深さ（reps）", min_value=1, max_value=3, value=1)

experiment_name = st.text_input("実験名", value="H2 VQE実験")

st.divider()

# VQE実行
st.subheader("② VQE実行")

if st.button("VQEを実行", use_container_width=True):
    with st.spinner("量子計算中...（30秒〜1分かかります）"):
        result = run_vqe(
            shots=shots,
            reps=reps,
            experiment_name=experiment_name
        )

    # 結果表示
    st.success("計算完了！")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("基底状態エネルギー", f"{result['energy']} Ha")
    with col2:
        st.metric("最適化回数", f"{result['iterations']} 回")
    with col3:
        st.metric("収束", "✅ Yes" if result["converged"] else "⚠️ No")

    # エネルギー収束グラフ
    if result["energy_history"]:
        st.subheader("エネルギー収束グラフ")
        fig, ax = plt.subplots()
        ax.plot(result["energy_history"], marker="o", color="royalblue")
        ax.set_xlabel("繰り返し回数")
        ax.set_ylabel("エネルギー (Ha)")
        ax.set_title("VQEエネルギー収束")
        ax.grid(True)
        st.pyplot(fig)

    st.info("結果は実験ログに自動保存されました！")