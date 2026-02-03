source fastapi-env/bin/activate
uvicorn backend.main:app --reload &
cd frontend
npm run dev