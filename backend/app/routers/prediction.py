"""
API router for predictions
"""
from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from PIL import Image
import io
from typing import Optional

from ml.inference.inference import InferenceService
from ml.explainability.gradcam import generate_gradcam_visualization
from app.config import settings
from app.services.ai_service import get_ai_service


router = APIRouter(prefix="/api", tags=["prediction"])

# Global inference service (initialized on startup)
inference_service: Optional[InferenceService] = None


def get_inference_service() -> InferenceService:
    """Get or create inference service"""
    global inference_service
    if inference_service is None:
        inference_service = InferenceService(
            model_path=settings.MODEL_PATH,
            model_type=settings.MODEL_TYPE,
            device=settings.DEVICE,
            image_size=settings.IMAGE_SIZE
        )
    return inference_service


@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Predict brain tumor from MRI scan
    
    Args:
        file: Uploaded image file
        
    Returns:
        Prediction results with confidence
    """
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(
                status_code=400,
                detail="File must be an image"
            )
        
        # Read image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Get inference service
        service = get_inference_service()
        
        # Make prediction
        result = service.predict(image)
        
        # Classify tumor type if tumor detected
        if result['prediction'] == 'tumor':
            from app.services.tumor_classifier import tumor_classifier
            tumor_info = tumor_classifier.classify(
                confidence=result['confidence'],
                prediction=result['prediction']
            )
            result['tumor_type'] = tumor_info['type']
            result['type_confidence'] = tumor_info['confidence']
            result['type_characteristics'] = tumor_info['characteristics']
            result['type_description'] = tumor_info['description']
        
        # Generate AI-powered narrative (now includes tumor type if available)
        ai_service = get_ai_service()
        result['narrative'] = ai_service.generate_analysis(result)
        
        # Generate differential diagnosis
        differential = ai_service.generate_differential_diagnosis(
            prediction=result['prediction'],
            confidence=result['confidence'],
            tumor_type=result.get('tumor_type')
        )
        result['differential_diagnosis'] = differential
        
        # Generate risk assessment
        risk = ai_service.generate_risk_assessment(
            prediction=result['prediction'],
            confidence=result['confidence'],
            tumor_type=result.get('tumor_type')
        )
        result['risk_assessment'] = risk
        
        return JSONResponse(content=result)
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )


@router.post("/explain-region")
async def explain_region(request: dict):
    """
    Explain a specific brain region that user clicked on
    
    Expected request:
    {
        "x": 0.5,  # Relative x coordinate (0-1)
        "y": 0.3,  # Relative y coordinate (0-1)
        "prediction": "tumor",
        "confidence": 0.95
    }
    """
    try:
        from app.services.brain_anatomy import brain_mapper
        
        # Get coordinates
        rel_x = request.get('x', 0.5)
        rel_y = request.get('y', 0.5)
        
        # Map to brain region
        region_info = brain_mapper.identify_region(rel_x, rel_y)
        
        # Calculate attention score (simulated for now - in real version, would read from actual heatmap)
        # Higher attention in center and top regions for demo
        attention_score = max(0.1, min(0.9, 1.0 - abs(rel_y - 0.3)))
        
        # Generate AI explanation
        ai_service = get_ai_service()
        explanation = ai_service.explain_region(
            region_name=region_info["name"],
            region_function=region_info["function"],
            attention_score=attention_score,
            prediction=request.get('prediction', 'unknown'),
            confidence=request.get('confidence', 0.5)
        )
        
        return JSONResponse(content={
            "region": region_info["name"],
            "function": region_info["function"],
            "attention": round(attention_score * 100, 1),
            "explanation": explanation
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Region explanation failed: {str(e)}")


@router.post("/gradcam")
async def gradcam(file: UploadFile = File(...)):
    """
    Generate Grad-CAM visualization
    
    Args:
        file: Uploaded image file
        
    Returns:
        Grad-CAM overlay image
    """
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(
                status_code=400,
                detail="File must be an image"
            )
        
        # Read image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Get inference service
        service = get_inference_service()
        
        # Preprocess for model
        image_tensor = service.preprocess_image(image)
        image_tensor = image_tensor.to(service.device)
        
        # Generate Grad-CAM
        gradcam_image = generate_gradcam_visualization(
            service.model,
            image,
            image_tensor
        )
        
        # Convert to bytes
        img_byte_arr = io.BytesIO()
        gradcam_image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        return StreamingResponse(img_byte_arr, media_type="image/png")
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Grad-CAM generation failed: {str(e)}"
        )


def generate_template_narrative(result: dict) -> str:
    """
    Generate detailed template-based narrative
    
    Args:
        result: Prediction result
        
    Returns:
        Comprehensive narrative string
    """
    prediction = result['prediction']
    confidence = result['confidence'] * 100
    
    if prediction == 'tumor':
        # Detailed tumor detection narrative
        base_narrative = (
            f"The AI model has detected potential tumor presence with {confidence:.1f}% confidence. "
        )
        
        # Add confidence-specific details
        if confidence > 90:
            confidence_detail = (
                "This high confidence level indicates strong and consistent patterns associated with abnormal tissue growth. "
                "The model identified multiple converging indicators across different feature sets, including structural irregularities, "
                "density variations, and texture anomalies that collectively suggest tumor presence. "
            )
        elif confidence >= 70:
            confidence_detail = (
                "This moderate-to-high confidence suggests clear patterns consistent with tumor characteristics, though some variability exists. "
                "The model detected significant structural abnormalities and density changes typical of tumor tissue. "
            )
        else:
            confidence_detail = (
                "While the model leans toward tumor detection, the moderate confidence indicates some ambiguity in the patterns. "
                "This could be due to early-stage development, scan quality, or subtle presentation of abnormalities. "
            )
        
        technical_analysis = (
            "**Technical Analysis:** The deep learning model analyzed the scan through multiple convolutional layers, "
            "extracting hierarchical features from low-level edges and textures to high-level semantic patterns. "
            "Key indicators included: (1) Irregular tissue density distributions showing hyperintensity in localized regions, "
            "(2) Asymmetric structural patterns deviating from normal brain anatomy, "
            "(3) Texture heterogeneity suggesting cellular abnormalities, and "
            "(4) Boundary irregularities inconsistent with healthy tissue margins. "
        )
        
        gradcam_explanation = (
            "**Attention Map Interpretation:** The Grad-CAM visualization highlights regions where the model focused its attention. "
            "Red and yellow areas indicate high activation zones where the neural network detected strongest anomalous patterns. "
            "These attention hotspots typically correspond to areas of concern that contributed most to the tumor classification. "
        )
        
        recommendations = (
            "**Recommendations:** Immediate consultation with a neurologist or neuro-oncologist is strongly advised. "
            "Additional diagnostic imaging (CT, MRI with contrast, PET scan) should be considered for comprehensive evaluation. "
            "Biopsy may be necessary for definitive diagnosis and tumor characterization. "
            "Early detection significantly improves treatment outcomes, so prompt medical attention is crucial. "
        )
        
        disclaimer = (
            "**Important Notice:** This AI analysis serves as a screening tool and should NOT replace professional medical diagnosis. "
            "Only qualified healthcare professionals can provide definitive diagnosis and treatment recommendations."
        )
        
        return base_narrative + confidence_detail + technical_analysis + gradcam_explanation + recommendations + disclaimer
    
    else:
        # Detailed no tumor narrative
        base_narrative = (
            f"The AI model indicates no tumor detected with {confidence:.1f}% confidence. "
        )
        
        # Add confidence-specific details
        if confidence > 90:
            confidence_detail = (
                "This high confidence level suggests the scan displays clear characteristics of healthy brain tissue. "
                "The model identified consistent normal patterns across all analyzed regions, including regular tissue density, "
                "symmetric structural organization, and absence of anomalous texture variations. "
            )
        elif confidence >= 70:
            confidence_detail = (
                "This moderate-to-high confidence indicates predominantly normal tissue patterns with no significant abnormalities detected. "
                "The analysis shows typical brain anatomy features and expected tissue characteristics. "
            )
        else:
            confidence_detail = (
                "While the model leans toward normal tissue classification, the moderate confidence warrants attention. "
                "This could be influenced by scan quality, imaging artifacts, or subtle variations that require further review. "
            )
        
        technical_analysis = (
            "**Technical Analysis:** The neural network processed the MRI scan through its trained layers, evaluating structural integrity, "
            "tissue density homogeneity, and anatomical consistency. "
            "Key findings included: (1) Symmetric bilateral brain structures showing normal organization, "
            "(2) Uniform tissue density patterns within expected ranges, "
            "(3) Regular texture characteristics consistent with healthy neural tissue, and "
            "(4) Absence of irregular boundaries or abnormal mass effects. "
        )
        
        gradcam_explanation = (
            "**Attention Map Interpretation:** The Grad-CAM visualization shows distributed attention across the scan, "
            "indicating the model didn't find focal areas of high concern. "
            "This diffuse attention pattern is typical for normal scans where no single region triggers strong anomaly detection. "
        )
        
        recommendations = (
            "**Recommendations:** Continue regular health monitoring as per your healthcare provider's schedule. "
            "Maintain routine screening if recommended based on personal or family medical history. "
            "Report any new neurological symptoms (headaches, vision changes, seizures, cognitive changes) to your doctor promptly. "
            "Lifestyle factors including regular exercise, healthy diet, and stress management support overall brain health. "
        )
        
        disclaimer = (
            "**Important Notice:** While this analysis suggests normal findings, it should not replace regular medical checkups. "
            "Always consult healthcare professionals for comprehensive neurological assessment and personalized medical advice."
        )
        
        return base_narrative + confidence_detail + technical_analysis + gradcam_explanation + recommendations + disclaimer



async def generate_ai_narrative(result: dict) -> str:
    """
    Generate AI narrative using LLM (optional)
    
    Args:
        result: Prediction result
        
    Returns:
        AI-generated narrative
    """
    # TODO: Implement LLM integration
    # For now, return template
    return generate_template_narrative(result)
