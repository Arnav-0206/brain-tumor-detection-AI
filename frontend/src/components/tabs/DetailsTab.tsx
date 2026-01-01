import { motion } from 'framer-motion'
import { PredictionResult } from '../../App'
import { CollapsibleNarrative } from '../CollapsibleNarrative'

interface DetailsTabProps {
    result: PredictionResult
}

export function DetailsTab({ result }: DetailsTabProps) {
    return (
        <div className="space-y-6">
            {/* AI Medical Narrative */}
            {result.narrative && (
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                >
                    <CollapsibleNarrative narrative={result.narrative} />
                </motion.div>
            )}

            {/* Technical Details */}
            <motion.div
                className="p-5 glass-dark rounded-xl border border-gray-400/30"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 }}
            >
                <h5 className="text-white font-semibold mb-4 flex items-center gap-2">
                    <span className="text-xl">⚙️</span>
                    Technical Details
                </h5>

                <div className="space-y-3">
                    <div className="grid grid-cols-2 gap-4">
                        <div>
                            <p className="text-white/60 text-sm">Model Architecture</p>
                            <p className="text-white font-semibold">EfficientNet-B4</p>
                        </div>
                        <div>
                            <p className="text-white/60 text-sm">Method</p>
                            <p className="text-white font-semibold">Grad-CAM</p>
                        </div>
                        <div>
                            <p className="text-white/60 text-sm">Training Accuracy</p>
                            <p className="text-white font-semibold">92.3%</p>
                        </div>
                        <div>
                            <p className="text-white/60 text-sm">Dataset</p>
                            <p className="text-white font-semibold">3,264 MRI Scans</p>
                        </div>
                        <div>
                            <p className="text-white/60 text-sm">Framework</p>
                            <p className="text-white font-semibold">PyTorch</p>
                        </div>
                        <div>
                            <p className="text-white/60 text-sm">Input Size</p>
                            <p className="text-white font-semibold">224x224 px</p>
                        </div>
                    </div>

                    {result.processingTime && (
                        <div className="pt-3 border-t border-white/10">
                            <p className="text-white/60 text-sm">Processing Time</p>
                            <p className="text-white font-semibold">{result.processingTime.toFixed(3)} seconds</p>
                        </div>
                    )}
                </div>
            </motion.div>

            {/* AI Model Information */}
            <motion.div
                className="p-5 glass-dark rounded-xl border border-blue-400/30"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
            >
                <h5 className="text-white font-semibold mb-4 flex items-center gap-2">
                    <span className="text-xl">🤖</span>
                    AI Features
                </h5>

                <div className="space-y-2 text-sm">
                    <div className="flex items-start gap-2">
                        <span className="text-green-400">✓</span>
                        <span className="text-white/80">Gemini 2.5 Flash AI-powered medical narratives</span>
                    </div>
                    <div className="flex items-start gap-2">
                        <span className="text-green-400">✓</span>
                        <span className="text-white/80">Interactive brain region analysis</span>
                    </div>
                    <div className="flex items-start gap-2">
                        <span className="text-green-400">✓</span>
                        <span className="text-white/80">Tumor type classification (3 types)</span>
                    </div>
                    <div className="flex items-start gap-2">
                        <span className="text-green-400">✓</span>
                        <span className="text-white/80">Differential diagnosis generation</span>
                    </div>
                    <div className="flex items-start gap-2">
                        <span className="text-green-400">✓</span>
                        <span className="text-white/80">Risk assessment with severity scoring</span>
                    </div>
                    <div className="flex items-start gap-2">
                        <span className="text-green-400">✓</span>
                        <span className="text-white/80">Comprehensive medical report generation</span>
                    </div>
                </div>
            </motion.div>

            {/* Disclaimers */}
            <motion.div
                className="p-5 bg-red-500/10 border-2 border-red-500/30 rounded-xl"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 }}
            >
                <h5 className="text-red-400 font-semibold mb-3 flex items-center gap-2">
                    <span className="text-xl">⚠️</span>
                    Important Disclaimers
                </h5>

                <div className="space-y-2 text-sm text-white/80">
                    <p>
                        <strong className="text-red-400">•</strong> This is an AI screening tool for research and educational purposes only.
                    </p>
                    <p>
                        <strong className="text-red-400">•</strong> All findings must be validated by qualified radiologists and healthcare professionals.
                    </p>
                    <p>
                        <strong className="text-red-400">•</strong> Not a replacement for professional medical diagnosis or clinical decision-making.
                    </p>
                    <p>
                        <strong className="text-red-400">•</strong> No clinical validation or regulatory approval for diagnostic use.
                    </p>
                    <p className="text-red-300 font-semibold mt-3">
                        Always consult qualified healthcare professionals for medical advice.
                    </p>
                </div>
            </motion.div>
        </div>
    )
}
