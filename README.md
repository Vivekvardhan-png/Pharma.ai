## Pharmacy AI Inventory Platform

This is a full-stack AI-powered pharmacy inventory management platform.

### Tech Stack
- **Frontend**: React + Vite, Material UI, Recharts, Axios
- **Backend**: FastAPI, SQLAlchemy, APScheduler
- **AI/ML**: pandas, numpy, scikit-learn (with lightweight naive forecasting implemented, Prophet/ARIMA pluggable)
- **DB**: SQLite by default (PostgreSQL ready via `DATABASE_URL`)

### Project Structure
- `backend/app`: FastAPI app with `api`, `models`, `services`, `ml`, `chatbot`, `utils`
- `frontend`: React SPA with dashboard, uploads, and chatbot
- `data/sample_excel_files`: sample formats for inventory and sales uploads

### Running Backend Locally
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --app-dir backend
```

Environment:
- `DATABASE_URL` (optional): e.g. `sqlite:///./pharmacy.db` or PostgreSQL URL.

### Running Frontend Locally
```bash
cd frontend
npm install
npm run dev
```

Configure API base URL:
- Create `.env` in `frontend` with `VITE_API_BASE_URL=http://localhost:8000`

### Deployment Notes
- **Frontend**: deploy `frontend` to Vercel/Netlify (build command `npm run build`, output `dist`).
- **Backend**: deploy `backend` to Render/Railway using `uvicorn app.main:app`.
- Use free-tier PostgreSQL in production by setting `DATABASE_URL`.



