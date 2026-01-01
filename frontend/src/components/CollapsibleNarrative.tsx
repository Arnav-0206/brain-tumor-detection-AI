// Collapsible Narrative Component
import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Zap, ChevronDown } from 'lucide-react'

interface CollapsibleNarrativeProps {
    narrative: string
}

export function CollapsibleNarrative({ narrative }: CollapsibleNarrativeProps) {
    const [isExpanded, setIsExpanded] = useState(false)

    // Extract summary (first sentence or up to first period + space)
    const getSummary = () => {
        const sentences = narrative.split('. ')
        // Get first 2 sentences for summary
        return sentences.slice(0, 2).join('. ') + (sentences.length > 2 ? '.' : '')
    }

    // Parse narrative into sections
    const sections = narrative.split('**').filter(s => s.trim())

    return (
        <motion.div
            className="glass-dark rounded-xl overflow-hidden"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
        >
            {/* Header */}
            <div className="p-4 border-b border-white/10">
                <div className="flex items-center gap-2 mb-2">
                    <Zap size={20} className="text-yellow-400" />
                    <h5 className="text-white font-semibold">AI Explanation</h5>
                </div>

                {/* Summary - Always Visible */}
                <p className="text-white/80 text-sm leading-relaxed mb-3">
                    {getSummary()}
                </p>

                {/* Expand Button */}
                <button
                    onClick={() => setIsExpanded(!isExpanded)}
                    className="flex items-center gap-2 text-purple-300 hover:text-purple-200 text-sm font-medium transition-colors group"
                >
                    <span>{isExpanded ? 'Show less' : 'Read detailed analysis'}</span>
                    <motion.div
                        animate={{ rotate: isExpanded ? 180 : 0 }}
                        transition={{ duration: 0.3 }}
                    >
                        <ChevronDown size={16} className="group-hover:translate-y-0.5 transition-transform" />
                    </motion.div>
                </button>
            </div>

            {/* Expandable Full Content */}
            <AnimatePresence>
                {isExpanded && (
                    <motion.div
                        initial={{ height: 0, opacity: 0 }}
                        animate={{ height: "auto", opacity: 1 }}
                        exit={{ height: 0, opacity: 0 }}
                        transition={{ duration: 0.3 }}
                        className="overflow-hidden"
                    >
                        <div className="p-4 space-y-4 border-t border-white/5">
                            <div className="flex items-center gap-2 mb-2">
                                <div className="h-1 w-1 rounded-full bg-purple-400"></div>
                                <span className="text-purple-300 text-xs font-semibold uppercase tracking-wide">Detailed Analysis</span>
                            </div>

                            {sections.map((section, index) => {
                                // Skip empty sections
                                if (!section.trim()) return null

                                // Check if this is a section header (ends with :)
                                const parts = section.split(':')
                                if (parts.length > 1 && parts[0].length < 50) {
                                    // This is a section with header
                                    return (
                                        <div key={index} className="border-l-2 border-purple-400/30 pl-4">
                                            <h6 className="text-purple-300 font-semibold mb-2">
                                                {parts[0]}:
                                            </h6>
                                            <p className="text-white/80 text-sm leading-relaxed">
                                                {parts.slice(1).join(':').trim()}
                                            </p>
                                        </div>
                                    )
                                } else {
                                    // Regular paragraph
                                    return (
                                        <p key={index} className="text-white/80 text-sm leading-relaxed">
                                            {section.trim()}
                                        </p>
                                    )
                                }
                            })}
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </motion.div>
    )
}
