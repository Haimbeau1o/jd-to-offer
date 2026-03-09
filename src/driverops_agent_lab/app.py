from __future__ import annotations

import uvicorn
from fastapi import FastAPI

from driverops_agent_lab.agent import DriverOpsAgent
from driverops_agent_lab.schemas import AgentResponse, ChatRequest

app = FastAPI(title="DriverOps Agent Lab", version="0.1.0")
agent = DriverOpsAgent()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/chat", response_model=AgentResponse)
def chat(payload: ChatRequest) -> AgentResponse:
    return agent.run(driver_id=payload.driver_id, city=payload.city, query=payload.query)


def main() -> None:
    uvicorn.run("driverops_agent_lab.app:app", host="0.0.0.0", port=8001, reload=False)


if __name__ == "__main__":
    main()
