import { motion } from 'framer-motion'
import { Brain, Sparkles, BarChart3, Cpu } from 'lucide-react'

interface HeaderProps {
    onOpenDashboard?: () => void
    onOpenTraining?: () => void
}

export default function Header({ onOpenDashboard, onOpenTraining }: HeaderProps) {
    return (
        <motion.header
            className="text-center"
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
        >
            <div className="flex items-center justify-center gap-3 mb-4">
                <motion.div
                    animate={{
                        rotate: [0, 360],
                    }}
                    transition={{
                        duration: 20,
                        repeat: Infinity,
                        ease: "linear"
                    }}
                >
                    <Brain size={48} className="text-purple-400" />
                </motion.div>
                <h1 className="text-5xl md:text-6xl font-bold bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
                    NeuroScan AI
                </h1>
            </div>

            <div className="flex items-center justify-center gap-2 mb-6">
                <Sparkles size={20} className="text-yellow-400" />
                <h2 className="text-2xl md:text-3xl text-white/90 font-light">
                    Brain Tumor Detection
                </h2>
                <Sparkles size={20} className="text-yellow-400" />
            </div>

            <p className="text-white/70 text-lg max-w-2xl mx-auto">
                AI-powered MRI analysis with{' '}
                <span className="text-purple-300 font-semibold">explainable AI</span> and{' '}
                <span className="text-blue-300 font-semibold">real-time insights</span>
            </p>

            <div className="mt-6 flex items-center justify-center gap-4 text-sm text-white/50">
                <span className="px-3 py-1 glass rounded-full">EfficientNet-B4</span>
                <span className="px-3 py-1 glass rounded-full">Grad-CAM</span>
                <span className="px-3 py-1 glass rounded-full">AI Narratives</span>
            </div>

            {/* Action Buttons */}
            <div className="mt-8 flex items-center justify-center gap-4">
                {onOpenTraining && (
                    <motion.button
                        onClick={onOpenTraining}
                        className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-blue-500 to-cyan-500 hover:from-blue-600 hover:to-cyan-600 rounded-xl text-white font-semibold shadow-lg hover:shadow-xl transition-all"
                        whileHover={{ scale: 1.05, y: -2 }}
                        whileTap={{ scale: 0.95 }}
                    >
                        <Cpu size={20} />
                        <span>Training Simulation</span>
                    </motion.button>
                )}

                {onOpenDashboard && (
                    <motion.button
                        onClick={onOpenDashboard}
                        className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 rounded-xl text-white font-semibold shadow-lg hover:shadow-xl transition-all"
                        whileHover={{ scale: 1.05, y: -2 }}
                        whileTap={{ scale: 0.95 }}
                    >
                        <BarChart3 size={20} />
                        <span>Model Metrics</span>
                    </motion.button>
                )}
            </div>
        </motion.header>
    )
}
