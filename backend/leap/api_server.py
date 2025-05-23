"""
FastAPI server entry point.
"""
import uvicorn
from .api import create_app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "leap.api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
