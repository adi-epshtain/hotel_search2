## 🏨 BoomNow Hotel Search

Full-stack demo for searching BoomNow hotels. FastAPI backend proxies BoomNow APIs, Vue frontend provides a simple search widget.

---

### 🚀 Backend Setup
1. `cd backend`
2. Create virtualenv (optional): `python -m venv .venv && .\.venv\Scripts\activate`
3. Install deps: `pip install -r requirements.txt`
4. Run main app

---

### 🌐 Frontend Setup
1. `cd frontend`
2. Install deps: `npm install`
3. Dev server: `npm run dev`
4. Open `http://localhost:5173/`

---

### 🔌 API Overview
- `GET /api/health` → BoomNow status (calls `/open_api/v1/status`)
- `GET /api/search?city=TLV&adults=2` → forwards to BoomNow `/open_api/v1/search`

Auth tokens are cached in `BoomNowAuth` with expiry buffer; credentials fetched from env.

---

### 🧪 Quick Test
```bash
curl "http://127.0.0.1:8000/api/search?city=Tel%20Aviv&adults=2"
```

---

### 🧱 Tech Stack
- FastAPI + httpx async client
- Vue 3 + Axios

---

### 🔍 Troubleshooting
- 403 from BoomNow → verify client id/secret
- 204/no data in frontend → ensure proxy to backend works (avoid hitting Vite dev server)
- Token miss → check `.env` loaded (via `load_dotenv()` in `config.py`)
Hotel Search Widget (FastAPI + Vue)

A small demo project showing a hotel search widget built with FastAPI (Python) and Vue.js, integrating with the BoomNow Open API.

Features

Search by city + number of adults

FastAPI backend calling BoomNow /open_api/v1/listings

Vue UI displaying hotel cards (image, name, price)

Setup
Backend
cd backend
uvicorn backend.app.main:app --reload


Create backend/.env:

BOOMNOW_BASE_URL=https://app.boomnow.com
BOOMNOW_API_TOKEN=<your_token>

Frontend
cd frontend
npm install
npm run dev


Runs at: http://localhost:5173

Proxy to backend is configured in vite.config.js.

API
GET /api/search?city=<city>&adults=<n>