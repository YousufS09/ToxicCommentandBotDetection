# Deployment Guide

## Backend Deployment

The FastAPI backend lives in `backend/`.

Run locally:

```bash
cd backend
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000
```

Expected runtime assets:

- `Models/BERT_Toxic`
- `Models/bot_hybrid_rf.pkl`
- `Models/bot_feature_info.json`
- `Models/sbert_encoder`

## Frontend Deployment

The React frontend lives in `frontend/`.

Build for production:

```bash
cd frontend
npm install
npm run build
```

Set the backend URL before building or running in another environment:

```bash
REACT_APP_API_URL=https://your-backend-domain
```

## Suggested Hosting Pattern

- Host the backend as an API service
- Host the frontend as a static site
- Point the frontend to the backend with `REACT_APP_API_URL`

## Health Check

The backend exposes:

- `GET /`

which returns a simple status message.
