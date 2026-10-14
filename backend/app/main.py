from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import logging

from app.config import settings
from app.api.search import router as search_router
from app.services.elastic import does_index_exist, setup_index
from app.seed_data import insert_seed_data

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="DeepDoc AI",
    version="0.1.0",
    description="Semantic search engine for internal documents"
)

@app.on_event("startup")
def initialize_search_index():
    if not does_index_exist():
        setup_index()
        if settings.insert_seed_data:
            logger.info("Seeding enabled: inserting seed documents...")
            insert_seed_data()
        else:
            logger.info("Seeding skipped.")

@app.get("/config-check")
def show_config():
    return {
        "index": settings.index_name,
        "elastic_url": settings.elasticsearch_url,
        "frontend_url": settings.frontend_url,
        "embed_model": settings.embed_model
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(search_router)
