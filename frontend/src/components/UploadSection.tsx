import { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { motion, AnimatePresence } from 'framer-motion'
import { Upload, Image as ImageIcon, X, Loader2 } from 'lucide-react'

interface UploadSectionProps {
    onPredict: (file: File) => void
    isLoading: boolean
    onReset: () => void
}

export default function UploadSection({ onPredict, isLoading, onReset }: UploadSectionProps) {
    const [selectedFile, setSelectedFile] = useState<File | null>(null)
    const [preview, setPreview] = useState<string | null>(null)

    const onDrop = useCallback((acceptedFiles: File[]) => {
        const file = acceptedFiles[0]
        if (file) {
            setSelectedFile(file)

            // Create preview
            const reader = new FileReader()
            reader.onloadend = () => {
                setPreview(reader.result as string)
            }
            reader.readAsDataURL(file)
        }
    }, [])

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: {
            'image/*': ['.png', '.jpg', '.jpeg']
        },
        multiple: false,
        disabled: isLoading
    })

    const handleClear = () => {
        setSelectedFile(null)
        setPreview(null)
        onReset() // Also clear results
    }

    const handleAnalyze = () => {
        if (selectedFile) {
            onPredict(selectedFile)
        }
    }

    return (
        <div className="glass rounded-2xl p-8 h-full flex flex-col">
            <h3 className="text-2xl font-bold text-white mb-6 flex items-center gap-2">
                <Upload size={28} className="text-purple-400" />
                Upload MRI Scan
            </h3>

            {/* Dropzone */}
            <div className="flex-1">
                <AnimatePresence mode="wait">
                    {!preview ? (
                        <motion.div
                            key="dropzone"
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            {...(getRootProps() as any)}
                            className={`
                border-2 border-dashed rounded-xl p-12 h-full
                flex flex-col items-center justify-center
                cursor-pointer transition-all duration-300
                ${isDragActive
                                    ? 'border-purple-400 bg-purple-500/10'
                                    : 'border-white/30 hover:border-purple-400/50 hover:bg-white/5'
                                }
              `}
                        >
                            <input {...getInputProps()} />
                            <motion.div
                                animate={isDragActive ? { scale: 1.1 } : { scale: 1 }}
                                transition={{ duration: 0.2 }}
                            >
                                <ImageIcon size={64} className="text-white/40 mb-4" />
                            </motion.div>
                            <p className="text-white text-lg font-semibold mb-2">
                                {isDragActive ? 'Drop the MRI scan here' : 'Drag & drop MRI scan'}
                            </p>
                            <p className="text-white/60 text-sm">
                                or click to browse (PNG, JPG, JPEG)
                            </p>
                        </motion.div>
                    ) : (
                        <motion.div
                            key="preview"
                            initial={{ opacity: 0, scale: 0.9 }}
                            animate={{ opacity: 1, scale: 1 }}
                            exit={{ opacity: 0, scale: 0.9 }}
                            className="relative h-full"
                        >
                            <img
                                src={preview}
                                alt="Preview"
                                className="w-full h-full object-contain rounded-xl"
                            />
                            {!isLoading && (
                                <button
                                    onClick={handleClear}
                                    className="absolute top-4 right-4 p-2 bg-red-500/80 hover:bg-red-500 rounded-full text-white transition-colors"
                                >
                                    <X size={20} />
                                </button>
                            )}
                        </motion.div>
                    )}
                </AnimatePresence>
            </div>

            {/* Action Button */}
            <motion.button
                onClick={handleAnalyze}
                disabled={!selectedFile || isLoading}
                className={`
          mt-6 w-full py-4 rounded-xl font-semibold text-lg
          transition-all duration-300 flex items-center justify-center gap-2
          ${selectedFile && !isLoading
                        ? 'bg-gradient-to-r from-purple-500 to-blue-500 hover:from-purple-600 hover:to-blue-600 text-white shadow-lg hover:shadow-xl'
                        : 'bg-white/10 text-white/40 cursor-not-allowed'
                    }
        `}
                whileHover={selectedFile && !isLoading ? { scale: 1.02 } : {}}
                whileTap={selectedFile && !isLoading ? { scale: 0.98 } : {}}
            >
                {isLoading ? (
                    <>
                        <Loader2 size={24} className="animate-spin" />
                        Analyzing...
                    </>
                ) : (
                    <>
                        <Sparkles size={24} />
                        Analyze Scan
                    </>
                )}
            </motion.button>
        </div >
    )
}

// Mini component for sparkle icon
function Sparkles({ size }: { size: number }) {
    return (
        <svg width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 2L14 10L22 12L14 14L12 22L10 14L2 12L10 10L12 2Z" fill="currentColor" />
        </svg>
    )
}
