import { motion } from 'framer-motion'
import { useState } from 'react'
import { PredictionResult } from '../../App'
import { Brain } from 'lucide-react'

interface AnalysisTabProps {
    result: PredictionResult
}

export function AnalysisTab({ result }: AnalysisTabProps) {
    const [clickedRegion, setClickedRegion] = useState<{
        x: number
        y: number
        region: string
        attention: number
        explanation: string
    } | null>(null)
    const [isLoading, setIsLoading] = useState(false)

    const isTumor = result.prediction === 'tumor'

    const handleImageClick = async (e: React.MouseEvent<HTMLImageElement>) => {
        if (!result.gradcamUrl) return

        const rect = e.currentTarget.getBoundingClientRect()
        const relX = (e.clientX - rect.left) / rect.width
        const relY = (e.clientY - rect.top) / rect.height
        const displayX = relX * 100
        const displayY = relY * 100

        setIsLoading(true)

        try {
            const response = await fetch('/api/explain-region', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    x: relX,
                    y: relY,
                    prediction: isTumor ? 'tumor' : 'no_tumor',
                    confidence: result.confidence
                })
            })

            if (!response.ok) throw new Error('Failed to get region explanation')

            const data = await response.json()

            setClickedRegion({
                x: displayX,
                y: displayY,
                region: data.region,
                attention: data.attention,
                explanation: data.explanation
            })
        } catch (error) {
            console.error('Region explanation error:', error)
            setClickedRegion({
                x: displayX,
                y: displayY,
                region: 'Brain Region',
                attention: 50,
                explanation: 'Unable to fetch detailed explanation. Please try again.'
            })
        } finally {
            setIsLoading(false)
        }
    }

    return (
        <div className="space-y-6">
            {/* Tumor Classification */}
            {result.tumor_type && (
                <motion.div
                    className="p-5 glass-dark rounded-xl border border-purple-400/30"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                >
                    <div className="flex items-center gap-2 mb-3">
                        <div className="text-2xl">🧬</div>
                        <h5 className="text-white font-semibold">Tumor Classification</h5>
                    </div>

                    <div className="space-y-3">
                        <div className="flex items-baseline justify-between">
                            <span className="text-lg font-bold text-purple-300">{result.tumor_type}</span>
                            <span className="text-sm text-white/70">
                                {(result.type_confidence! * 100).toFixed(1)}% confidence
                            </span>
                        </div>

                        {result.type_description && (
                            <p className="text-white/70 text-sm">{result.type_description}</p>
                        )}

                        {result.type_characteristics && result.type_characteristics.length > 0 && (
                            <div>
                                <p className="text-white/80 text-sm font-semibold mb-2">Key Characteristics:</p>
                                <ul className="space-y-1">
                                    {result.type_characteristics.map((char, idx) => (
                                        <li key={idx} className="text-white/70 text-sm flex items-start gap-2">
                                            <span className="text-purple-400 mt-1">•</span>
                                            <span>{char}</span>
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        )}
                    </div>
                </motion.div>
            )}

            {/* Differential Diagnosis */}
            {result.differential_diagnosis && result.differential_diagnosis.length > 0 && (
                <motion.div
                    className="p-5 glass-dark rounded-xl border border-blue-400/30"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.1 }}
                >
                    <div className="flex items-center gap-2 mb-4">
                        <div className="text-2xl">🔬</div>
                        <h5 className="text-white font-semibold">Differential Diagnosis</h5>
                    </div>

                    <div className="space-y-3">
                        {result.differential_diagnosis.map((dx, index) => (
                            <motion.div
                                key={index}
                                className="p-3 bg-white/5 rounded-lg border border-white/10 hover:border-blue-400/50 transition-colors"
                                initial={{ opacity: 0, x: -20 }}
                                animate={{ opacity: 1, x: 0 }}
                                transition={{ delay: 0.2 + index * 0.1 }}
                            >
                                <div className="flex items-start justify-between mb-2">
                                    <div className="flex items-start gap-2 flex-1">
                                        <span className="flex items-center justify-center w-6 h-6 rounded-full bg-blue-500/20 text-blue-300 text-xs font-bold">
                                            {index + 1}
                                        </span>
                                        <div className="flex-1">
                                            <h6 className="text-white font-semibold">{dx.diagnosis}</h6>
                                            <div className="flex items-center gap-2 mt-1">
                                                <div className="flex-1 bg-white/10 rounded-full h-2 overflow-hidden">
                                                    <motion.div
                                                        className="h-full bg-gradient-to-r from-blue-500 to-purple-500 rounded-full"
                                                        initial={{ width: 0 }}
                                                        animate={{ width: `${dx.likelihood}%` }}
                                                        transition={{ duration: 0.8, delay: 0.3 + index * 0.1 }}
                                                    />
                                                </div>
                                                <span className="text-blue-300 text-sm font-bold min-w-[3rem] text-right">
                                                    {dx.likelihood}%
                                                </span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <p className="text-white/70 text-sm mb-2 ml-8">{dx.reasoning}</p>
                                <div className="flex items-center gap-2 ml-8">
                                    <span className="text-blue-400 text-xs">🔑</span>
                                    <span className="text-white/60 text-xs italic">{dx.key_feature}</span>
                                </div>
                            </motion.div>
                        ))}
                    </div>
                </motion.div>
            )}

            {/* Interactive Grad-CAM */}
            {result.gradcamUrl && (
                <motion.div
                    className="p-4 glass-dark rounded-xl"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.3 }}
                >
                    <h5 className="text-white font-semibold mb-3 flex items-center gap-2">
                        <Brain size={20} className="text-purple-400" />
                        Interactive Attention Heatmap
                    </h5>

                    <motion.div
                        className="mb-4 p-3 bg-gradient-to-r from-purple-500/20 to-blue-500/20 border-2 border-purple-400/50 rounded-lg"
                        animate={{
                            borderColor: ['rgba(167, 139, 250, 0.5)', 'rgba(96, 165, 250, 0.8)', 'rgba(167, 139, 250, 0.5)'],
                        }}
                        transition={{ duration: 2, repeat: Infinity }}
                    >
                        <div className="flex items-center gap-3">
                            <motion.div
                                animate={{ scale: [1, 1.2, 1] }}
                                transition={{ duration: 1.5, repeat: Infinity }}
                                className="text-3xl"
                            >
                                👆
                            </motion.div>
                            <div>
                                <p className="text-white font-bold text-lg">Click Anywhere on the Heatmap!</p>
                                <p className="text-white/70 text-sm">Explore different regions to see what the AI detected</p>
                            </div>
                        </div>
                    </motion.div>

                    <div className="relative">
                        <img
                            src={result.gradcamUrl}
                            alt="Grad-CAM"
                            className="w-full rounded-lg cursor-pointer hover:opacity-90 transition-opacity border-2 border-purple-400/30"
                            onClick={handleImageClick}
                        />
                        {clickedRegion && (
                            <div
                                className="absolute w-8 h-8 border-4 border-white rounded-full pointer-events-none"
                                style={{
                                    left: `${clickedRegion.x}%`,
                                    top: `${clickedRegion.y}%`,
                                    transform: 'translate(-50%, -50%)'
                                }}
                            />
                        )}
                    </div>

                    {clickedRegion && (
                        <motion.div
                            className="mt-4 p-4 bg-purple-500/20 border border-purple-400/30 rounded-lg"
                            initial={{ opacity: 0, height: 0 }}
                            animate={{ opacity: 1, height: "auto" }}
                        >
                            <div className="flex items-start gap-2">
                                <div className="text-2xl">🧠</div>
                                <div className="flex-1">
                                    <div className="flex items-baseline justify-between mb-2">
                                        <h6 className="text-white font-semibold">{clickedRegion.region}</h6>
                                        <span className="text-purple-300 text-sm font-bold">
                                            {clickedRegion.attention}% Attention
                                        </span>
                                    </div>
                                    {isLoading ? (
                                        <div className="flex items-center gap-2 text-white/60">
                                            <div className="w-4 h-4 border-2 border-purple-400 border-t-transparent rounded-full animate-spin" />
                                            <span>Generating AI explanation...</span>
                                        </div>
                                    ) : (
                                        <p className="text-white/80 text-sm leading-relaxed">
                                            {clickedRegion.explanation}
                                        </p>
                                    )}
                                </div>
                            </div>
                        </motion.div>
                    )}

                    {!clickedRegion && (
                        <p className="text-center text-white/60 text-sm mt-4">
                            Click any part of the image to explore!
                        </p>
                    )}
                </motion.div>
            )}
        </div>
    )
}
