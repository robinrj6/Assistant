source fastapi-env/bin/activate

# Trap Ctrl+C to kill both processes
trap 'kill $(jobs -p) 2>/dev/null' EXIT INT TERM

uvicorn backend.main:app --reload &
cd frontend
npm run dev

wait