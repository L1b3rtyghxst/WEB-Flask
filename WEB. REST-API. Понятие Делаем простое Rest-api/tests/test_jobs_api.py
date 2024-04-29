import datetime
import requests

BASE_URL = "http://127.0.0.1:8080"


def test_get_all_jobs():
    """получение всех работ"""
    resp = requests.get(f"{BASE_URL}/api/jobs")
    jobs = resp.json()["jobs"]
    assert "is_finished" in jobs[-1]


def test_get_job():
    """получение одной работы"""
    resp = requests.get(f"{BASE_URL}/api/jobs/1")
    job = resp.json()["jobs"][0]
    assert "is_finished" in job


def test_wrong_get_job():
    """получение несуществующей работы"""
    resp = requests.get(f"{BASE_URL}/api/jobs/0")
    assert resp.status_code == 404 and "Not Found" in resp.json()["error"]


def test_wrong_type_get_job():
    """Получение работы с неверным типом id"""
    resp = requests.get(f"{BASE_URL}/api/jobs/string")
    assert resp.status_code == 404 and "Not Found" in resp.json()["error"]


def test_job_post_empty():
    """пустой запрос"""
    data = {}
    resp = requests.post(f"{BASE_URL}/api/jobs", json=data)
    assert resp.status_code == 400 and "Empty request" in resp.json()["error"]


def test_job_post_with_missing_fields():
    """Поле is_finished отсутсвует"""
    data = {
        "id": 1,
        "team_leader_id": 4,
        "job": "Working hard",
        "work_size": 100,
        "collaborators": "1, 2, 3",
        "start_date": datetime.datetime.now().isoformat(),
    }
    resp = requests.post(f"{BASE_URL}/api/jobs", json=data)
    assert resp.status_code == 400 and "Missing fields" in resp.json()["error"]


def test_job_post_with_existing_id():
    """существующая работа"""
    data = {
        "id": 1,
        "team_leader_id": 4,
        "job": "Working hard",
        "work_size": 100,
        "collaborators": "1, 2, 3",
        "start_date": datetime.datetime.now().isoformat(),
        "end_date": None,
        "is_finished": False
    }
    resp = requests.post(f"{BASE_URL}/api/jobs", json=data)
    assert resp.status_code == 400 and "Id already exists" in resp.json()["error"]


def test_job_post():
    """создание работы"""
    job_id = 10
    data = {
        "id": job_id,
        "team_leader_id": 4,
        "job": "Working hard",
        "work_size": 100,
        "collaborators": "1, 2, 3",
        "start_date": datetime.datetime.now().isoformat(),
        "end_date": None,
        "is_finished": False
    }
    resp = requests.post(f"{BASE_URL}/api/jobs", json=data)
    resp.raise_for_status()
    resp = requests.get(f"{BASE_URL}/api/jobs/{job_id}")
    jobs = resp.json()["jobs"]
    assert jobs[0]["job"] == "Working hard"


def test_missing_job_delete():
    """удаление несуществующей работы"""
    job_id = 0
    resp = requests.delete(f"{BASE_URL}/api/jobs/{job_id}")  # несуществующая работа
    assert resp.status_code == 404 and "Not Found" in resp.json()["error"]


def test_wrong_type_delete_job():
    """удаление работы с неверным типом id"""
    resp = requests.delete(f"{BASE_URL}/api/jobs/string")
    assert resp.status_code == 404 and "Not Found" in resp.json()["error"]


def test_job_delete():
    """удаление работы"""
    job_id = 1
    resp = requests.delete(f"{BASE_URL}/api/jobs/{job_id}")
    resp.raise_for_status()
    resp = requests.get(f"{BASE_URL}/api/jobs/{job_id}")  # проверяем что такой работы уже нет
    assert resp.status_code == 404 and "Not Found" in resp.json()["error"]


def test_missing_job_edit():
    """удаление несуществующей работы"""
    job_id = 0
    resp = requests.put(f"{BASE_URL}/api/jobs/{job_id}")  # несуществующая работа
    assert resp.status_code == 404 and "Not Found" in resp.json()["error"]


def test_wrong_type_edit_job():
    """редактирование работы с неверным типом id"""
    resp = requests.put(f"{BASE_URL}/api/jobs/string")
    assert resp.status_code == 404 and "Not Found" in resp.json()["error"]


def test_job_edit():
    """редактирование работы"""
    job_id = 2
    data = {
        "id": 2,
        "team_leader_id": 4,
        "job": "Working hard",
        "work_size": 100,
        "collaborators": "1, 2, 3",
        "start_date": datetime.datetime.now().isoformat(),
        "end_date": None,
        "is_finished": False
    }
    resp = requests.put(f"{BASE_URL}/api/jobs/{job_id}", json=data)
    resp.raise_for_status()
    resp = requests.get(f"{BASE_URL}/api/jobs/{job_id}")
    resp.raise_for_status()
    job = resp.json()["jobs"][0]
    assert job["job"] == "Working hard"
