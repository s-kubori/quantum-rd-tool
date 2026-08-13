import streamlit as st
import pandas as pd
from utils.db import get_experiments

st.title("📊 Experiment Log")
st.caption("Lists past experiment results")

st.divider()

# Get experiment logs
experiments = get_experiments()

if not experiments:
    st.warning("No experiments yet. Run a VQE computation on the Quantum Computation page.")
else:
    st.subheader(f"{len(experiments)} experiments")

    # Formatting for table display
    rows = []
    for exp in experiments:
        result = exp["result"] or {}
        rows.append({
            "ID": exp["id"],
            "Name": exp["name"],
            "Algorithm": exp["algorithm"],
            "Energy (Ha)": result.get("energy", "-"),
            "Iterations": result.get("iterations", "-"),
            "Converged": "✅" if result.get("converged") else "⚠️",
            "Run at": exp["created_at"][:19].replace("T", " ")
        })

    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True)

    st.divider()

    # Details display
    st.subheader("Details")
    exp_ids = [f"ID {e['id']}: {e['name']}" for e in experiments]
    selected = st.selectbox("Select an experiment", exp_ids)

    selected_id = int(selected.split(":")[0].replace("ID ", ""))
    selected_exp = next(e for e in experiments if e["id"] == selected_id)

    col1, col2 = st.columns(2)
    with col1:
        st.write("**Parameters**")
        st.json(selected_exp["parameters"])
    with col2:
        st.write("**Result**")
        st.json(selected_exp["result"])