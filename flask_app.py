from flask import Flask
import datetime as dt
import html
import platform
import socket
import subprocess

app = Flask(__name__)


def _run(cmd: list[str], timeout: int = 6) -> str:
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, timeout=timeout, text=True)
        return out.strip() or "(no output)"
    except Exception as e:
        return f"Error: {e}"


@app.get('/')
def dashboard():
    now = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    host = socket.gethostname()
    pyver = platform.python_version()
    os_name = f"{platform.system()} {platform.release()}"

    openclaw_status = _run(["openclaw", "status"])

    return f"""
<!doctype html>
<html lang='ru'>
<head>
  <meta charset='utf-8'>
  <meta name='viewport' content='width=device-width, initial-scale=1'>
  <title>OpenClaw Status</title>
  <style>
    body {{ font-family: Inter, Arial, sans-serif; margin: 24px; background:#0f172a; color:#e2e8f0; }}
    .card {{ background:#111827; border:1px solid #334155; border-radius:12px; padding:16px; margin-bottom:16px; }}
    h1 {{ margin-top:0; }}
    .muted {{ color:#94a3b8; }}
    pre {{ white-space: pre-wrap; background:#020617; padding:12px; border-radius:8px; overflow:auto; }}
  </style>
</head>
<body>
  <div class='card'>
    <h1>🚀 OpenClaw Dashboard</h1>
    <p><b>Сообщение:</b> Девелы Петбай Максим, новым плодим и готовимся!</p>
    <p class='muted'>Обновлено: {html.escape(now)}</p>
    <ul>
      <li><b>Host:</b> {html.escape(host)}</li>
      <li><b>OS:</b> {html.escape(os_name)}</li>
      <li><b>Python:</b> {html.escape(pyver)}</li>
    </ul>
  </div>

  <div class='card'>
    <h2>Служебная статистика OpenClaw</h2>
    <pre>{html.escape(openclaw_status)}</pre>
  </div>
</body>
</html>
"""


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
