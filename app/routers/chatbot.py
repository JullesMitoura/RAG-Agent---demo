from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from app.services.agent import CustomAgent

router = APIRouter(prefix="/agent", tags=["Agent"])


class TaskData(BaseModel):
    prompt: str

agent_service = CustomAgent()

@router.post("/execute")
def execute_agent_task(task: TaskData, collection: str = Query(..., description="Collection name for Qdrant search")):
    try:
        result = agent_service.agent_exec(user_input=task.prompt, collection=collection)
        
        return {
            "response": result["response"],
            "metadata": {
                "tool_name": result["tool_name"],
                "RAGContext": result["RAGContext"]
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))