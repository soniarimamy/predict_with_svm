import requests
from temporalio import activity

API_URL = "http://127.0.0.1:8000"

@activity.defn
async def call_predict(mot: str):
    response = requests.post(f"{API_URL}/predict", json={"mot": mot})
    return response.json()


@activity.defn
async def call_perf():
    response = requests.get(f"{API_URL}/show_perf_as_number")
    return response.json()
