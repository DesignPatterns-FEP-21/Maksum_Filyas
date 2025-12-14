import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Імпортує роутер з  ендпоінтами
from drones.api.endpoints import router as mission_router

# Створення екземпляру додатку FastAPI
app = FastAPI(
    title="Drone Mission Control API",
    description="API для керування місіями дронів (Lab 7 Design Patterns)",
    version="1.0.0"
)

# дозволяє запити з будь-якого джерела 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Підключення маршрутів 
app.include_router(mission_router)

@app.get("/")
async def root():
    """Перевірка  сервера."""
    return {"message": "Drone Control System is Online", "docs_url": "/docs"}

if __name__ == "__main__":
    uvicorn.run("drones.api.server:app", host="127.0.0.1", port=8000, reload=True)