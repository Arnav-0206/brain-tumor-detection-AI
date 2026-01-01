# 🎨 AntiGravity Frontend

Modern React frontend for brain tumor detection with beautiful UI and smooth animations.

## 🚀 Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

The app will run on http://localhost:3000

## 🛠️ Tech Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool (lightning fast!)
- **Tailwind CSS** - Utility-first styling
- **Framer Motion** - Smooth animations
- **React Dropzone** - Drag & drop file upload
- **Lucide React** - Beautiful icons

## ✨ Features

- 🎭 **Dark Mode** - Toggle between light and dark themes
- 📤 **Drag & Drop Upload** - Easy MRI scan upload
- 🎨 **Glass morphism UI** - Modern, beautiful design
- ✨ **Smooth Animations** - Framer Motion powered
- 📊 **Real-time Results** - Live prediction display
- 🔮 **AI Narratives** - Explainable AI explanations
- 🎯 **Responsive Design** - Works on all devices

## 📁 Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Header.tsx          # App header with branding
│   │   ├── UploadSection.tsx   # File upload & preview
│   │   └── ResultsSection.tsx  # Results display
│   ├── App.tsx                 # Main app component
│   ├── main.tsx                # Entry point
│   └── index.css               # Global styles
├── public/                     # Static assets
├── index.html                  # HTML template
├── package.json                # Dependencies
├── tsconfig.json               # TypeScript config
├── tailwind.config.js          # Tailwind config
└── vite.config.ts              # Vite config
```

## 🎨 Design System

### Colors
- **Primary**: Purple gradients (#8B5CF6 → #6366F1)
- **Accent**: Blue/Pink gradients
- **Background**: Dark gradient (slate-900 → purple-900)

### Animations
- Fade in/out transitions
- Scale animations on hover
- Smooth loading states
- Gradient text effects

## 🔌 API Integration

The frontend is configured to proxy API requests to `http://localhost:8000/api`.

To connect to backend:
1. Ensure backend is running on port 8000
2. Frontend will automatically proxy requests
3. No CORS issues!

## 🚧 Development

```bash
# Install dependencies
npm install

# Run dev server with hot reload
npm run dev

# Type checking
npm run tsc --noEmit

# Lint code
npm run lint

# Build for production
npm run build

# Preview production build
npm run preview
```

## 📱 Responsive Breakpoints

- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

## 🎯 Next Steps

- [ ] Connect to real backend API
- [ ] Add Grad-CAM visualization
- [ ] Implement multiple file upload
- [ ] Add model comparison view
- [ ] Create metrics dashboard
- [ ] Add export/download results
