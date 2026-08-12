import pytest

from utils import db, quantum


def test_hamiltonian_shape():
    """H2 Hamiltonian is a 5-term, 2-qubit operator."""
    assert quantum.H2_HAMILTONIAN.num_qubits == 2
    assert len(quantum.H2_HAMILTONIAN) == 5


def test_default_ansatz_matches_hamiltonian_qubits():
    """run_vqe() relies on build_ansatz() defaults lining up with the Hamiltonian."""
    ansatz = quantum.build_ansatz()
    assert ansatz.num_qubits == quantum.H2_HAMILTONIAN.num_qubits


def test_build_ansatz_parameter_count_grows_with_reps():
    """TwoLocal with ry+rz rotations gains parameters as reps increase."""
    one_rep = quantum.build_ansatz(num_qubits=2, reps=1).num_parameters
    two_reps = quantum.build_ansatz(num_qubits=2, reps=2).num_parameters
    assert one_rep > 0
    assert two_reps > one_rep


@pytest.mark.slow
def test_run_vqe_converges_to_h2_ground_state(temp_db):
    """VQE should land near the known H2 ground state energy (~-1.857 Ha)."""
    outcome = quantum.run_vqe(reps=1, experiment_name="pytest H2 VQE")

    assert outcome["energy"] == pytest.approx(-1.857, abs=0.02)
    assert outcome["iterations"] > 0
    assert len(outcome["energy_history"]) <= 10


@pytest.mark.slow
def test_run_vqe_persists_experiment(temp_db):
    quantum.run_vqe(reps=1, experiment_name="pytest persistence check")

    experiments = db.get_experiments()
    assert len(experiments) == 1
    assert experiments[0]["name"] == "pytest persistence check"
    assert experiments[0]["algorithm"] == "VQE"
