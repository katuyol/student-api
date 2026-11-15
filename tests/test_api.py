import importlib

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("DB_PATH", str(tmp_path / "test.db"))
    import app.database as database
    importlib.reload(database)
    import app.controllers as controllers
    importlib.reload(controllers)
    import app.main as main
    importlib.reload(main)
    import migrate.migrate as mig
    importlib.reload(mig)
    mig.migrate()
    with TestClient(main.app) as c:
        yield c


def test_migrated_data_is_served(client):
    data = client.get("/students").json()
    assert len(data) == 5 and data[0]["name"] == "Zainab"


def test_create_and_validate(client):
    ok = client.post("/students", json={"name": "Tola", "score": 77})
    assert ok.status_code == 201 and ok.json()["grade"] == "A"
    assert client.post("/students", json={"name": "Bad", "score": 150}).status_code == 422


def test_stats_and_delete(client):
    assert client.get("/stats").json()["count"] == 5
    assert client.delete("/students/1").status_code == 204
    assert client.get("/students/1").status_code == 404
