"""
AI Service using Google Gemini API for Medical Analysis

Generates dynamic, context-aware medical explanations for brain tumor detection.
"""

import os
import logging
from typing import Dict, Optional

try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    print("⚠️ google-generativeai not installed")

logger = logging.getLogger(__name__)


class AIService:
    """Service for generating AI-powered medical narratives using Gemini"""
    
    def __init__(self):
        """Initialize Gemini AI service"""
        self.api_key = os.getenv("GEMINI_API_KEY", "")
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-pro")
        self.use_ai = os.getenv("USE_AI_NARRATIVES", "false").lower() == "true"
        self.model = None
        
        print(f"🔍 AI Service Init:")
        print(f"   - API Key present: {bool(self.api_key)}")
        print(f"   - USE_AI_NARRATIVES: {self.use_ai}")
        print(f"   - GENAI_AVAILABLE: {GENAI_AVAILABLE}")
        
        if self.use_ai and self.api_key and GENAI_AVAILABLE:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel(self.model_name)
                print(f"✅ Gemini AI initialized: {self.model_name}")
                logger.info(f"✅ Gemini AI initialized: {self.model_name}")
            except Exception as e:
                print(f"❌ Failed to initialize Gemini: {str(e)}")
                logger.error(f"❌ Failed to initialize Gemini: {str(e)}")
                self.use_ai = False
        else:
            print("📝 AI narratives disabled - using templates")
            logger.info("📝 AI narratives disabled - using templates")
    
    def generate_analysis(self, result: Dict) -> str:
        """
        Generate comprehensive AI analysis
        
        Args:
            result: Dictionary with prediction, confidence, etc.
            
        Returns:
            AI-generated medical narrative
        """
        if self.use_ai and self.model:
            try:
                print("🤖 Calling Gemini API...")
                return self._generate_with_ai(result)
            except Exception as e:
                print(f"❌ AI generation failed: {str(e)}")
                logger.error(f"AI generation failed: {str(e)}")
                logger.info("Falling back to template")
                return self._generate_template(result)
        
        print("📝 Using template (AI disabled)")
        return self._generate_template(result)
    
    def _generate_with_ai(self, result: Dict) -> str:
        """Generate narrative using Gemini API"""
        prediction = result.get('prediction', 'unknown')
        confidence = result.get('confidence', 0.0) * 100
        tumor_type = result.get('tumor_type')
        type_confidence = result.get('type_confidence', 0.0) * 100 if tumor_type else 0
        
        # Build scan results section
        scan_results = f"""**Scan Results:**
- Detection: {"Tumor detected" if prediction == "tumor" else "No tumor detected"}
- Confidence: {confidence:.1f}%
- Model: Deep Learning (EfficientNet-B4)
- Analysis Method: Grad-CAM attention mapping"""
        
        # Add tumor type if detected
        if tumor_type:
            scan_results += f"\n- Tumor Type (Preliminary): {tumor_type} ({type_confidence:.1f}% confidence)"
        
        prompt = f"""You are an expert medical AI assistant specializing in brain tumor analysis. Analyze the following MRI scan results and provide a comprehensive, professional medical explanation.

{scan_results}

**Generate a comprehensive medical analysis with these sections:**

1. **Executive Summary** (2-3 sentences)
   - State the finding clearly
   - Mention confidence level and tumor type if detected
   - Provide immediate recommendation

2. **Detailed Analysis**
   - Imaging patterns identified by the AI model
   - Key features that contributed to classification
   - Grad-CAM attention regions and their significance
   - Comparison with normal brain tissue patterns

3. **Tumor Classification** (if tumor detected)
   {"- Classified as: " + tumor_type if tumor_type else "- Analyze likely tumor type based on imaging:"}
   - Explain characteristics specific to this type
   - Confidence in classification
   - Distinguishing features
   - Common presentation and behavior

4. **Clinical Significance**
   - What these findings mean clinically
   - Potential impact on the patient
   - Urgency level (routine/urgent/emergency)

5. **Recommendations**
   - Next steps for diagnosis
   - Suggested imaging (contrast MRI, CT, etc.)
   - Specialist consultations needed
   - Timeline for follow-up

6. **Important Disclaimers**
   - This is an AI screening tool
   - Must be validated by qualified radiologists
   - Not a replacement for professional diagnosis
   - Part of clinical decision support

**Tone:** Professional, empathetic, medically accurate
**Format:** Use markdown with clear section headers
**Length:** Comprehensive but concise (400-500 words)

Generate the analysis now:"""

        response = self.model.generate_content(prompt)
        
        print("✅ Gemini API call successful!")
        return response.text
    
    def explain_region(
        self, 
        region_name: str,
        region_function: str,
        attention_score: float,
        prediction: str,
        confidence: float
    ) -> str:
        """
        Generate AI explanation for a specific brain region
        
        Args:
            region_name: Name of the brain region
            region_function: Function of the region
            attention_score: How much model focused here (0-1)
            prediction: Overall prediction (tumor/no tumor)
            confidence: Overall confidence (0-1)
            
        Returns:
            AI-generated explanation
        """
        if not self.use_ai or not self.model:
            # Fallback template
            attention_level = "high" if attention_score > 0.5 else "moderate" if attention_score > 0.2 else "low"
            return f"The {region_name} shows {attention_level} attention from the AI model. This region is responsible for {region_function.lower()}. The model's focus here contributes to the overall {prediction} prediction with {confidence*100:.1f}% confidence."
        
        try:
            print(f"🤖 Explaining region: {region_name}...")
            
            prompt = f"""You are a medical AI assistant explaining brain MRI analysis to patients.

**Brain Region Clicked:** {region_name}
**Region Function:** {region_function}
**Model Attention:** {attention_score*100:.1f}% (how intensely the AI focused on this area)
**Overall Diagnosis:** {prediction}
**Confidence:** {confidence*100:.1f}%

**Task:** In 3-4 sentences, explain:
1. What this brain region does (in simple terms)
2. Why the AI model {"focused heavily" if attention_score > 0.5 else "showed moderate interest in" if attention_score > 0.2 else "showed minimal focus on"} this area
3. What this means for the diagnosis

**Tone:** Educational but accessible. Medical accuracy is important but avoid jargon.
**Format:** Plain text, conversational.

Generate explanation:"""

            response = self.model.generate_content(prompt)
            print("✅ Region explanation generated!")
            return response.text
            
        except Exception as e:
            print(f"❌ Region explanation failed: {str(e)}")
            # Return template fallback
            attention_level = "high" if attention_score > 0.5 else "moderate" if attention_score > 0.2 else "low"
            return f"The {region_name} is responsible for {region_function.lower()}. The AI model showed {attention_level} attention to this region during analysis, which contributed to the {prediction} prediction."
    
    def generate_differential_diagnosis(
        self,
        prediction: str,
        confidence: float,
        tumor_type: str = None
    ) -> list:
        """
        Generate differential diagnosis list
        
        Args:
            prediction: 'tumor' or 'no_tumor'
            confidence: Detection confidence (0-1)
            tumor_type: Classified tumor type if available
            
        Returns:
            List of differential diagnoses with likelihood and reasoning
        """
        if not self.use_ai or not self.model:
            # Fallback template-based differential
            return self._generate_template_differential(prediction, tumor_type)
        
        try:
            print(f"🤖 Generating differential diagnosis...")
            
            confidence_pct = confidence * 100
            
            prompt = f"""You are an expert neuroradiologist providing differential diagnosis for a brain MRI scan.

**Scan Analysis:**
- Primary Finding: {"Tumor detected" if prediction == "tumor" else "No significant abnormality detected"}
- Detection Confidence: {confidence_pct:.1f}%
{f"- Preliminary Classification: {tumor_type}" if tumor_type else ""}

**Task:** Generate a differential diagnosis list with 3-5 possible diagnoses ranked by likelihood.

**Format your response as a JSON array ONLY, for example:**
[
  {{
    "diagnosis": "Glioblastoma Multiforme",
    "likelihood": 75,
    "reasoning": "Most likely given infiltrative pattern and irregular borders on imaging.",
    "key_feature": "Aggressive growth pattern"
  }},
  {{
    "diagnosis": "Metastatic Tumor",
    "likelihood": 15,
    "reasoning": "Consider if patient has history of systemic cancer.",
    "key_feature": "Multiple lesions possible"
  }}
]

**Guidelines:**
- Likelihood percentages should sum to ~100%
- Primary diagnosis: 60-80%
- Secondary: 10-25%
- Tertiary and beyond: 5-15% each
- Include both common and rare but important considerations
- Be medically accurate

Generate ONLY the JSON array, no additional text:"""

            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Extract JSON from response (handle markdown code blocks)
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            # Parse JSON
            import json
            differential = json.loads(response_text)
            
            print(f"✅ Differential diagnosis generated: {len(differential)} diagnoses")
            return differential
            
        except Exception as e:
            print(f"❌ Differential generation failed: {str(e)}")
            logger.error(f"Differential generation failed: {str(e)}")
            return self._generate_template_differential(prediction, tumor_type)
    
    def _generate_template_differential(self, prediction: str, tumor_type: str = None) -> list:
        """Fallback template-based differential diagnosis"""
        if prediction == "tumor":
            if tumor_type == "Glioma":
                return [
                    {"diagnosis": "Glioblastoma", "likelihood": 70, "reasoning": "Most aggressive glioma type, common in adults", "key_feature": "Infiltrative growth"},
                    {"diagnosis": "Anaplastic Astrocytoma", "likelihood": 20, "reasoning": "High-grade glioma, less aggressive than GBM", "key_feature": "Grade III malignancy"},
                    {"diagnosis": "Metastatic Tumor", "likelihood": 10, "reasoning": "Rule out metastasis from systemic cancer", "key_feature": "History dependent"}
                ]
            elif tumor_type == "Meningioma":
                return [
                    {"diagnosis": "Benign Meningioma", "likelihood": 85, "reasoning": "Most common, slow-growing, good prognosis", "key_feature": "Dura attachment"},
                    {"diagnosis": "Atypical Meningioma", "likelihood": 12, "reasoning": "Grade II, higher recurrence risk", "key_feature": "Increased mitoses"},
                    {"diagnosis": "Hemangiopericytoma", "likelihood": 3, "reasoning": "Rare dural-based tumor", "key_feature": "Aggressive behavior"}
                ]
            else:
                return [
                    {"diagnosis": "Primary Brain Tumor", "likelihood": 60, "reasoning": "Imaging consistent with primary CNS neoplasm", "key_feature": "Intrinsic to brain"},
                    {"diagnosis": "Metastatic Disease", "likelihood": 25, "reasoning": "Consider systemic malignancy", "key_feature": "Multiple possible"},
                    {"diagnosis": "Abscess", "likelihood": 10, "reasoning": "Infectious etiology to consider", "key_feature": "Ring enhancement"},
                    {"diagnosis": "Demyelinating Lesion", "likelihood": 5, "reasoning": "MS or other demyelinating process", "key_feature": "Periventricular"}
                ]
        else:
            return [
                {"diagnosis": "Normal Anatomy", "likelihood": 80, "reasoning": "No significant abnormality detected", "key_feature": "Healthy tissue"},
                {"diagnosis": "Age-Related Changes", "likelihood": 12, "reasoning": "Expected involutional changes", "key_feature": "Non-pathologic"},
                {"diagnosis": "White Matter Changes", "likelihood": 5, "reasoning": "Chronic small vessel disease", "key_feature": "Vascular etiology"},
                {"diagnosis": "Artifact", "likelihood": 3, "reasoning": "Motion or technical artifact", "key_feature": "Non-diagnostic"}
            ]
    
    def generate_risk_assessment(
        self,
        prediction: str,
        confidence: float,
        tumor_type: str = None
    ) -> dict:
        """
        Generate risk assessment with severity score and urgency level
        
        Args:
            prediction: 'tumor' or 'no_tumor'
            confidence: Detection confidence (0-1)
            tumor_type: Classified tumor type if available
            
        Returns:
            Dictionary with severity_score, urgency_level, timeline, reasoning
        """
        if not self.use_ai or not self.model:
            # Fallback template-based risk assessment
            return self._generate_template_risk(prediction, confidence, tumor_type)
        
        try:
            print(f"🤖 Generating risk assessment...")
            
            confidence_pct = confidence * 100
            
            prompt = f"""You are an expert medical AI providing risk assessment for a brain MRI scan.

**Scan Analysis:**
- Primary Finding: {"Tumor detected" if prediction == "tumor" else "No significant abnormality detected"}
- Detection Confidence: {confidence_pct:.1f}%
{f"- Tumor Type: {tumor_type}" if tumor_type else ""}

**Task:** Generate a risk assessment with severity score, urgency level, and recommended timeline.

**Format your response as JSON ONLY:**
{{
  "severity_score": 8,
  "urgency_level": "urgent",
  "timeline": "Consult neurosurgeon within 24-48 hours",
  "reasoning": "High-grade tumor suspected with significant clinical implications"
}}

**Guidelines:**
- **severity_score**: 1-10 scale
  - 1-3: Low risk (benign/normal, routine follow-up)
  - 4-6: Moderate risk (monitoring needed, non-urgent)
  - 7-8: High risk (prompt specialist consultation)
  - 9-10: Critical risk (immediate emergency evaluation)
  
- **urgency_level**: Must be one of: "routine", "urgent", or "emergency"
  - routine: Normal findings or benign conditions
  - urgent: Concerning findings requiring prompt evaluation (24-48 hours)
  - emergency: Life-threatening findings requiring immediate action
  
- **timeline**: Specific actionable timeframe (e.g., "Schedule appointment within 2 weeks", "See specialist within 24 hours", "Go to ER immediately")

- **reasoning**: 1-2 sentence explanation of the risk level

Generate ONLY the JSON object, no additional text:"""

            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Extract JSON from response (handle markdown code blocks)
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            # Parse JSON
            import json
            risk = json.loads(response_text)
            
            print(f"✅ Risk assessment generated: Severity {risk.get('severity_score')}/10, {risk.get('urgency_level')}")
            return risk
            
        except Exception as e:
            print(f"❌ Risk assessment failed: {str(e)}")
            logger.error(f"Risk assessment failed: {str(e)}")
            return self._generate_template_risk(prediction, confidence, tumor_type)
    
    def _generate_template_risk(self, prediction: str, confidence: float, tumor_type: str = None) -> dict:
        """Fallback template-based risk assessment"""
        if prediction == "tumor":
            if tumor_type == "Glioma":
                return {
                    "severity_score": 8,
                    "urgency_level": "urgent",
                    "timeline": "Consult neurosurgeon within 24-48 hours",
                    "reasoning": "High-grade glioma suspected; requires prompt specialist evaluation and treatment planning"
                }
            elif tumor_type == "Meningioma":
                return {
                    "severity_score": 5,
                    "urgency_level": "routine",
                    "timeline": "Schedule neurosurgeon consultation within 1-2 weeks",
                    "reasoning": "Meningioma typically slow-growing; planned evaluation and monitoring appropriate"
                }
            else:
                return {
                    "severity_score": 7,
                    "urgency_level": "urgent",
                    "timeline": "See specialist within 48-72 hours",
                    "reasoning": "Brain tumor detected; requires timely medical evaluation for diagnosis and treatment planning"
                }
        else:
            return {
                "severity_score": 2,
                "urgency_level": "routine",
                "timeline": "Continue routine health monitoring",
                "reasoning": "No significant abnormalities detected; routine follow-up care recommended"
            }
    
    def _generate_template(self, result: Dict) -> str:
        """Fallback template-based narrative"""
        prediction = result.get('prediction', 'unknown')
        confidence = result.get('confidence', 0.0) * 100
        
        if prediction == 'tumor':
            narrative = f"""**Executive Summary**

The AI model has detected potential tumor presence with {confidence:.1f}% confidence. This finding requires immediate medical evaluation and confirmatory imaging.

**Detailed Analysis**

The deep learning model analyzed the MRI scan through multiple convolutional layers, identifying patterns associated with abnormal tissue growth. Key indicators include irregular tissue density distributions, asymmetric structural patterns, and texture heterogeneity suggesting cellular abnormalities.

**Grad-CAM Interpretation**

The attention heatmap highlights regions where the model detected strongest anomalous patterns. Red and yellow areas indicate high-attention zones that contributed most to the tumor classification.

**Clinical Significance**

These findings suggest the presence of a space-occupying lesion requiring urgent evaluation. The confidence level indicates clear pattern recognition by the AI system.

**Recommendations**

- Immediate consultation with a neurologist or neuro-oncologist
- Additional imaging: Contrast-enhanced MRI, CT scan
- Consider biopsy for definitive diagnosis
- Timeline: Urgent evaluation within 24-48 hours

**Important Notice**

This AI analysis is a screening tool and must be validated by qualified medical professionals. All findings should be confirmed through comprehensive diagnostic procedures."""
        
        else:
            narrative = f"""**Executive Summary**

The AI model did not identify significant tumor indicators in this scan ({confidence:.1f}% confidence). However, clinical correlation is essential.

**Detailed Analysis**

The neural network processed the MRI scan and found tissue density, structural symmetry, and texture patterns consistent with healthy brain anatomy. No significant deviations from normal were detected across multiple analytical layers.

**Grad-CAM Interpretation**

The attention map shows distributed focus without concentrated hotspots, indicating no specific regions triggered tumor-associated patterns.

**Clinical Significance**

While encouraging, this result should be interpreted within the full clinical context including symptoms, history, and physical examination.

**Recommendations**

- Continue routine health monitoring
- Report any neurological symptoms to your healthcare provider
- Follow recommended screening schedule
- Maintain healthy lifestyle practices

**Important Notice**

This AI screening does not replace regular medical checkups. Always consult healthcare professionals for comprehensive neurological assessment and personalized medical advice."""
        
        return narrative


# Global AI service instance
_ai_service = None

def get_ai_service() -> AIService:
    """Get or create global AI service instance"""
    global _ai_service
    if _ai_service is None:
        _ai_service = AIService()
    return _ai_service
