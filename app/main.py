from fastapi import FastAPI

app = FastAPI(title="Todo List API")


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}
