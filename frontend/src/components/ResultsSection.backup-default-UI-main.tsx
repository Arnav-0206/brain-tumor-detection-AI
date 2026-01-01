import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Brain, CheckCircle, AlertTriangle, Clock, Download } from 'lucide-react'
import { PredictionResult } from '../App'
import { generatePDFReport } from '../utils/reportGenerator'
import { CollapsibleNarrative } from './CollapsibleNarrative'

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

            <div className="flex-1 flex items-center justify-center">
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
                    scale: { duration: 1, repeat: Infinity },
                }}
                className="mb-6"
            >
                <Brain size={64} className="text-purple-400 mx-auto" />
            </motion.div>
            <h4 className="text-white text-xl font-semibold mb-2">Analyzing MRI Scan</h4>
            <p className="text-white/60 mb-4">AI model is processing your image...</p>
            <div className="flex justify-center gap-2">
                <motion.div
                    className="w-2 h-2 bg-purple-400 rounded-full"
                    animate={{ scale: [1, 1.5, 1] }}
                    transition={{ duration: 1, repeat: Infinity, delay: 0 }}
                />
                <motion.div
                    className="w-2 h-2 bg-blue-400 rounded-full"
                    animate={{ scale: [1, 1.5, 1] }}
                    transition={{ duration: 1, repeat: Infinity, delay: 0.2 }}
                />
                <motion.div
                    className="w-2 h-2 bg-pink-400 rounded-full"
                    animate={{ scale: [1, 1.5, 1] }}
                    transition={{ duration: 1, repeat: Infinity, delay: 0.4 }}
                />
            </div>
        </motion.div>
    )
}

function EmptyState() {
    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="text-center text-white/40"
        >
            <Brain size={64} className="mx-auto mb-4 opacity-30" />
            <p className="text-lg">Upload an MRI scan to see results</p>
            <p className="text-sm mt-2">AI analysis will appear here</p>
        </motion.div>
    )
}

