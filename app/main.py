import uvicorn
from fastapi import FastAPI
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from app.routers.chatbot import router as agent_router

app = FastAPI()


app.include_router(agent_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)