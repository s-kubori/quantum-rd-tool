import json
import sqlite3

from utils import db


def test_init_db_creates_table(temp_db):
    conn = sqlite3.connect(str(temp_db))
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='experiments'"
    )
    row = cursor.fetchone()
    conn.close()
    assert row is not None


def test_init_db_is_idempotent(temp_db):
    """Calling init_db twice must not raise or drop existing rows."""
    db.save_experiment("first", "VQE", {"reps": 1}, {"energy": -1.0})
    db.init_db()
    assert len(db.get_experiments()) == 1


def test_save_and_get_experiment_roundtrip(temp_db):
    parameters = {"shots": 1000, "reps": 1, "num_params": 8}
    result = {"energy": -1.857, "iterations": 134, "converged": True}

    db.save_experiment("H2 VQE", "VQE", parameters, result)
    experiments = db.get_experiments()

    assert len(experiments) == 1
    record = experiments[0]
    assert record["name"] == "H2 VQE"
    assert record["algorithm"] == "VQE"
    assert record["parameters"] == parameters
    assert record["result"] == result
    assert record["created_at"]


def test_get_experiments_returns_empty_list_when_no_rows(temp_db):
    assert db.get_experiments() == []


def test_dict_fields_are_stored_as_json(temp_db):
    """parameters/result are dicts in Python but TEXT in SQLite."""
    db.save_experiment("json check", "VQE", {"a": 1}, {"b": 2})

    conn = sqlite3.connect(str(temp_db))
    cursor = conn.cursor()
    cursor.execute("SELECT parameters, result FROM experiments")
    raw_parameters, raw_result = cursor.fetchone()
    conn.close()

    assert json.loads(raw_parameters) == {"a": 1}
    assert json.loads(raw_result) == {"b": 2}
