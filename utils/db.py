import sqlite3
import json
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "data" / "experiments.db"


def init_db():
    """DBとテーブルを初期化する"""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS experiments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            algorithm TEXT NOT NULL,
            parameters TEXT NOT NULL,
            result TEXT,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def save_experiment(name: str, algorithm: str, parameters: dict, result: dict):
    """実験結果を保存する"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO experiments (name, algorithm, parameters, result, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (
        name,
        algorithm,
        json.dumps(parameters),
        json.dumps(result),
        datetime.now().isoformat()
    ))
    conn.commit()
    conn.close()


def get_experiments():
    """全実験結果を取得する"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM experiments ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()

    experiments = []
    for row in rows:
        experiments.append({
            "id": row[0],
            "name": row[1],
            "algorithm": row[2],
            "parameters": json.loads(row[3]),
            "result": json.loads(row[4]) if row[4] else None,
            "created_at": row[5]
        })
    return experiments