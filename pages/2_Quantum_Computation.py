import streamlit as st
import matplotlib.pyplot as plt
from utils.quantum import run_vqe

st.title("⚛️ Quantum Computation")
st.caption("Computes the ground state energy of H2 with the VQE algorithm")

st.divider()

# Parameters
st.subheader("1. Parameters")

col1, col2 = st.columns(2)

with col1:
    shots = st.slider("Shots", min_value=100, max_value=5000, value=1000, step=100)

with col2:
    reps = st.slider("Circuit depth (reps)", min_value=1, max_value=3, value=1)

experiment_name = st.text_input("Experiment name", value="H2 VQE")

st.divider()

# Run VQE
st.subheader("2. Run VQE")

if st.button("Run VQE", use_container_width=True):
    with st.spinner("Running the computation (30s to 1 min)..."):
        result = run_vqe(
            shots=shots,
            reps=reps,
            experiment_name=experiment_name
        )

    # Show result
    st.success("Computation complete")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Ground state energy", f"{result['energy']} Ha")
    with col2:
        st.metric("Iterations", result["iterations"])
    with col3:
        st.metric("Converged", "✅ Yes" if result["converged"] else "⚠️ No")

    # Energy convergence graph
    if result["energy_history"]:
        st.subheader("Energy convergence")
        fig, ax = plt.subplots()
        ax.plot(result["energy_history"], marker="o", color="royalblue")
        ax.set_xlabel("Iteration")
        ax.set_ylabel("Energy (Ha)")
        ax.set_title("VQE energy convergence")
        ax.grid(True)
        st.pyplot(fig)

    st.info("The result has been saved to the experiment log.")
