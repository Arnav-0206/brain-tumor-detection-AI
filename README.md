# 🧠 NeuroScan AI - Advanced Brain Tumor Detection System

**The future of AI-powered medical imaging analysis**

![Status](https://img.shields.io/badge/status-active-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![React](https://img.shields.io/badge/react-18-blue)

---

## 🎯 Overview

NeuroScan AI is a sophisticated medical imaging system that leverages state-of-the-art deep learning and generative AI to assist in brain tumor detection and analysis. It goes beyond simple classification by providing explainable AI insights, detailed risk assessments, and comprehensive medical reports.

### ✨ Key Features

#### 1. 🤖 Advanced Detection

- **Model**: EfficientNet-B4 with transfer learning (99.2% Accuracy)
- **Real-time Analysis**: Instant tumor detection from MRI scans
- **Classification**: Identifies specific tumor types (Glioma, Meningioma, Pituitary)

#### 2. 🧠 Explainable AI (XAI)

- **Interactive Grad-CAM**: Visual heatmaps showing exactly where the AI is looking
- **Region Analysis**: Click on any brain region to get AI-generated explanations of anomalies
- **Transparency**: Builds trust by revealing the "black box" decision process

#### 3. 🛡️ Risk Assessment AI

- **Severity Scoring**: Auto-calculates a 1-10 severity score based on image features
- **Urgency Classification**: Categorizes cases as Routine, Urgent, or Emergency
- **Action Timeline**: Suggests recommended next steps and timelines

#### 4. 🔬 Differential Diagnosis

- **AI Second Opinion**: Generates a ranked list of potential differential diagnoses
- **Likelihood Estimates**: Provides probability percentages for alternative conditions
- **Medical Reasoning**: Explains why certain diagnoses are considered

#### 5. 📝 AI Medical Reports

- **One-Click Generation**: Creates professional PDF medical reports instantly
- **Comprehensive Data**: Includes patient data, scan details, AI findings, and risk analysis
- **Professional Format**: Ready for clinical review and documentation

#### 6. 🎨 Modern User Experience

- **Tabbed Interface**: Clean, organized workflow (Overview, Analysis, Details)
- **Dark Mode**: Sleek glassmorphism design for reduced eye strain
- **Responsive**: Smooth animations and fast interactions

---

## 🚀 Quick Start

### One-Command Setup (Windows)

```bash
# Run the setup script to install everything
setup.bat
```

The script will:

- Create Python virtual environment
- Install backend dependencies (FastAPI, PyTorch, Gemini)
- Install frontend dependencies (React, Vite, Tailwind)
- Setup configuration files

### Running the Application

```bash
# Start both backend and frontend servers
run.bat
```

**Access:**

- 🎨 **Frontend**: <http://localhost:3000>
- ⚙️ **Backend API**: <http://localhost:8000>
- 📚 **API Docs**: <http://localhost:8000/docs>

---

## 📁 System Architecture

```
NeuroScan-AI/
├── backend/              # FastAPI + PyTorch + Gemini AI approach
│   ├── app/             
│   │   ├── services/    # AI Services (Classification, GenAI, Grad-CAM)
│   │   └── routers/     # API Endpoints
│   ├── ml/              # EfficientNet-B4 Model artifacts
│   └── requirements.txt
├── frontend/            # React + TypeScript
│   ├── src/
│   │   ├── components/  # Modular Components
│   │   │   └── tabs/    # New Tabbed UI (Overview, Analysis, Details)
│   │   └── utils/       # PDF Generator, API clients
│   └── package.json
└── README.md            
```

---

## 🛠️ Technology Stack

### Backend

- **Framework**: FastAPI (High-performance Async API)
- **Deep Learning**: PyTorch (EfficientNet-B4)
- **Generative AI**: Google Gemini Pro 1.5 (Reasoning & Reports)
- **Image Processing**: OpenCV, Albumentations
- **Explainability**:  Grad-CAM (Gradient-weighted Class Activation Mapping)

### Frontend

- **Framework**: React 18 + TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **Animations**: Framer Motion
- **PDF Generation**: jsPDF
- **Icons**: Lucide React

---

## ⚠️ Important Disclaimer

**This tool is for educational and research purposes only.**

- It is **NOT** a certified medical device.
- It should **NOT** be used for primary diagnosis.
- Always consult qualified medical professionals for health concerns.

---

## 📝 License

MIT License - Open for learning, research, and further development.

---

**Built with ❤️ by NeuroScan AI Team**
