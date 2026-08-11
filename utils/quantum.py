import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import TwoLocal
from qiskit.quantum_info import SparsePauliOp
from qiskit_aer import AerSimulator
from qiskit.primitives import StatevectorEstimator
from scipy.optimize import minimize
from utils.db import init_db, save_experiment

# 水素分子 H2 のハミルトニアン（簡略版）
H2_HAMILTONIAN = SparsePauliOp.from_list([
    ("II", -1.0523732),
    ("IZ",  0.3979374),
    ("ZI", -0.3979374),
    ("ZZ", -0.0112801),
    ("XX",  0.1809312),
])


def build_ansatz(num_qubits: int = 2, reps: int = 1):
    """VQE用の変分量子回路（ansatz）を構築する"""
    ansatz = TwoLocal(
        num_qubits,
        rotation_blocks=["ry", "rz"],
        entanglement_blocks="cx",
        reps=reps
    )
    return ansatz


def run_vqe(shots: int = 1000, reps: int = 1, experiment_name: str = "H2 VQE"):
    """VQEを実行して基底状態エネルギーを計算する"""
    ansatz = build_ansatz(reps=reps)
    estimator = StatevectorEstimator()
    num_params = ansatz.num_parameters

    # エネルギー期待値を計算する関数
    eval_count = [0]
    energy_history = []

    def cost_function(params):
        bound = ansatz.assign_parameters(params)
        job = estimator.run([(bound, H2_HAMILTONIAN)])
        result = job.result()
        energy = result[0].data.evs.item()
        eval_count[0] += 1
        energy_history.append(energy)
        return energy

    # 初期パラメータをランダムに設定
    initial_params = np.random.uniform(-np.pi, np.pi, num_params)

    # 古典最適化（COBYLA）
    result = minimize(
        cost_function,
        initial_params,
        method="COBYLA",
        options={"maxiter": 200}
    )

    # 結果をまとめる
    outcome = {
        "energy": round(result.fun, 6),
        "iterations": eval_count[0],
        "converged": result.success,
        "energy_history": energy_history[:10]  # 最初の10件だけ保存
    }

    # DBに保存
    init_db()
    save_experiment(
        name=experiment_name,
        algorithm="VQE",
        parameters={"shots": shots, "reps": reps, "num_params": num_params},
        result=outcome
    )

    return outcome