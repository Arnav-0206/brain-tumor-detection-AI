/**
 * Generate a professional comprehensive PDF report for AI analysis
 * Includes all AI findings: tumor type, differential diagnosis, risk assessment
 */

import { jsPDF } from 'jspdf'

export interface ReportData {
    prediction: 'tumor' | 'no_tumor'
    confidence: number
    timestamp: string
    processingTime?: number
    narrative?: string
    modelInfo: {
        name: string
        accuracy: number
        dataset: string
    }
    // New AI fields
    tumor_type?: string
    type_confidence?: number
    type_characteristics?: string[]
    differential_diagnosis?: Array<{
        diagnosis: string
        likelihood: number
        reasoning: string
    }>
    risk_assessment?: {
        severity_score: number
        urgency_level: string
        timeline: string
        reasoning: string
    }
}

export function generatePDFReport(data: ReportData) {
    const doc = new jsPDF()
    const confidencePercent = (data.confidence * 100).toFixed(1)
    const date = new Date().toLocaleString()
    const reportId = `NS-${Date.now()}`

    let yPos = 20
    const pageWidth = doc.internal.pageSize.width
    const pageHeight = doc.internal.pageSize.height
    const margin = 20
    const contentWidth = pageWidth - (2 * margin)

    // Helper function to add text with word wrap
    const addText = (text: string, x: number, y: number, options: any = {}) => {
        const lines = doc.splitTextToSize(text, options.maxWidth || contentWidth)
        doc.text(lines, x, y)
        return y + (lines.length * (options.lineHeight || 6))
    }

    // Helper to check page break
    const checkPageBreak = (requiredSpace: number) => {
        if (yPos + requiredSpace > pageHeight - 30) {
            doc.addPage()
            yPos = 20
            return true
        }
        return false
    }

    // Helper to add section header
    const addSectionHeader = (title: string, color: [number, number, number]) => {
        checkPageBreak(15)
        doc.setFillColor(color[0], color[1], color[2])
        doc.rect(margin, yPos, contentWidth, 8, 'F')
        doc.setTextColor(255, 255, 255)
        doc.setFontSize(12)
        doc.setFont('helvetica', 'bold')
        doc.text(title, margin + 3, yPos + 5.5)
        yPos += 12
    }

    // ========== HEADER ==========
    doc.setFillColor(88, 28, 135) // Purple
    doc.rect(0, 0, pageWidth, 40, 'F')

    doc.setTextColor(255, 255, 255)
    doc.setFontSize(26)
    doc.setFont('helvetica', 'bold')
    doc.text('NEUROSCAN AI', pageWidth / 2, 18, { align: 'center' })

    doc.setFontSize(11)
    doc.setFont('helvetica', 'normal')
    doc.text('Medical AI Brain Imaging Analysis Report', pageWidth / 2, 30, { align: 'center' })

    yPos = 50

    // ========== REPORT METADATA ==========
    doc.setFontSize(8)
    doc.setTextColor(100, 100, 100)
    doc.setFont('helvetica', 'italic')
    doc.text(`Generated: ${date}`, margin, yPos)
    doc.text(`Report ID: ${reportId}`, pageWidth - margin, yPos, { align: 'right' })
    yPos += 8

    // Divider
    doc.setDrawColor(200, 200, 200)
    doc.setLineWidth(0.3)
    doc.line(margin, yPos, pageWidth - margin, yPos)
    yPos += 12

    // ========== PRIMARY FINDING ==========
    addSectionHeader('PRIMARY FINDING', [139, 92, 246])

    const resultColor: [number, number, number] = data.prediction === 'tumor' ? [220, 38, 38] : [34, 197, 94]
    doc.setFontSize(14)
    doc.setFont('helvetica', 'bold')
    doc.setTextColor(resultColor[0], resultColor[1], resultColor[2])
    doc.text(data.prediction === 'tumor' ? '● TUMOR DETECTED' : '● NO TUMOR DETECTED', margin + 3, yPos)
    yPos += 8

    doc.setFontSize(10)
    doc.setTextColor(60, 60, 60)
    doc.setFont('helvetica', 'normal')
    doc.text(`Detection Confidence: ${confidencePercent}% (${data.confidence > 0.9 ? 'HIGH' : data.confidence >= 0.6 ? 'MEDIUM' : 'LOW'})`, margin + 3, yPos)
    if (data.processingTime) {
        yPos += 5
        doc.text(`Processing Time: ${data.processingTime.toFixed(2)} seconds`, margin + 3, yPos)
    }
    yPos += 10

    // ========== TUMOR CLASSIFICATION ==========
    if (data.tumor_type) {
        addSectionHeader('TUMOR CLASSIFICATION', [168, 85, 247])

        doc.setFontSize(11)
        doc.setFont('helvetica', 'bold')
        doc.setTextColor(168, 85, 247)
        doc.text(`Type: ${data.tumor_type}`, margin + 3, yPos)
        yPos += 6

        doc.setFontSize(9)
        doc.setFont('helvetica', 'normal')
        doc.setTextColor(60, 60, 60)
        const typeConf = data.type_confidence ? (data.type_confidence * 100).toFixed(1) : '0'
        doc.text(`Classification Confidence: ${typeConf}%`, margin + 3, yPos)
        yPos += 8

        if (data.type_characteristics && data.type_characteristics.length > 0) {
            doc.setFont('helvetica', 'bold')
            doc.text('Key Characteristics:', margin + 3, yPos)
            yPos += 5

            doc.setFont('helvetica', 'normal')
            data.type_characteristics.forEach(char => {
                checkPageBreak(8)
                doc.text(`• ${char}`, margin + 6, yPos)
                yPos += 5
            })
        }
        yPos += 5
    }

    // ========== DIFFERENTIAL DIAGNOSIS ==========
    if (data.differential_diagnosis && data.differential_diagnosis.length > 0) {
        addSectionHeader('DIFFERENTIAL DIAGNOSIS', [59, 130, 246])

        data.differential_diagnosis.forEach((dx, index) => {
            checkPageBreak(15)

            doc.setFontSize(10)
            doc.setFont('helvetica', 'bold')
            doc.setTextColor(59, 130, 246)
            doc.text(`${index + 1}. ${dx.diagnosis} (${dx.likelihood}%)`, margin + 3, yPos)
            yPos += 5

            doc.setFontSize(9)
            doc.setFont('helvetica', 'normal')
            doc.setTextColor(60, 60, 60)
            yPos = addText(dx.reasoning, margin + 6, yPos, { maxWidth: contentWidth - 9, lineHeight: 4.5 })
            yPos += 3
        })
        yPos += 5
    }

    // ========== RISK ASSESSMENT ==========
    if (data.risk_assessment) {
        const risk = data.risk_assessment
        const riskColor: [number, number, number] =
            risk.severity_score >= 9 ? [220, 38, 38] : // Red
                risk.severity_score >= 7 ? [249, 115, 22] : // Orange
                    risk.severity_score >= 4 ? [234, 179, 8] : // Yellow
                        [34, 197, 94] // Green

        addSectionHeader('RISK ASSESSMENT', riskColor)

        // Severity Score
        doc.setFontSize(11)
        doc.setFont('helvetica', 'bold')
        doc.setTextColor(riskColor[0], riskColor[1], riskColor[2])
        const riskLabel = risk.severity_score >= 9 ? 'CRITICAL RISK' :
            risk.severity_score >= 7 ? 'HIGH RISK' :
                risk.severity_score >= 4 ? 'MODERATE RISK' : 'LOW RISK'
        doc.text(`Severity: ${risk.severity_score}/10 - ${riskLabel}`, margin + 3, yPos)
        yPos += 8

        // Urgency
        doc.setFontSize(10)
        doc.setFont('helvetica', 'normal')
        doc.setTextColor(60, 60, 60)
        doc.text(`Urgency Level: ${risk.urgency_level.toUpperCase()}`, margin + 3, yPos)
        yPos += 5

        // Timeline
        doc.setFont('helvetica', 'bold')
        doc.text('Recommended Action:', margin + 3, yPos)
        yPos += 5
        doc.setFont('helvetica', 'normal')
        yPos = addText(risk.timeline, margin + 3, yPos, { maxWidth: contentWidth - 6, lineHeight: 4.5 })
        yPos += 5

        // Reasoning
        doc.setFont('helvetica', 'italic')
        doc.setTextColor(80, 80, 80)
        yPos = addText(risk.reasoning, margin + 3, yPos, { maxWidth: contentWidth - 6, lineHeight: 4.5 })
        yPos += 8
    }

    // ========== AI MEDICAL ANALYSIS ==========
    if (data.narrative) {
        addSectionHeader('AI MEDICAL ANALYSIS', [139, 92, 246])

        doc.setFontSize(9)
        doc.setTextColor(40, 40, 40)
        doc.setFont('helvetica', 'normal')

        const sections = data.narrative.split('**').filter(s => s.trim())

        sections.forEach((section) => {
            checkPageBreak(20)

            const parts = section.split(':')
            if (parts.length > 1 && parts[0].length < 50) {
                // Section header
                doc.setFont('helvetica', 'bold')
                doc.setTextColor(88, 28, 135)
                yPos = addText(parts[0] + ':', margin + 3, yPos, { maxWidth: contentWidth - 6, lineHeight: 5 })
                yPos += 2

                // Section content
                doc.setFont('helvetica', 'normal')
                doc.setTextColor(50, 50, 50)
                yPos = addText(parts.slice(1).join(':').trim(), margin + 3, yPos, { maxWidth: contentWidth - 6, lineHeight: 5 })
                yPos += 5
            } else {
                // Regular paragraph
                doc.setFont('helvetica', 'normal')
                doc.setTextColor(50, 50, 50)
                yPos = addText(section.trim(), margin + 3, yPos, { maxWidth: contentWidth - 6, lineHeight: 5 })
                yPos += 5
            }
        })
    }

    // ========== MODEL INFORMATION ==========
    checkPageBreak(40)
    addSectionHeader('TECHNICAL DETAILS', [100, 100, 100])

    doc.setFontSize(9)
    doc.setTextColor(40, 40, 40)
    doc.setFont('helvetica', 'normal')

    const modelData = [
        ['Architecture:', data.modelInfo.name],
        ['Method:', 'Grad-CAM Attention Visualization'],
        ['Training Accuracy:', `${(data.modelInfo.accuracy * 100).toFixed(1)}%`],
        ['Dataset:', data.modelInfo.dataset],
    ]

    modelData.forEach(([label, value]) => {
        doc.setFont('helvetica', 'bold')
        doc.text(label, margin + 3, yPos)
        doc.setFont('helvetica', 'normal')
        doc.text(value, margin + 40, yPos)
        yPos += 5
    })
    yPos += 8

    // ========== DISCLAIMERS ==========
    checkPageBreak(40)
    addSectionHeader('IMPORTANT DISCLAIMERS', [220, 38, 38])

    doc.setFillColor(254, 242, 242)
    doc.rect(margin, yPos, contentWidth, 30, 'F')
    doc.setDrawColor(220, 38, 38)
    doc.setLineWidth(0.5)
    doc.rect(margin, yPos, contentWidth, 30)

    doc.setFontSize(8)
    doc.setFont('helvetica', 'bold')
    doc.setTextColor(220, 38, 38)
    doc.text('⚠ CRITICAL NOTICE:', margin + 3, yPos + 5)

    doc.setFont('helvetica', 'normal')
    doc.setTextColor(60, 60, 60)
    const disclaimerText = 'This AI system is for RESEARCH and SCREENING purposes only. It is NOT a substitute for professional medical diagnosis. All findings must be validated by qualified radiologists and healthcare professionals. No clinical validation or regulatory approval for diagnostic use.'
    yPos = addText(disclaimerText, margin + 3, yPos + 10, { maxWidth: contentWidth - 6, lineHeight: 4 })

    // ========== FOOTER ==========
    const footerY = pageHeight - 15
    doc.setFillColor(248, 250, 252)
    doc.rect(0, footerY - 5, pageWidth, 20, 'F')

    doc.setDrawColor(200, 200, 200)
    doc.setLineWidth(0.3)
    doc.line(margin, footerY - 5, pageWidth - margin, footerY - 5)

    doc.setFontSize(7)
    doc.setTextColor(120, 120, 120)
    doc.setFont('helvetica', 'italic')
    doc.text('Generated by NeuroScan AI v2.0.0 - Advanced Medical AI Analysis', pageWidth / 2, footerY, { align: 'center' })
    doc.text('© 2026 NeuroScan AI - For research and educational use only', pageWidth / 2, footerY + 4, { align: 'center' })

    // Save PDF
    doc.save(`neuroscan-ai-comprehensive-report-${Date.now()}.pdf`)
}
