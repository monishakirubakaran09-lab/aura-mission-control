from fastapi import FastAPI

app = FastAPI(title="Autonomous Mission Commander")


@app.get("/")
def home():
    return {
        "status": "online",
        "message": "Mission Commander Backend is running"
    }
    