function ResultDisplay({ result }: { result: PredictionResult }) {
    const isTumor = result.prediction === 'tumor'
    const confidencePercent = (result.confidence * 100).toFixed(1)
    const confidence = result.confidence * 100

    // Determine animation based on confidence
    const getConfidenceAnimation = () => {
        if (confidence > 90) {
            // High confidence - subtle static glow (professional)
            return {
                boxShadow: `0 0 25px ${isTumor ? 'rgba(239, 68, 68, 0.4)' : 'rgba(34, 197, 94, 0.4)'}`
            }
        } else if (confidence >= 60) {
            // Medium confidence - very subtle pulse
            return {
                scale: [1, 1.01, 1],
                transition: { duration: 3, repeat: Infinity, ease: "easeInOut" }
            }
        } else {
            // Low confidence - subtle shake effect
            return {
                x: [0, -1, 1, -1, 1, 0],
                transition: { duration: 0.4, repeat: Infinity, repeatDelay: 2 }
            }
        }
    }

    return (
        <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.9 }}
            className="w-full space-y-6"
        >
            {/* Main Result with Dynamic Animation */}
            <motion.div
                className={`
          p-6 rounded-xl border-2 relative overflow-hidden
          ${isTumor
                        ? 'bg-red-500/10 border-red-500/50'
                        : 'bg-green-500/10 border-green-500/50'
                    }
        `}
                initial={{ scale: 0 }}
                animate={{
                    scale: 1,
                    ...getConfidenceAnimation()
                }}
                transition={{ type: "spring", duration: 0.6, delay: 0.2 }}
            >
                {/* Confidence Level Indicator */}
                <div className="absolute top-2 right-2">
                    {confidence > 90 ? (
                        <span className="px-2 py-1 bg-green-500/20 text-green-300 text-xs rounded-full font-bold">
                            ⚡ HIGH
                        </span>
                    ) : confidence >= 60 ? (
                        <span className="px-2 py-1 bg-yellow-500/20 text-yellow-300 text-xs rounded-full font-bold">
                            ⚠️ MEDIUM
                        </span>
                    ) : (
                        <span className="px-2 py-1 bg-red-500/20 text-red-300 text-xs rounded-full font-bold">
                            ⚠️ LOW
                        </span>
                    )}
                </div>

                <div className="flex items-center gap-4 mb-4">
                    {isTumor ? (
                        <AlertTriangle size={40} className="text-red-400" />
                    ) : (
                        <CheckCircle size={40} className="text-green-400" />
                    )}
                    <div>
                        <h4 className="text-2xl font-bold text-white">
                            {isTumor ? 'Tumor Detected' : 'No Tumor Detected'}
                        </h4>
                        <p className="text-white/70">
                            Confidence: <span className="font-bold">{confidencePercent}%</span>
                        </p>
                    </div>
                </div>

                {/* Confidence Bar */}
                <div className="w-full bg-white/10 rounded-full h-3 overflow-hidden">
                    <motion.div
                        className={`h-full rounded-full ${isTumor ? 'bg-red-500' : 'bg-green-500'}`}
                        initial={{ width: 0 }}
                        animate={{ width: `${confidencePercent}%` }}
                        transition={{ duration: 1, delay: 0.5 }}
                    />
                </div>
            </motion.div>

            {/* Tumor Type Classification */}
            {result.tumor_type && (
                <motion.div
                    className="p-5 glass-dark rounded-xl border border-purple-400/30"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.4 }}
                >
                    <div className="flex items-center gap-2 mb-3">
                        <div className="text-2xl">🧬</div>
                        <h5 className="text-white font-semibold">Tumor Classification</h5>
                    </div>

                    <div className="space-y-3">
                        {/* Type and Confidence */}
                        <div className="flex items-baseline justify-between">
                            <span className="text-lg font-bold text-purple-300">{result.tumor_type}</span>
                            <span className="text-sm text-white/70">
                                {(result.type_confidence! * 100).toFixed(1)}% confidence
                            </span>
                        </div>

                        {/* Description */}
                        {result.type_description && (
                            <p className="text-white/70 text-sm">{result.type_description}</p>
                        )}

                        {/* Characteristics */}
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
                    transition={{ delay: 0.5 }}
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
                                transition={{ delay: 0.6 + index * 0.1 }}
                            >
                                {/* Rank and Diagnosis Name */}
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
                                                        transition={{ duration: 0.8, delay: 0.7 + index * 0.1 }}
                                                    />
                                                </div>
                                                <span className="text-blue-300 text-sm font-bold min-w-[3rem] text-right">
                                                    {dx.likelihood}%
                                                </span>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                {/* Reasoning */}
                                <p className="text-white/70 text-sm mb-2 ml-8">{dx.reasoning}</p>

                                {/* Key Feature */}
                                <div className="flex items-center gap-2 ml-8">
                                    <span className="text-blue-400 text-xs">🔑</span>
                                    <span className="text-white/60 text-xs italic">{dx.key_feature}</span>
                                </div>
                            </motion.div>
                        ))}
                    </div>

                    <p className="text-white/50 text-xs mt-4 text-center">
                        AI-generated differential diagnosis • Requires clinical correlation
                    </p>
                </motion.div>
            )}

            {/* Risk Assessment */}
            {result.risk_assessment && (
                <motion.div
                    className={`p-5 glass-dark rounded-xl border-2 ${result.risk_assessment.severity_score >= 9 ? 'border-red-500/50' :
                        result.risk_assessment.severity_score >= 7 ? 'border-orange-500/50' :
                            result.risk_assessment.severity_score >= 4 ? 'border-yellow-500/50' :
                                'border-green-500/50'
                        }`}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.6 }}
                >
                    <div className="flex items-center gap-2 mb-4">
                        <div className="text-2xl">⚠️</div>
                        <h5 className="text-white font-semibold">Risk Assessment</h5>
                    </div>

                    {/* Severity Score */}
                    <div className="mb-4">
                        <div className="flex items-baseline justify-between mb-2">
                            <span className="text-white/80">Severity Score</span>
                            <span className={`text-2xl font-bold ${result.risk_assessment.severity_score >= 9 ? 'text-red-400' :
                                result.risk_assessment.severity_score >= 7 ? 'text-orange-400' :
                                    result.risk_assessment.severity_score >= 4 ? 'text-yellow-400' :
                                        'text-green-400'
                                }`}>
                                {result.risk_assessment.severity_score}/10
                            </span>
                        </div>

                        {/* Severity Bar */}
                        <div className="w-full bg-white/10 rounded-full h-4 overflow-hidden">
                            <motion.div
                                className={`h-full rounded-full ${result.risk_assessment.severity_score >= 9 ? 'bg-gradient-to-r from-red-600 to-red-400' :
                                    result.risk_assessment.severity_score >= 7 ? 'bg-gradient-to-r from-orange-600 to-orange-400' :
                                        result.risk_assessment.severity_score >= 4 ? 'bg-gradient-to-r from-yellow-600 to-yellow-400' :
                                            'bg-gradient-to-r from-green-600 to-green-400'
                                    }`}
                                initial={{ width: 0 }}
                                animate={{ width: `${(result.risk_assessment.severity_score / 10) * 100}%` }}
                                transition={{ duration: 1, delay: 0.7 }}
                            />
                        </div>

                        <p className="text-xs text-white/60 mt-1 text-center">
                            {result.risk_assessment.severity_score >= 9 ? 'Critical Risk' :
                                result.risk_assessment.severity_score >= 7 ? 'High Risk' :
                                    result.risk_assessment.severity_score >= 4 ? 'Moderate Risk' :
                                        'Low Risk'}
                        </p>
                    </div>

                    {/* Urgency Level */}
                    <div className="mb-4">
                        <div className="flex items-center justify-between">
                            <span className="text-white/80">Urgency Level</span>
                            <span className={`px-3 py-1 rounded-full font-bold text-sm ${result.risk_assessment.urgency_level === 'emergency' ? 'bg-red-500/20 text-red-300' :
                                result.risk_assessment.urgency_level === 'urgent' ? 'bg-orange-500/20 text-orange-300' :
                                    'bg-green-500/20 text-green-300'
                                }`}>
                                {result.risk_assessment.urgency_level === 'emergency' ? '🔴 EMERGENCY' :
                                    result.risk_assessment.urgency_level === 'urgent' ? '🟠 URGENT' :
                                        '🟢 ROUTINE'}
                            </span>
                        </div>
                    </div>

                    {/* Timeline */}
                    <div className="mb-4 p-3 bg-white/5 rounded-lg">
                        <p className="text-white/70 text-sm mb-1">
                            <span className="font-semibold text-white">Recommended Action:</span>
                        </p>
                        <p className="text-white text-sm">{result.risk_assessment.timeline}</p>
                    </div>

                    {/* Reasoning */}
                    <div className="p-3 bg-white/5 rounded-lg">
                        <p className="text-white/70 text-sm italic">
                            {result.risk_assessment.reasoning}
                        </p>
                    </div>
                </motion.div>
            )}

            {/* AI Narrative - Collapsible */}
            {result.narrative && (
                <CollapsibleNarrative narrative={result.narrative} />
            )}

            {/* Download Report Button */}
            <motion.button
                onClick={() => {
                    generatePDFReport({
                        prediction: result.prediction,
                        confidence: result.confidence,
                        timestamp: new Date().toISOString(),
                        processingTime: result.processingTime,
                        narrative: result.narrative,
                        modelInfo: {
                            name: 'EfficientNet-B4',
                            accuracy: 0.923,
                            dataset: '3,264 Brain MRI Scans (Kaggle)'
                        },
                        // New AI fields
                        tumor_type: result.tumor_type,
                        type_confidence: result.type_confidence,
                        type_characteristics: result.type_characteristics,
                        differential_diagnosis: result.differential_diagnosis,
                        risk_assessment: result.risk_assessment
                    })
                }}
                className="w-full py-3 rounded-xl font-semibold flex items-center justify-center gap-2
                    bg-gradient-to-r from-blue-500 to-purple-500 
                    hover:from-blue-600 hover:to-purple-600 
                    text-white shadow-lg hover:shadow-xl
                    transition-all duration-300"
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.5 }}
            >
                <Download size={20} />
                Download AI Report
            </motion.button>

            {/* Processing Time */}
            {result.processingTime && (
                <motion.div
                    className="flex items-center justify-center gap-2 text-white/60 text-sm"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.6 }}
                >
                    <Clock size={16} />
                    <span>Processed in {result.processingTime.toFixed(2)}s</span>
                </motion.div>
            )}

            {/* Interactive Grad-CAM */}
            {result.gradcamUrl && (
                <InteractiveGradCAM gradcamUrl={result.gradcamUrl} isTumor={isTumor} />
            )}
        </motion.div>
    )
}

