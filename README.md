# 🧠 AntiGravity - Brain Tumor Detection System

**The future of AI-powered medical imaging analysis**

![Status](https://img.shields.io/badge/status-in%20development-yellow)
![License](https://img.shields.io/badge/license-MIT-blue)

---

## 🎯 Overview

AntiGravity is a cutting-edge brain tumor detection system built for the hackathon, combining state-of-the-art deep learning with beautiful user experience and explainable AI.

### ✨ Key Features

- 🤖 **Modern AI Models**: EfficientNet-B4 / ResNet50 with transfer learning
- 🎨 **Beautiful UI**: React + TypeScript + Tailwind CSS with animations
- 🔍 **Explainable AI**: Grad-CAM visualizations (coming soon)
- 📝 **AI Narratives**: LLM-generated explanations (optional)
- ⚡ **Fast & Responsive**: Real-time predictions with smooth UX
- 🌙 **Dark Mode**: Modern glassmorphism design

---

## 🚀 Quick Start

### One-Command Setup (Windows)

```bash
# Run thesetup script
setup.bat
```

That's it! The script will:
- Create Python virtual environment
- Install all dependencies (backend + frontend)
- Setup configuration files
- Create data directories

### Running the Application

```bash
# Start both backend and frontend
run.bat
```

**Access:**
- 🎨 Frontend: http://localhost:3000
- ⚙️ Backend API: http://localhost:8000
- 📚 API Docs: http://localhost:8000/docs

---

## 📁 Project Structure

```
AntiGravity/
├── backend/              # FastAPI + PyTorch backend
│   ├── app/             # API application
│   ├── ml/              # ML models & training
│   └── requirements.txt # Python dependencies
├── frontend/            # React + TypeScript frontend
│   ├── src/
│   │   ├── components/  # React components
│   │   └── App.tsx      # Main app
│   └── package.json     # Node dependencies
├── data/                 # Datasets (gitignored)
├── setup.bat            # Setup script
├── run.bat              # Run script
└── README.md            # This file
```

---

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI
- **ML**: PyTorch 2.x
- **Models**: EfficientNet-B4, ResNet50
- **Data**: Albumententations for augmentation
- **Training**: Early stopping, LR scheduling

### Frontend
- **Framework**: React 18 + TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **Animations**: Framer Motion
- **Upload**: React Dropzone
- **Icons**: Lucide React

### ML Pipeline
- Transfer learning with pretrained models
- Data augmentation (Albumentations)
- Stratified train/val/test splits
- Class-weighted loss for imbalanced data
- Cosine annealing LR scheduler

---

## 📊 Current Status

### ✅ Completed
- [x] Project structure & setup
- [x] Backend API foundation (FastAPI)
- [x] ML pipeline (data loading, models, training)
- [x] Frontend UI (React + TypeScript + Tailwind)
- [x] Upload interface with drag & drop
- [x] Results visualization
- [x] Animations & dark mode
- [x] Helper scripts (setup.bat, run.bat)

### 🔄 In Progress
- [ ] Dataset download & preparation
- [ ] Model training
- [ ] Inference API endpoints
- [ ] Grad-CAM implementation

### 📋 Planned
- [ ] LLM integration for narratives
- [ ] Model comparison dashboard
- [ ] Batch processing
- [ ] Deployment (Docker + Cloud)

---

## 💻 Development

### Manual Setup

**Backend:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
cp .env.example .env
```

**Frontend:**
```bash
cd frontend
npm install
```

### Running Manually

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

## 📚 Documentation

- [Baseline Analysis](C:/Users/s/.gemini/antigravity/brain/.../baseline_analysis.md) - Repository comparison
- [Phase 1 Plan](C:/Users/s/.gemini/antigravity/brain/.../phase1_plan.md) - Setup details
- [Frontend README](frontend/README.md) - Frontend documentation
- [Scripts Guide](SCRIPTS.md) - Helper scripts usage

---

## 🎯 Hackathon Features

What makes this project stand out:

1. **Modern Architecture**: Latest ML models with proven performance
2. **Beautiful UX**: Professional UI with smooth animations
3. **Explainable AI**: Grad-CAM visualizations (coming soon)
4. **AI Narratives**: LLM-generated explanations
5. **Easy Setup**: One-command installation
6. **Professional Code**: TypeScript, linting, best practices

---

## ⚠️ Important Notes

- This is a **research/educational project**
- **Not for clinical use** or medical diagnosis
- Always consult medical professionals for health concerns
- Dataset used is for demonstration purposes

---

## 🏆 Built For Hackathon Success

This project combines:
- ✅ Technical depth (modern ML, proper architecture)
- ✅ User experience (beautiful UI, smooth animations)
- ✅ Innovation (explainable AI, AI narratives)
- ✅ Polish (documentation, easy setup, professional code)

---

## 📝 License

MIT License - feel free to use for learning and research!

---

## 🙏 Acknowledgments

- Brain tumor datasets from Kaggle community
- Open source ML frameworks (PyTorch, timm)
- React & modern web ecosystem

---

**Built with ❤️ and lots of ☕**

🚀 Ready to revolutionize medical AI!
