import { motion, AnimatePresence } from 'framer-motion'
import { Brain } from 'lucide-react'
import { PredictionResult } from '../App'
import { ResultsTabs } from './ResultsTabs'

interface ResultsSectionProps {
    result: PredictionResult | null
    isLoading: boolean
}

export default function ResultsSection({ result, isLoading }: ResultsSectionProps) {
    return (
        <div className="glass rounded-2xl p-8 h-full flex flex-col">
            <h3 className="text-2xl font-bold text-white mb-6 flex items-center gap-2">
                <Brain size={28} className="text-blue-400" />
                Analysis Results
            </h3>

            <div className="flex-1 flex items-center justify-center overflow-auto">
                <AnimatePresence mode="wait">
                    {isLoading ? (
                        <LoadingState key="loading" />
                    ) : result ? (
                        <ResultDisplay key="result" result={result} />
                    ) : (
                        <EmptyState key="empty" />
                    )}
                </AnimatePresence>
            </div>
        </div>
    )
}

function LoadingState() {
    return (
        <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="text-center"
        >
            <motion.div
                animate={{
                    rotate: 360,
                    scale: [1, 1.2, 1],
                }}
                transition={{
                    rotate: { duration: 2, repeat: Infinity, ease: "linear" },
                    scale: { duration: 1.5, repeat: Infinity, ease: "easeInOut" }
                }}
                className="inline-block mb-6"
            >
                <Brain size={64} className="text-purple-400" />
            </motion.div>

            <h4 className="text-2xl font-bold text-white mb-2">Analyzing MRI Scan</h4>
            <p className="text-white/60 mb-6">AI is processing your image...</p>

            <div className="flex flex-col gap-3 max-w-md mx-auto">
                <LoadingStep label="Loading image..." delay={0} />
                <LoadingStep label="Running EfficientNet-B4 model..." delay={0.2} />
                <LoadingStep label="Generating Grad-CAM visualization..." delay={0.4} />
                <LoadingStep label="Creating AI analysis..." delay={0.6} />
            </div>
        </motion.div>
    )
}

function LoadingStep({ label, delay }: { label: string; delay: number }) {
    return (
        <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay, duration: 0.5 }}
            className="flex items-center gap-3 text-white/80"
        >
            <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                className="w-4 h-4 border-2 border-purple-400 border-t-transparent rounded-full"
            />
            <span>{label}</span>
        </motion.div>
    )
}

function EmptyState() {
    return (
        <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="text-center text-white/60"
        >
            <motion.div
                animate={{
                    y: [0, -10, 0],
                }}
                transition={{
                    duration: 2,
                    repeat: Infinity,
                    ease: "easeInOut"
                }}
                className="mb-4"
            >
                <Brain size={64} className="text-white/30 mx-auto" />
            </motion.div>
            <p className="text-lg">Upload an MRI scan to begin analysis</p>
            <p className="text-sm mt-2">AI-powered brain tumor detection with comprehensive insights</p>
        </motion.div>
    )
}

function ResultDisplay({ result }: { result: PredictionResult }) {
    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="w-full"
        >
            <ResultsTabs result={result} />
        </motion.div>
    )
}
