import { useState } from 'react'
import { motion } from 'framer-motion'
import UploadSection from './components/UploadSection'
import ResultsSection from './components/ResultsSection'
import Header from './components/Header'
import ModelDashboard from './components/ModelDashboard'
import TrainingSimulation from './components/TrainingSimulation'

export interface PredictionResult {
    prediction: 'tumor' | 'no_tumor'
    confidence: number
    gradcamUrl?: string
    narrative?: string
    processingTime?: number
    tumor_type?: string
    type_confidence?: number
    type_characteristics?: string[]
    type_description?: string
    differential_diagnosis?: Array<{
        diagnosis: string
        likelihood: number
        reasoning: string
        key_feature: string
    }>
    risk_assessment?: {
        severity_score: number
        urgency_level: string
        timeline: string
        reasoning: string
    }
}

function App() {
    const [result, setResult] = useState<PredictionResult | null>(null)
    const [isLoading, setIsLoading] = useState(false)
    const [isDashboardOpen, setIsDashboardOpen] = useState(false)
    const [isTrainingOpen, setIsTrainingOpen] = useState(false)

    const handleReset = () => {
        setResult(null)
    }

    const handlePrediction = async (file: File) => {
        setIsLoading(true)
        setResult(null)

        try {
            // Create form data for prediction
            const formData = new FormData()
            formData.append('file', file)

            // Call prediction API
            const response = await fetch('/api/predict', {
                method: 'POST',
                body: formData,
            })

            if (!response.ok) {
                throw new Error(`Prediction failed: ${response.statusText}`)
            }

            const data = await response.json()

            // Fetch Grad-CAM visualization
            const gradcamFormData = new FormData()
            gradcamFormData.append('file', file)

            const gradcamResponse = await fetch('/api/gradcam', {
                method: 'POST',
                body: gradcamFormData,
            })

            let gradcamUrl = undefined
            if (gradcamResponse.ok) {
                const gradcamBlob = await gradcamResponse.blob()
                gradcamUrl = URL.createObjectURL(gradcamBlob)
            }

            // Set result with Grad-CAM
            setResult({
                ...data,
                gradcamUrl
            })

        } catch (error) {
            console.error('Prediction error:', error)
            alert(`Error: ${error instanceof Error ? error.message : 'Failed to get prediction'}`)
        } finally {
            setIsLoading(false)
        }
    }



    return (
        <div className='dark'>
            <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 dark:from-slate-950 dark:via-purple-950 dark:to-slate-950 transition-colors duration-500">
                {/* Background effects */}
                <div className="fixed inset-0 overflow-hidden pointer-events-none">
                    <div className="absolute top-0 left-0 w-96 h-96 bg-purple-500/30 rounded-full blur-3xl animate-pulse-slow" />
                    <div className="absolute bottom-0 right-0 w-96 h-96 bg-blue-500/30 rounded-full blur-3xl animate-pulse-slow" style={{ animationDelay: '1s' }} />
                </div>



                {/* Main content */}
                <div className="relative z-10 container mx-auto px-4 py-8">
                    <Header
                        onOpenDashboard={() => setIsDashboardOpen(true)}
                        onOpenTraining={() => setIsTrainingOpen(true)}
                    />

                    <div className="mt-12 grid lg:grid-cols-2 gap-8">
                        {/* Upload Section */}
                        <motion.div
                            initial={{ opacity: 0, x: -50 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ duration: 0.5 }}
                        >
                            <UploadSection
                                onPredict={handlePrediction}
                                isLoading={isLoading}
                                onReset={handleReset}
                            />
                        </motion.div>

                        {/* Results Section */}
                        <motion.div
                            initial={{ opacity: 0, x: 50 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ duration: 0.5, delay: 0.2 }}
                        >
                            <ResultsSection
                                result={result}
                                isLoading={isLoading}
                            />
                        </motion.div>
                    </div>

                    {/* Footer */}
                    <motion.footer
                        className="mt-16 text-center text-white/60"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ delay: 0.8 }}
                    >
                        <p className="text-sm">
                            Built with ❤️ for medical AI advancement
                        </p>
                        <p className="text-xs mt-2">
                            ⚠️ For research purposes only. Not for clinical diagnosis.
                        </p>
                    </motion.footer>

                    {/* Model Dashboard */}
                    <ModelDashboard
                        isOpen={isDashboardOpen}
                        onClose={() => setIsDashboardOpen(false)}
                    />

                    {/* Training Simulation */}
                    <TrainingSimulation
                        isOpen={isTrainingOpen}
                        onClose={() => setIsTrainingOpen(false)}
                    />
                </div>
            </div>
        </div>
    )
}

export default App
