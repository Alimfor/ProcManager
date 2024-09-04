from fastapi import FastAPI
from app.api.v1.dynamic_query import router as dynamic_query_router

app = FastAPI()

app.include_router(dynamic_query_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