// Interactive Grad-CAM Component
function InteractiveGradCAM({ gradcamUrl, isTumor }: { gradcamUrl: string; isTumor: boolean }) {
    const [clickedRegion, setClickedRegion] = useState<{
        x: number;
        y: number;
        region: string;
        attention: number;
        explanation: string;
    } | null>(null)
    const [isLoading, setIsLoading] = useState(false)

    const handleImageClick = async (e: React.MouseEvent<HTMLImageElement>) => {
        const rect = e.currentTarget.getBoundingClientRect()
        const relX = (e.clientX - rect.left) / rect.width
        const relY = (e.clientY - rect.top) / rect.height
        const displayX = relX * 100
        const displayY = relY * 100

        setIsLoading(true)

        try {
            // Call backend API
            const response = await fetch('/api/explain-region', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    x: relX,
                    y: relY,
                    prediction: isTumor ? 'tumor' : 'no_tumor',
                    confidence: 0.95 // TODO: Pass actual confidence
                })
            })

            if (!response.ok) {
                throw new Error('Failed to get region explanation')
            }

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
            // Fallback to simple message
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
        <motion.div
            className="p-4 glass-dark rounded-xl relative"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.8 }}
        >
            <h5 className="text-white font-semibold mb-3 flex items-center gap-2">
                <Brain size={20} className="text-purple-400" />
                Interactive Attention Heatmap
            </h5>

            {/* Prominent Call-to-Action Banner */}
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

            <motion.div
                className="relative border-4 border-transparent rounded-lg overflow-hidden"
                animate={{
                    borderColor: clickedRegion
                        ? ['rgba(167, 139, 250, 0)', 'rgba(167, 139, 250, 0)', 'rgba(167, 139, 250, 0)']
                        : ['rgba(167, 139, 250, 0.3)', 'rgba(96, 165, 250, 0.6)', 'rgba(167, 139, 250, 0.3)'],
                }}
                transition={{ duration: 2, repeat: Infinity }}
            >
                <img
                    src={gradcamUrl}
                    alt="Grad-CAM"
                    className="w-full rounded-lg cursor-pointer hover:opacity-90 transition-opacity"
                    onClick={handleImageClick}
                />
                {clickedRegion && (
                    <motion.div
                        className="absolute rounded-full w-8 h-8 border-4 border-white pointer-events-none"
                        style={{
                            left: `${clickedRegion.x}%`,
                            top: `${clickedRegion.y}%`,
                            transform: 'translate(-50%, -50%)'
                        }}
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        transition={{ type: "spring", duration: 0.3 }}
                    />
                )}
            </motion.div>

            {/* Region Explanation */}
            <AnimatePresence>
                {clickedRegion && (
                    <motion.div
                        className="mt-4 p-4 bg-purple-500/20 border border-purple-400/30 rounded-lg"
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: "auto" }}
                        exit={{ opacity: 0, height: 0 }}
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
                                        <motion.div
                                            animate={{ rotate: 360 }}
                                            transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                                            className="w-4 h-4 border-2 border-purple-400 border-t-transparent rounded-full"
                                        />
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
            </AnimatePresence>

            {!clickedRegion && (
                <motion.p
                    className="text-center text-white/60 text-sm mt-4 flex items-center justify-center gap-2"
                    animate={{ opacity: [0.6, 1, 0.6] }}
                    transition={{ duration: 2, repeat: Infinity }}
                >
                    <span className="text-yellow-400 text-lg">⚡</span>
                    <span>Click any part of the image above to start exploring!</span>
                    <span className="text-yellow-400 text-lg">⚡</span>
                </motion.p>
            )}
        </motion.div>
    )
}
