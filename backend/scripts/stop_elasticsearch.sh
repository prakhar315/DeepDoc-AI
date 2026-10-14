#!/bin/bash
echo "Stopping Elasticsearch Docker container..."
docker stop elastic
docker rm elastic
echo "Elasticsearch stopped and removed."
