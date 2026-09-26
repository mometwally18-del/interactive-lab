import platform
import subprocess
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Interactive Lab Engine API")

# الخريطة الخاصة بالتجارب (Telemetry Map)
TELEMETRY_MAP = {
    # يمكنك إضافة الـ Techniques الخاصة بك هنا
}


class LabRunRequest(BaseModel):
  technique_id: str
  test_number: int


@app.get('/')
def home():
  return {
      'status': 'success',
      'message': 'Interactive Lab Engine is Running',
  }


@app.post('/api/v1/run-lab')
def run_lab(data: LabRunRequest):
  # أمر Atomic Test
  cmd = f"Invoke-AtomicTest {data.technique_id} -TestNumbers {data.test_number} -Confirm:$False"

  try:
    # التحقق من نظام التشغيل لمنع خطأ سيرفرات لينكس (Vercel)
    if platform.system() == 'Windows':
      shell_cmd = ['powershell', '-Command', cmd]
    else:
      # على سحابة Vercel (Linux)، نرجع رد تجريبي آمن لمنع توقف السيرفر
      return {
          'status': 'simulated',
          'technique_id': data.technique_id,
          'output': (
              'Atomic Tests execution requires a local Windows environment with'
              ' PowerShell.'
          ),
          'expected_event_ids': TELEMETRY_MAP.get(data.technique_id, [1]),
      }

    execution = subprocess.run(
        shell_cmd, capture_output=True, text=True, timeout=30
    )

  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))

  return {
      'status': 'executed',
      'technique_id': data.technique_id,
      'output': execution.stdout if execution.stdout else execution.stderr,
      'expected_event_ids': TELEMETRY_MAP.get(data.technique_id, [1]),
  }