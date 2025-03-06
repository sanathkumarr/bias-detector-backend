#!/bin/bash
pip install -r requirements.txt  # Install dependencies
python -m spacy download en_core_web_sm  # Install Spacy model
uvicorn src.api.main:app --host=0.0.0.0 --port=10000
