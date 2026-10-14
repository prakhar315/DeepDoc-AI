from elasticsearch import Elasticsearch
from uuid import uuid4
from app.config import settings

INDEX_NAME = settings.index_name

client = Elasticsearch(settings.elasticsearch_url)

def does_index_exist() -> bool:
    return client.indices.exists(index=INDEX_NAME)

def setup_index():

    mapping = {
        "mappings": {
            "properties": {
                "text": { "type": "text" },
                "embedding": {
                    "type": "dense_vector",
                    "dims": 384,  # adjust to your model
                    "index": True,
                    "similarity": "cosine"
                },
                "metadata": {
                    "properties": {
                        "department": { "type": "keyword" },
                        "doc_id": { "type": "keyword" },
                        "source": { "type": "keyword" },
                        "title": { "type": "keyword" }
                    }
                }
            }
        }
    }

    client.indices.create(index=INDEX_NAME, body=mapping)
    
    

def index_document(text:str, embedding:list, metadata:dict):
    id = str(uuid4())
    body = {
        "text": text,
        "embedding": embedding,
        "metadata": metadata
    }
    
    client.index(index=INDEX_NAME, id= id, document = body)
    return {"id": id}

def search_similar_documents(query_embedding: list, department: str = None, top_k: int = 5):
    base_query = {
        "match_all": {}
    }
    if department:
        base_query = {
            "bool": {
                "must": {"match_all": {}},
                "filter": {
                    "term": {"metadata.department": department}
                }
            }
        }
    
    search_query = {
        "size": top_k,
        "query": {
            "script_score": {
                "query": base_query,
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                    "params": {"query_vector": query_embedding}
                }
            }
        }
    }
    
    response = client.search(index = INDEX_NAME, body = search_query)
    hits = response["hits"]["hits"]
    
    results = []
    for hit in hits:
        results.append({
            "id": hit["_id"],
            "score": hit["_score"],
            "text": hit["_source"]["text"],
            "metadata": hit["_source"].get("metadata", {})
        })
    return results

def delete_document(doc_id: str):
    response = client.delete(index=INDEX_NAME, id=doc_id, ignore=[404])
    return response

def get_full_document_text_by_group(key: str, value: str) -> dict:
    query = {
        "query": {
            "term": {
                f"metadata.{key}": value
            }
        },
        "_source": ["text", "metadata"]
    }

    response = client.search(index=INDEX_NAME, body=query, size=100)
    hits = response["hits"]["hits"]

    # Sort by chunk number if available
    sorted_hits = sorted(
        hits,
        key=lambda h: h["_source"].get("metadata", {}).get("chunk", 0)
    )

    full_text = "\n\n".join([hit["_source"]["text"] for hit in sorted_hits])
    metadata = sorted_hits[0]["_source"].get("metadata", {}) if sorted_hits else {}

    return {
        "doc_id": value,
        "text": full_text,
        "metadata": metadata,
        "chunk_count": len(sorted_hits)
    }

def delete_all_by_document_id(doc_id: str):
    query = {
        "query": {
            "term": {
                "metadata.doc_id": doc_id
            }
        }
    }
    response = client.delete_by_query(index=INDEX_NAME, body=query)
    return response