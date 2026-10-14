
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    elasticsearch_url: str = "http://localhost:9200"
    # Keep the existing index name to avoid orphaning data during branding changes.
    index_name: str = "querydesk_documents"
    frontend_url: str = "http://localhost:5173"
    embed_model: str ="all-MiniLM-L6-v2"
    insert_seed_data: bool = False
    
    class Config:
        env_file = ".env"

settings = Settings()