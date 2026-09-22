from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess

app = FastAPI(title="Interactive Lab Engine API")

# نموذج الطلب اللي هيجي من زميلك
class LabRunRequest(BaseModel):
    technique_id: str
    test_number: int = 1

# خريطة الأحداث المتوقعة للـ 22 لاب (Telemetry Mapping)
TELEMETRY_MAP = {
    "T1110.001": [4625, 4624],
    "T1110.002": [4768, 4769],
    "T1110.003": [4776, 4625],
    "T1110.004": [3, 4625],
    "T1078.001": [4722, 4738],
    "T1053.005": [4698],
    "T1543.003": [7045, 1],
    "T1547.001": [13, 11],
    "T1562.001": [5001, 1],
    "T1070.001": [1102, 104],
    "T1218": [1, 3],
    "T1218.005": [1],
    "T1003.001": [10],
    "T1003.002": [4656, 1],
    "T1555.003": [11, 1],
    "T1087.002": [1, 4104],
    "T1082": [1],
    "T1049": [1],
    "T1059.001": [4104, 1],
    "T1021.002": [5140, 1],
    "T1021.001": [4624]
}

@app.get("/")
def home():
    return {"status": "success", "message": "Interactive Lab Engine is Running"}

@app.post("/api/v1/run-lab")
def run_lab(data: LabRunRequest):
    # أمر تنفيذ الـ Atomic Test
    cmd = f"Invoke-AtomicTest {data.technique_id} -TestNumbers {data.test_number} -Confirm:$False"
    
    try:
        # تشغيل الأمر في الخلفية
        execution = subprocess.run(
            ["powershell", "-Command", cmd],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        return {
            "status": "executed",
            "technique_id": data.technique_id,
            "output": execution.stdout if execution.stdout else execution.stderr,
            "expected_event_ids": TELEMETRY_MAP.get(data.technique_id, [1])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))