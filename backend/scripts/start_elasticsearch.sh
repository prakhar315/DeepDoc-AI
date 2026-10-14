#!/bin/bash

echo "Starting Elasticsearch from docker/elasticsearch-compose.yml..."

# Navigate to the repo root if not already there
cd "$(dirname "$0")"/..

# Start the container
docker compose -f docker/elasticsearch-compose.yml up -d

echo "Elasticsearch is starting..."
echo "Access it at: http://localhost:9200"
echo "Check memory with: docker stats elastic"
