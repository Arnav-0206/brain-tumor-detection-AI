# 🚀 Backend API - Quick Start Guide

## ✅ Setup Backend

```bash
# Navigate to backend
cd backend

# Create virtual environment (if not done)
python -m venv venv

# Activate
.\venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Copy environment file
copy .env.example .env
```

## 🏃 Run Backend

```bash
# Make sure you're in backend folder and venv is activated
uvicorn app.main:app --reload --port 8000
```

**Access:**
- API: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- Prediction endpoint: http://localhost:8000/api/predict
- Grad-CAM endpoint: http://localhost:8000/api/gradcam

## 📝 API Endpoints

### 1. Health Check
```
GET /
GET /health
```

### 2. Predict Brain Tumor
```
POST /api/predict
Content-Type: multipart/form-data

Body: {
  file: <image file>
}

Response: {
  "prediction": "tumor" | "no_tumor",
  "confidence": 0.94,
  "probabilities": {
    "no_tumor": 0.06,
    "tumor": 0.94
  },
  "processing_time": 1.2,
  "narrative": "AI-generated explanation..."
}
```

### 3. Generate Grad-CAM
```
POST /api/gradcam
Content-Type: multipart/form-data

Body: {
  file: <image file>
}

Response: PNG image with heatmap overlay
```

## 🧪 Test with Curl

```bash
# Health check
curl http://localhost:8000/health

# Prediction (replace with your image path)
curl -X POST "http://localhost:8000/api/predict" \
  -F "file=@path/to/brain_scan.jpg"

# Grad-CAM
curl -X POST "http://localhost:8000/api/gradcam" \
  -F "file=@path/to/brain_scan.jpg" \
  -o gradcam_output.png
```

## 📊 Model Information

The API will:
1. **Try to load trained model** from `ml/checkpoints/best_model.pth`
2. **Fallback to pretrained model** if checkpoint not found
3. Use EfficientNet-B4 architecture by default

## ⚙️ Configuration

Edit `.env` file:
```env
MODEL_PATH=ml/checkpoints/best_model.pth
MODEL_TYPE=efficientnet_b4
DEVICE=cuda  # or cpu
IMAGE_SIZE=224
```

## 🔌 Connect Frontend

Frontend is already configured to proxy `/api` requests to `http://localhost:8000`.

Just make sure both services are running:
- Backend: `http://localhost:8000`
- Frontend: `http://localhost:3000`

## 🐛 Troubleshooting

**Model not found warning:**
- Normal! API will use pretrained model until you train your own
- To train: see Phase 5 instructions

**CUDA not available:**
- Set `DEVICE=cpu` in `.env`
- Performance will be slower but still works

**Import errors:**
- Make sure venv is activated
- Run `pip install -r requirements.txt` again

---

**Next:** Train your own model in Phase 5! 🤖
