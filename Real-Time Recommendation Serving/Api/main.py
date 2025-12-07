from fastapi import FastAPI
from core.config import settings
from routers import recommend, similar, trending, health, reload

app = FastAPI(
    title="Phase-4 Recommendation API",
    version="1.0.0",
)

# Routers
app.include_router(recommend.router)
app.include_router(similar.router)
app.include_router(trending.router)
app.include_router(health.router)
app.include_router(reload.router)


@app.get("/")
def root():
    return {"message": "Recommendation API Running", "version": app.version}
