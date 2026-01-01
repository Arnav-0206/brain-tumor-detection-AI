import { motion } from 'framer-motion'
import { AlertTriangle, CheckCircle, Download, Clock } from 'lucide-react'
import { PredictionResult } from '../../App'
import { generatePDFReport } from '../../utils/reportGenerator'

interface OverviewTabProps {
    result: PredictionResult
}

export function OverviewTab({ result }: OverviewTabProps) {
    const isTumor = result.prediction === 'tumor'
    const confidencePercent = (result.confidence * 100).toFixed(1)

    return (
        <div className="space-y-6">
            {/* Main Result Card  */}
            <motion.div
                className={`
                    p-6 rounded-xl border-2 relative overflow-hidden
                    ${isTumor
                        ? 'bg-red-500/10 border-red-500/50'
                        : 'bg-green-500/10 border-green-500/50'
                    }
                `}
                initial={{ scale: 0.95 }}
                animate={{ scale: 1 }}
                transition={{ type: "spring", duration: 0.5 }}
            >
                <div className="flex items-center gap-4 mb-4">
                    {isTumor ? (
                        <AlertTriangle size={48} className="text-red-400" />
                    ) : (
                        <CheckCircle size={48} className="text-green-400" />
                    )}
                    <div className="flex-1">
                        <h3 className="text-3xl font-bold text-white mb-2">
                            {isTumor ? 'Tumor Detected' : 'No Tumor Detected'}
                        </h3>
                        <p className="text-white/70 text-lg">
                            Confidence: <span className="font-bold text-white">{confidencePercent}%</span>
                        </p>
                    </div>
                </div>

                {/* Confidence Bar */}
                <div className="w-full bg-white/10 rounded-full h-4 overflow-hidden">
                    <motion.div
                        className={`h-full rounded-full ${isTumor ? 'bg-red-500' : 'bg-green-500'}`}
                        initial={{ width: 0 }}
                        animate={{ width: `${confidencePercent}%` }}
                        transition={{ duration: 1, delay: 0.2 }}
                    />
                </div>
            </motion.div>

            {/* Risk Summary - Prominent If Tumor */}
            {result.risk_assessment && (
                <motion.div
                    className={`p-5 rounded-xl border-2 ${result.risk_assessment.severity_score >= 7
                            ? 'bg-red-500/10 border-red-500/50'
                            : result.risk_assessment.severity_score >= 4
                                ? 'bg-yellow-500/10 border-yellow-500/50'
                                : 'bg-green-500/10 border-green-500/50'
                        }`}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.3 }}
                >
                    <div className="flex items-start justify-between mb-3">
                        <div>
                            <h4 className="text-white font-bold text-xl mb-1">Risk Assessment</h4>
                            <p className={`text-2xl font-bold ${result.risk_assessment.severity_score >= 7 ? 'text-red-400' :
                                    result.risk_assessment.severity_score >= 4 ? 'text-yellow-400' : 'text-green-400'
                                }`}>
                                {result.risk_assessment.severity_score}/10
                                <span className="text-sm ml-2 text-white/60">
                                    {result.risk_assessment.severity_score >= 7 ? 'High Risk' :
                                        result.risk_assessment.severity_score >= 4 ? 'Moderate Risk' : 'Low Risk'}
                                </span>
                            </p>
                        </div>
                        <span className={`px-4 py-2 rounded-full font-bold ${result.risk_assessment.urgency_level === 'emergency' ? 'bg-red-500/20 text-red-300' :
                                result.risk_assessment.urgency_level === 'urgent' ? 'bg-orange-500/20 text-orange-300' :
                                    'bg-green-500/20 text-green-300'
                            }`}>
                            {result.risk_assessment.urgency_level === 'emergency' ? '🔴 EMERGENCY' :
                                result.risk_assessment.urgency_level === 'urgent' ? '🟠 URGENT' :
                                    '🟢 ROUTINE'}
                        </span>
                    </div>

                    <div className="p-3 bg-white/5 rounded-lg mb-3">
                        <p className="text-white/70 text-sm mb-1">
                            <span className="font-semibold text-white">Recommended Action:</span>
                        </p>
                        <p className="text-white font-medium">{result.risk_assessment.timeline}</p>
                    </div>

                    <p className="text-white/60 text-sm italic">{result.risk_assessment.reasoning}</p>
                </motion.div>
            )}

            {/* Quick Stats */}
            <div className="grid grid-cols-2 gap-4">
                {result.tumor_type && (
                    <motion.div
                        className="p-4 glass-dark rounded-xl"
                        initial={{ opacity: 0, scale: 0.9 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ delay: 0.4 }}
                    >
                        <p className="text-white/60 text-sm mb-1">Tumor Type</p>
                        <p className="text-white font-bold text-lg">{result.tumor_type}</p>
                        <p className="text-purple-300 text-sm">
                            {((result.type_confidence || 0) * 100).toFixed(1)}% confidence
                        </p>
                    </motion.div>
                )}

                {result.processingTime && (
                    <motion.div
                        className="p-4 glass-dark rounded-xl"
                        initial={{ opacity: 0, scale: 0.9 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ delay: 0.5 }}
                    >
                        <div className="flex items-center gap-2 mb-1">
                            <Clock size={16} className="text-white/60" />
                            <p className="text-white/60 text-sm">Processing Time</p>
                        </div>
                        <p className="text-white font-bold text-lg">{result.processingTime.toFixed(2)}s</p>
                    </motion.div>
                )}
            </div>

            {/* Download Report Button - Prominent */}
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
                        tumor_type: result.tumor_type,
                        type_confidence: result.type_confidence,
                        type_characteristics: result.type_characteristics,
                        differential_diagnosis: result.differential_diagnosis,
                        risk_assessment: result.risk_assessment
                    })
                }}
                className="w-full py-4 rounded-xl font-bold text-lg flex items-center justify-center gap-3
                    bg-gradient-to-r from-blue-500 to-purple-500 
                    hover:from-blue-600 hover:to-purple-600 
                    text-white shadow-lg hover:shadow-xl
                    transition-all duration-300"
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.6 }}
            >
                <Download size={24} />
                Download Complete Medical Report
            </motion.button>
        </div>
    )
}
