# 🧠 Brain Tumor Dataset - Download Guide

## Recommended Dataset

**Brain Tumor MRI Dataset** from Kaggle  
Contains: ~3,000+ MRI images classified into tumor/no tumor

### Option 1: Kaggle Dataset (Recommended)

**Dataset**: Brain Tumor Classification (MRI)  
**Link**: https://www.kaggle.com/datasets/sartajbhuvaji/brain-tumor-classification-mri

**What it contains:**
- **Training**: ~2,870 images
- **Testing**: ~394 images
- **Classes**: 4 classes (glioma, meningioma, pituitary, no tumor)
- **Format**: JPG images
- **Size**: ~50 MB

**We'll simplify to binary classification:**
- Tumor: glioma + meningioma + pituitary
- No Tumor: no tumor

---

## 📥 How to Download

### Method 1: Kaggle CLI (Fastest)

```bash
# 1. Install Kaggle CLI
pip install kaggle

# 2. Setup Kaggle API credentials
# - Go to https://www.kaggle.com/settings
# - Click "Create New API Token"
# - Download kaggle.json
# - Place in: C:\Users\<YourUsername>\.kaggle\kaggle.json

# 3. Download dataset
kaggle datasets download -d sartajbhuvaji/brain-tumor-classification-mri

# 4. Extract
# Windows: Right-click → Extract All
# Or use: tar -xf brain-tumor-classification-mri.zip
```

### Method 2: Manual Download

1. **Visit**: https://www.kaggle.com/datasets/sartajbhuvaji/brain-tumor-classification-mri
2. **Click** "Download" button (requires Kaggle account)
3. **Extract** the ZIP file to `AntiGravity/data/raw/`

---

## 📁 Expected Folder Structure

After extraction, organize like this:

```
AntiGravity/data/
├── raw/
│   ├── Training/
│   │   ├── glioma_tumor/
│   │   ├── meningioma_tumor/
│   │   ├── pituitary_tumor/
│   │   └── no_tumor/
│   └── Testing/
│       ├── glioma_tumor/
│       ├── meningioma_tumor/
│       ├── pituitary_tumor/
│       └── no_tumor/
└── processed/
    └── (will be created by script)
```

---

## 🔄 Alternative Datasets

If Kaggle doesn't work, try these:

### Option 2: Brain Tumor Detection 2020
- **Link**: https://www.kaggle.com/datasets/ahmedhamada0/brain-tumor-detection
- **Size**: ~250 MB
- **Images**: ~3,000
- **Classes**: Yes/No (already binary!)

### Option 3: Br35H Dataset
- **Link**: https://www.kaggle.com/datasets/ahmedhamada0/brain-tumor-detection
- **Size**: ~500 MB  
- **Images**: ~3,000+
- **Classes**: Tumor/No Tumor

---

## ⚙️ After Download

Once downloaded, run the preparation script:

```bash
cd backend
.\venv\Scripts\activate
python scripts/prepare_dataset.py
```

This will:
1. Scan the raw data folder
2. Combine tumor classes into binary (tumor/no_tumor)
3. Create train/val/test splits (70/15/15)
4. Generate `splits.json` file
5. Calculate class weights for balanced training

---

## 📊 Dataset Statistics

**Expected after preparation:**

- **Total Images**: ~3,200
- **Training**: ~2,240 (70%)
- **Validation**: ~480 (15%)
- **Test**: ~480 (15%)

**Class Distribution:**
- **Tumor**: ~60-70% (glioma + meningioma + pituitary)
- **No Tumor**: ~30-40%

---

## 🐛 Troubleshooting

**"Kaggle API not found"**
- Install: `pip install kaggle`
- Setup credentials as described above

**"Permission denied on kaggle.json"**
- Ensure file permissions allow read
- Windows: Right-click → Properties → Security

**"Dataset too large"**
- Start with smaller subset
- Or use Br35H (simpler dataset)

**"Wrong folder structure"**
- Manually organize folders as shown above
- Ensure class names match exactly

---

## ✅ Verification

Before training, check:

```bash
# In backend folder
python -c "from ml.data.prepare import count_images; count_images('../data/raw/')"
```

Should show image counts per class.

---

**Next**: Run `scripts/prepare_dataset.py` to create splits! 🚀
