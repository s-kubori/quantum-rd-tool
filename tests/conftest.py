import pytest

from utils import db


@pytest.fixture
def temp_db(tmp_path, monkeypatch):
    """Point db.DB_PATH at a throwaway file so tests never touch data/experiments.db.

    Returns the path so tests can inspect the database directly if needed.
    """
    path = tmp_path / "test_experiments.db"
    monkeypatch.setattr(db, "DB_PATH", str(path))
    db.init_db()
    return path
