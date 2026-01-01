import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { X, TrendingDown, TrendingUp } from 'lucide-react'

interface TrainingSimulationProps {
    isOpen: boolean
    onClose: () => void
}

export default function TrainingSimulation({ isOpen, onClose }: TrainingSimulationProps) {
    const [currentEpoch, setCurrentEpoch] = useState(0)
    const [isPlaying, setIsPlaying] = useState(false)
    const maxEpochs = 25

    // Generate training data (simulated realistic training curves)
    const generateTrainingData = (epoch: number) => {
        const data = []
        for (let i = 0; i <= epoch; i++) {
            // Realistic loss curve - exponential decay with some noise
            const trainLoss = 0.7 * Math.exp(-i / 8) + 0.05 + Math.random() * 0.03
            const valLoss = 0.7 * Math.exp(-i / 8) + 0.08 + Math.random() * 0.05

            // Realistic accuracy curve - logarithmic growth
            const trainAcc = 0.92 - 0.5 * Math.exp(-i / 5) + Math.random() * 0.02
            const valAcc = 0.92 - 0.5 * Math.exp(-i / 5) - 0.03 + Math.random() * 0.03

            data.push({
                epoch: i + 1,
                trainLoss: Math.max(0.05, trainLoss),
                valLoss: Math.max(0.08, valLoss),
                trainAcc: Math.min(0.98, trainAcc),
                valAcc: Math.min(0.95, valAcc)
            })
        }
        return data
    }

    const [trainingData, setTrainingData] = useState(generateTrainingData(0))

    useEffect(() => {
        if (isOpen && !isPlaying) {
            setIsPlaying(true)
            setCurrentEpoch(0)
        }
    }, [isOpen])

    useEffect(() => {
        if (isPlaying && currentEpoch < maxEpochs) {
            const timer = setTimeout(() => {
                setCurrentEpoch(prev => prev + 1)
                setTrainingData(generateTrainingData(currentEpoch + 1))
            }, 150) // Fast animation

            return () => clearTimeout(timer)
        } else if (currentEpoch >= maxEpochs) {
            setIsPlaying(false)
        }
    }, [isPlaying, currentEpoch])

    const handleRestart = () => {
        setCurrentEpoch(0)
        setIsPlaying(true)
        setTrainingData(generateTrainingData(0))
    }

    if (!isOpen) return null

    const currentData = trainingData[trainingData.length - 1]

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
            <motion.div
                initial={{ opacity: 0, scale: 0.95, y: 20 }}
                animate={{ opacity: 1, scale: 1, y: 0 }}
                exit={{ opacity: 0, scale: 0.95, y: 20 }}
                className="glass rounded-2xl p-6 max-w-5xl w-full max-h-[90vh] overflow-y-auto"
            >
                {/* Header */}
                <div className="flex items-center justify-between mb-6">
                    <div>
                        <h2 className="text-3xl font-bold text-white flex items-center gap-2">
                            🧠 Training Simulation
                        </h2>
                        <p className="text-white/60 text-sm mt-1">
                            EfficientNet-B4 model training visualization
                        </p>
                    </div>
                    <button
                        onClick={onClose}
                        className="p-2 hover:bg-white/10 rounded-full transition-colors"
                    >
                        <X size={24} className="text-white" />
                    </button>
                </div>

                {/* Training Info Banner */}
                <div className="glass-dark rounded-xl p-4 mb-6">
                    <div className="flex items-center justify-between mb-2">
                        <div className="text-white font-semibold">Training Configuration</div>
                        <div className={`px-3 py-1 rounded-full text-sm font-bold ${isPlaying ? 'bg-green-500/20 text-green-300' : 'bg-blue-500/20 text-blue-300'
                            }`}>
                            {isPlaying ? `⚡ Training... Epoch ${currentEpoch}/${maxEpochs}` : '✓ Complete'}
                        </div>
                    </div>
                    <p className="text-white/70 text-sm">
                        Model trained on <span className="font-bold text-purple-300">70/15/15 split</span> over{' '}
                        <span className="font-bold text-blue-300">{maxEpochs} epochs</span> with{' '}
                        <span className="font-bold text-green-300">data augmentation</span> and{' '}
                        <span className="font-bold text-pink-300">early stopping</span>.
                    </p>
                </div>

                {/* Current Metrics */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                    <MetricCard
                        icon={<TrendingDown />}
                        label="Train Loss"
                        value={currentData?.trainLoss.toFixed(4) || '0.0000'}
                        color="red"
                    />
                    <MetricCard
                        icon={<TrendingDown />}
                        label="Val Loss"
                        value={currentData?.valLoss.toFixed(4) || '0.0000'}
                        color="orange"
                    />
                    <MetricCard
                        icon={<TrendingUp />}
                        label="Train Acc"
                        value={currentData ? `${(currentData.trainAcc * 100).toFixed(1)}%` : '0%'}
                        color="green"
                    />
                    <MetricCard
                        icon={<TrendingUp />}
                        label="Val Acc"
                        value={currentData ? `${(currentData.valAcc * 100).toFixed(1)}%` : '0%'}
                        color="blue"
                    />
                </div>

                {/* Loss Chart */}
                <div className="glass-dark rounded-xl p-4 mb-4">
                    <h3 className="text-white font-semibold mb-3 flex items-center gap-2">
                        <TrendingDown size={20} className="text-red-400" />
                        Training & Validation Loss
                    </h3>
                    <ResponsiveContainer width="100%" height={200}>
                        <LineChart data={trainingData}>
                            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                            <XAxis
                                dataKey="epoch"
                                stroke="rgba(255,255,255,0.5)"
                                label={{ value: 'Epoch', position: 'insideBottom', offset: -5, fill: 'rgba(255,255,255,0.7)' }}
                            />
                            <YAxis
                                stroke="rgba(255,255,255,0.5)"
                                label={{ value: 'Loss', angle: -90, position: 'insideLeft', fill: 'rgba(255,255,255,0.7)' }}
                            />
                            <Tooltip
                                contentStyle={{ backgroundColor: 'rgba(30, 30, 50, 0.95)', border: '1px solid rgba(139, 92, 246, 0.5)', borderRadius: '8px' }}
                                labelStyle={{ color: 'white' }}
                            />
                            <Legend />
                            <Line
                                type="monotone"
                                dataKey="trainLoss"
                                stroke="#ef4444"
                                strokeWidth={2}
                                name="Training Loss"
                                dot={false}
                            />
                            <Line
                                type="monotone"
                                dataKey="valLoss"
                                stroke="#f97316"
                                strokeWidth={2}
                                name="Validation Loss"
                                dot={false}
                            />
                        </LineChart>
                    </ResponsiveContainer>
                </div>

                {/* Accuracy Chart */}
                <div className="glass-dark rounded-xl p-4 mb-4">
                    <h3 className="text-white font-semibold mb-3 flex items-center gap-2">
                        <TrendingUp size={20} className="text-green-400" />
                        Training & Validation Accuracy
                    </h3>
                    <ResponsiveContainer width="100%" height={200}>
                        <LineChart data={trainingData}>
                            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                            <XAxis
                                dataKey="epoch"
                                stroke="rgba(255,255,255,0.5)"
                                label={{ value: 'Epoch', position: 'insideBottom', offset: -5, fill: 'rgba(255,255,255,0.7)' }}
                            />
                            <YAxis
                                stroke="rgba(255,255,255,0.5)"
                                domain={[0.4, 1.0]}
                                label={{ value: 'Accuracy', angle: -90, position: 'insideLeft', fill: 'rgba(255,255,255,0.7)' }}
                            />
                            <Tooltip
                                contentStyle={{ backgroundColor: 'rgba(30, 30, 50, 0.95)', border: '1px solid rgba(139, 92, 246, 0.5)', borderRadius: '8px' }}
                                labelStyle={{ color: 'white' }}
                            />
                            <Legend />
                            <Line
                                type="monotone"
                                dataKey="trainAcc"
                                stroke="#22c55e"
                                strokeWidth={2}
                                name="Training Accuracy"
                                dot={false}
                            />
                            <Line
                                type="monotone"
                                dataKey="valAcc"
                                stroke="#3b82f6"
                                strokeWidth={2}
                                name="Validation Accuracy"
                                dot={false}
                            />
                        </LineChart>
                    </ResponsiveContainer>
                </div>

                {/* Control Button */}
                {!isPlaying && currentEpoch >= maxEpochs && (
                    <motion.button
                        onClick={handleRestart}
                        className="w-full py-3 rounded-xl font-semibold bg-gradient-to-r from-purple-500 to-blue-500 hover:from-purple-600 hover:to-blue-600 text-white transition-all"
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                    >
                        🔄 Replay Training
                    </motion.button>
                )}
            </motion.div>
        </div>
    )
}

function MetricCard({ icon, label, value, color }: { icon: React.ReactNode; label: string; value: string; color: string }) {
    const colorClasses: { [key: string]: string } = {
        red: 'from-red-500 to-rose-500',
        orange: 'from-orange-500 to-amber-500',
        green: 'from-green-500 to-emerald-500',
        blue: 'from-blue-500 to-cyan-500',
    }

    return (
        <div className="glass-dark rounded-xl p-4">
            <div className="flex items-center gap-2 text-white/60 mb-1">
                {icon}
                <span className="text-sm">{label}</span>
            </div>
            <div className={`text-2xl font-bold bg-gradient-to-r ${colorClasses[color]} bg-clip-text text-transparent`}>
                {value}
            </div>
        </div>
    )
}
