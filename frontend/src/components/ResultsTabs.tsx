import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { PredictionResult } from '../App'
import { OverviewTab } from './tabs/OverviewTab'
import { AnalysisTab } from './tabs/AnalysisTab'
import { DetailsTab } from './tabs/DetailsTab'

interface ResultsTabsProps {
    result: PredictionResult
}

type TabType = 'overview' | 'analysis' | 'details'

export function ResultsTabs({ result }: ResultsTabsProps) {
    const [activeTab, setActiveTab] = useState<TabType>('overview')

    const tabs = [
        { id: 'overview' as TabType, label: 'Overview', icon: '📊' },
        { id: 'analysis' as TabType, label: 'Analysis', icon: '🔬' },
        { id: 'details' as TabType, label: 'Details', icon: '📋' },
    ]

    return (
        <div className="w-full">
            {/* Tab Navigation */}
            <div className="flex gap-2 mb-6 p-1 bg-white/5 rounded-xl">
                {tabs.map((tab) => (
                    <button
                        key={tab.id}
                        onClick={() => setActiveTab(tab.id)}
                        className={`flex-1 flex items-center justify-center gap-2 px-4 py-3 rounded-lg font-semibold transition-all duration-300 ${activeTab === tab.id
                                ? 'bg-gradient-to-r from-purple-500 to-blue-500 text-white shadow-lg'
                                : 'text-white/60 hover:text-white/80 hover:bg-white/5'
                            }`}
                    >
                        <span className="text-xl">{tab.icon}</span>
                        <span>{tab.label}</span>
                    </button>
                ))}
            </div>

            {/* Tab Content */}
            <AnimatePresence mode="wait">
                <motion.div
                    key={activeTab}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -20 }}
                    transition={{ duration: 0.3 }}
                >
                    {activeTab === 'overview' && <OverviewTab result={result} />}
                    {activeTab === 'analysis' && <AnalysisTab result={result} />}
                    {activeTab === 'details' && <DetailsTab result={result} />}
                </motion.div>
            </AnimatePresence>
        </div>
    )
}
