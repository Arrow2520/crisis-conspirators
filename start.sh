#!/bin/bash

echo "Starting Pathway pipeline..."
python pipeline.py &

echo "Waiting for Pathway Vector Store to be ready..."

until curl -s http://localhost:8000/v1/retrieve > /dev/null; do
  sleep 2
done

echo "Pathway is ready. Starting Flask app..."
python app.py