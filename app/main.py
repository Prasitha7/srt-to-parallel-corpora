from fastapi import FastAPI
from .controllers.corpus_controller import router as corpus_router

def create_app() -> FastAPI:
    app = FastAPI(title="Subtitle Parallel Corpus API", version="1.0.0")
    app.include_router(corpus_router)
    return app

app = create_app()
