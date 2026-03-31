import os

import httpx

PEER_BASE_URL = os.getenv("PEER_BASE_URL")


def replicate_create_task(task_id: str, title: str, description: str | None) -> None:
    if not PEER_BASE_URL:
        return

    url = f"{PEER_BASE_URL}/internal/tasks"

    payload = {
        "task_id": task_id,
        "title": title,
        "description": description,
        "deleted": False,
    }

    try:
        response = httpx.post(url, json=payload, timeout=5.0)
        response.raise_for_status()
    except Exception as e:
        print("Replication create failed:", e)


def replicate_delete_task(task_id: str) -> None:
    if not PEER_BASE_URL:
        return

    url = f"{PEER_BASE_URL}/internal/tasks/delete"

    payload = {
        "task_id": task_id,
    }

    try:
        response = httpx.post(url, json=payload, timeout=5.0)
        response.raise_for_status()
    except Exception as e:
        print("Replication delete failed:", e)