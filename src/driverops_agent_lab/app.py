from __future__ import annotations

import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from driverops_agent_lab.agent import DriverOpsAgent
from driverops_agent_lab.schemas import AgentResponse, ChatRequest

app = FastAPI(title="DriverOps Agent Lab", version="0.1.0")
agent = DriverOpsAgent()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/demo", response_class=HTMLResponse)
def demo() -> str:
    return """
<!doctype html>
<html lang=\"zh-CN\">
  <head>
    <meta charset=\"utf-8\" />
    <title>DriverOps Agent Lab Demo</title>
    <style>
      body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; margin: 2rem auto; max-width: 920px; line-height: 1.5; }
      textarea { width: 100%; min-height: 100px; }
      button { padding: 0.6rem 1rem; margin-top: 0.8rem; }
      pre { background: #f6f8fa; padding: 1rem; border-radius: 8px; overflow: auto; }
      .row { display: grid; gap: 0.8rem; grid-template-columns: 1fr 1fr; }
      input { padding: 0.55rem; }
    </style>
  </head>
  <body>
    <h1>DriverOps Agent Lab Demo</h1>
    <p>输入司机问题，页面会请求 <code>/chat</code>，返回意图、建议、工具轨迹和 memory。</p>
    <div class=\"row\">
      <input id=\"driverId\" value=\"driver-001\" />
      <input id=\"city\" value=\"beijing\" />
    </div>
    <textarea id=\"query\">今天有什么活动适合我</textarea>
    <button onclick=\"runDemo()\">发送</button>
    <pre id=\"output\">等待请求…</pre>
    <script>
      async function runDemo() {
        const payload = {
          driver_id: document.getElementById('driverId').value,
          city: document.getElementById('city').value,
          query: document.getElementById('query').value,
        };
        const response = await fetch('/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        });
        const data = await response.json();
        document.getElementById('output').textContent = JSON.stringify(data, null, 2);
      }
    </script>
  </body>
</html>
"""


@app.post("/chat", response_model=AgentResponse)
def chat(payload: ChatRequest) -> AgentResponse:
    return agent.run(driver_id=payload.driver_id, city=payload.city, query=payload.query)


def main() -> None:
    uvicorn.run("driverops_agent_lab.app:app", host="0.0.0.0", port=8001, reload=False)


if __name__ == "__main__":
    main()
