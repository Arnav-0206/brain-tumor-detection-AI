# 🚀 Quick Start Scripts for AntiGravity

This directory contains helper scripts to make development easier.

## 📜 Available Scripts

### `setup.bat` (Windows)
One-command setup for the entire project.

```bash
setup.bat
```

**What it does:**
- Creates Python virtual environment
- Installs all Python dependencies
- Creates `.env` file from template
- Installs Node.js dependencies
- Creates data directories

**Requirements:**
- Python 3.11+
- Node.js 18+

---

### `run.bat` (Windows)
Start both backend and frontend in separate terminals.

```bash
run.bat
```

**What it does:**
- Starts backend server on port 8000
- Starts frontend dev server on port 3000
- Opens both in new command windows

**Access:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## 📝 Manual Setup (if scripts don't work)

### Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
cp .env.example .env
```

### Frontend Setup
```bash
cd frontend
npm install
```

###Running Manually

**Terminal 1 - Backend:**
```bash
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

---

## 🐛 Troubleshooting

### Python not found
- Install Python 3.11+ from https://python.org
- Make sure to check "Add Python to PATH" during installation

### Node.js not found
- Install Node.js 18+ from https://nodejs.org
- Restart terminal after installation

### Permission errors
- Run scripts as administrator
- Or run commands manually

### Port already in use
- Backend: Change port in `backend/app/config.py`
- Frontend: Change port in `frontend/vite.config.ts`

---

## 💡 Tips

- Run `setup.bat` only once for initial setup
- Use `run.bat` every time you want to start working
- Keep both terminal windows open while developing
- Changes to code will auto-reload (hot reload enabled)

---

Built with ❤️ for hackathon success! 🏆
