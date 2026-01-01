import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { BarChart3, Clock, Database, Zap, X, TrendingUp } from 'lucide-react'

interface ModelMetrics {
    model_info: {
        name: string
        size_mb: number
        parameters: string
        input_size: string
    }
    performance: {
        accuracy: number
        precision: number
        recall: number
        f1_score: number
        roc_auc: number
        specificity: number
    }
    dataset: {
        total_samples: number
        train_samples: number
        val_samples: number
        test_samples: number
        train_split: string
        val_split: string
        test_split: string
    }
    inference: {
        avg_time_cpu: number
        avg_time_gpu: number
        device: string
    }
}

interface ModelDashboardProps {
    isOpen: boolean
    onClose: () => void
}

export default function ModelDashboard({ isOpen, onClose }: ModelDashboardProps) {
    const [metrics, setMetrics] = useState<ModelMetrics | null>(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        if (isOpen) {
            fetchMetrics()
        }
    }, [isOpen])

    const fetchMetrics = async () => {
        try {
            const response = await fetch('/api/metrics')
            const data = await response.json()
            setMetrics(data)
        } catch (error) {
            console.error('Failed to fetch metrics:', error)
        } finally {
            setLoading(false)
        }
    }

    if (!isOpen) return null

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
            <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.95 }}
                className="glass rounded-2xl p-6 max-w-4xl w-full max-h-[90vh] overflow-y-auto"
            >
                {/* Header */}
                <div className="flex items-center justify-between mb-6">
                    <div className="flex items-center gap-3">
                        <BarChart3 size={32} className="text-purple-400" />
                        <h2 className="text-3xl font-bold text-white">Model Performance Dashboard</h2>
                    </div>
                    <button
                        onClick={onClose}
                        className="p-2 hover:bg-white/10 rounded-full transition-colors"
                    >
                        <X size={24} className="text-white" />
                    </button>
                </div>

                {loading ? (
                    <div className="flex items-center justify-center py-12">
                        <div className="text-white text-lg">Loading metrics...</div>
                    </div>
                ) : metrics ? (
                    <div className="space-y-6">
                        {/* Performance Metrics */}
                        <section>
                            <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                                <TrendingUp size={20} className="text-green-400" />
                                Performance Metrics
                            </h3>
                            <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                                <MetricCard
                                    label="Accuracy"
                                    value={`${(metrics.performance.accuracy * 100).toFixed(1)}%`}
                                    color="green"
                                />
                                <MetricCard
                                    label="Precision"
                                    value={`${(metrics.performance.precision * 100).toFixed(1)}%`}
                                    color="blue"
                                />
                                <MetricCard
                                    label="Recall"
                                    value={`${(metrics.performance.recall * 100).toFixed(1)}%`}
                                    color="purple"
                                />
                                <MetricCard
                                    label="F1 Score"
                                    value={`${(metrics.performance.f1_score * 100).toFixed(1)}%`}
                                    color="pink"
                                />
                                <MetricCard
                                    label="ROC-AUC"
                                    value={`${(metrics.performance.roc_auc * 100).toFixed(1)}%`}
                                    color="yellow"
                                />
                                <MetricCard
                                    label="Specificity"
                                    value={`${(metrics.performance.specificity * 100).toFixed(1)}%`}
                                    color="cyan"
                                />
                            </div>
                        </section>

                        {/* Model Info */}
                        <section>
                            <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                                <Zap size={20} className="text-yellow-400" />
                                Model Information
                            </h3>
                            <div className="glass-dark rounded-xl p-4 grid grid-cols-2 gap-3">
                                <InfoItem label="Architecture" value={metrics.model_info.name} />
                                <InfoItem label="Parameters" value={metrics.model_info.parameters} />
                                <InfoItem label="Model Size" value={`${metrics.model_info.size_mb} MB`} />
                                <InfoItem label="Input Size" value={metrics.model_info.input_size} />
                            </div>
                        </section>

                        {/* Dataset Info */}
                        <section>
                            <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                                <Database size={20} className="text-blue-400" />
                                Dataset Information
                            </h3>
                            <div className="glass-dark rounded-xl p-4">
                                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                                    <div className="text-center">
                                        <div className="text-2xl font-bold text-white">{metrics.dataset.total_samples}</div>
                                        <div className="text-sm text-white/60">Total Samples</div>
                                    </div>
                                    <div className="text-center">
                                        <div className="text-2xl font-bold text-green-400">{metrics.dataset.train_samples}</div>
                                        <div className="text-sm text-white/60">Training ({metrics.dataset.train_split})</div>
                                    </div>
                                    <div className="text-center">
                                        <div className="text-2xl font-bold text-yellow-400">{metrics.dataset.val_samples}</div>
                                        <div className="text-sm text-white/60">Validation ({metrics.dataset.val_split})</div>
                                    </div>
                                    <div className="text-center">
                                        <div className="text-2xl font-bold text-blue-400">{metrics.dataset.test_samples}</div>
                                        <div className="text-sm text-white/60">Test ({metrics.dataset.test_split})</div>
                                    </div>
                                </div>
                                {/* Visual split bar */}
                                <div className="w-full h-8 rounded-full overflow-hidden flex">
                                    <div className="bg-green-500 flex items-center justify-center text-xs font-bold text-white" style={{ width: metrics.dataset.train_split }}>
                                        Train
                                    </div>
                                    <div className="bg-yellow-500 flex items-center justify-center text-xs font-bold text-white" style={{ width: metrics.dataset.val_split }}>
                                        Val
                                    </div>
                                    <div className="bg-blue-500 flex items-center justify-center text-xs font-bold text-white" style={{ width: metrics.dataset.test_split }}>
                                        Test
                                    </div>
                                </div>
                            </div>
                        </section>

                        {/* Inference Time */}
                        <section>
                            <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                                <Clock size={20} className="text-purple-400" />
                                Inference Performance
                            </h3>
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                                <div className="glass-dark rounded-xl p-4 text-center">
                                    <div className="text-3xl font-bold text-purple-400">{metrics.inference.avg_time_cpu}s</div>
                                    <div className="text-sm text-white/60 mt-1">CPU Inference</div>
                                </div>
                                <div className="glass-dark rounded-xl p-4 text-center">
                                    <div className="text-3xl font-bold text-green-400">{metrics.inference.avg_time_gpu}s</div>
                                    <div className="text-sm text-white/60 mt-1">GPU Inference</div>
                                </div>
                                <div className="glass-dark rounded-xl p-4 text-center">
                                    <div className="text-3xl font-bold text-blue-400">{metrics.inference.device}</div>
                                    <div className="text-sm text-white/60 mt-1">Current Device</div>
                                </div>
                            </div>
                        </section>
                    </div>
                ) : (
                    <div className="text-white text-center py-12">Failed to load metrics</div>
                )}
            </motion.div>
        </div>
    )
}

function MetricCard({ label, value, color }: { label: string; value: string; color: string }) {
    const colorClasses = {
        green: 'from-green-500 to-emerald-500',
        blue: 'from-blue-500 to-cyan-500',
        purple: 'from-purple-500 to-pink-500',
        pink: 'from-pink-500 to-rose-500',
        yellow: 'from-yellow-500 to-orange-500',
        cyan: 'from-cyan-500 to-teal-500',
    }

    return (
        <motion.div
            className="glass-dark rounded-xl p-4 text-center"
            whileHover={{ scale: 1.05 }}
            transition={{ duration: 0.2 }}
        >
            <div className={`text-3xl font-bold bg-gradient-to-r ${colorClasses[color as keyof typeof colorClasses]} bg-clip-text text-transparent`}>
                {value}
            </div>
            <div className="text-sm text-white/60 mt-1">{label}</div>
        </motion.div>
    )
}

function InfoItem({ label, value }: { label: string; value: string }) {
    return (
        <div>
            <div className="text-xs text-white/50 mb-1">{label}</div>
            <div className="text-white font-semibold">{value}</div>
        </div>
    )
}
