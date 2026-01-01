"""
Test-Time Augmentation (TTA) for improved prediction accuracy and confidence

TTA applies multiple augmentations during inference and averages the predictions
to get more robust and confident results.
"""

import torch
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image
import numpy as np
from typing import Dict, List


class TTAWrapper:
    """Wrapper for Test-Time Augmentation"""
    
    def __init__(self, model, device='cpu', num_tta=5):
        """
        Initialize TTA wrapper
        
        Args:
            model: PyTorch model
            device: Device to run inference on
            num_tta: Number of TTA predictions to average
        """
        self.model = model
        self.device = device
        self.num_tta = num_tta
        
    def _augment_image(self, image_tensor: torch.Tensor, aug_type: str) -> torch.Tensor:
        """
        Apply augmentation to image tensor
        
        Args:
            image_tensor: Input tensor (C, H, W)
            aug_type: Type of augmentation
            
        Returns:
            Augmented tensor
        """
        if aug_type == 'original':
            return image_tensor
        
        elif aug_type == 'hflip':
            # Horizontal flip
            return torch.flip(image_tensor, dims=[-1])
        
        elif aug_type == 'vflip':
            # Vertical flip
            return torch.flip(image_tensor, dims=[-2])
        
        elif aug_type == 'rotate_5':
            # Rotate 5 degrees
            return transforms.functional.rotate(image_tensor, 5)
        
        elif aug_type == 'rotate_-5':
            # Rotate -5 degrees
            return transforms.functional.rotate(image_tensor, -5)
        
        elif aug_type == 'brightness':
            # Slight brightness adjustment
            return transforms.functional.adjust_brightness(image_tensor, 1.1)
        
        elif aug_type == 'contrast':
            # Slight contrast adjustment
            return transforms.functional.adjust_contrast(image_tensor, 1.1)
        
        return image_tensor
    
    def predict_with_tta(self, image_tensor: torch.Tensor) -> Dict[str, any]:
        """
        Run prediction with TTA
        
        Args:
            image_tensor: Preprocessed image tensor (1, C, H, W)
            
        Returns:
            Dictionary with prediction, confidence, and TTA details
        """
        self.model.eval()
        
        # Define augmentation types
        aug_types = ['original', 'hflip', 'rotate_5', 'rotate_-5', 'brightness']
        
        predictions = []
        confidences = []
        
        with torch.no_grad():
            for aug_type in aug_types[:self.num_tta]:
                # Apply augmentation
                aug_image = self._augment_image(image_tensor[0], aug_type)
                aug_image = aug_image.unsqueeze(0).to(self.device)
                
                # Get prediction
                output = self.model(aug_image)
                probs = F.softmax(output, dim=1)
                
                # Store results
                pred_class = torch.argmax(probs, dim=1).item()
                confidence = probs[0, pred_class].item()
                
                predictions.append(pred_class)
                confidences.append(probs[0].cpu().numpy())
        
        # Average probabilities across all TTAs
        avg_probs = np.mean(confidences, axis=0)
        final_pred = np.argmax(avg_probs)
        final_confidence = avg_probs[final_pred]
        
        # Calculate agreement (how many TTAs agreed)
        agreement = predictions.count(final_pred) / len(predictions)
        
        return {
            'prediction': 'tumor' if final_pred == 1 else 'no_tumor',
            'confidence': float(final_confidence),
            'tta_agreement': float(agreement),
            'tta_count': len(predictions),
            'individual_predictions': predictions,
            'average_probabilities': avg_probs.tolist()
        }


def apply_tta_ensemble(model, image_tensor: torch.Tensor, device='cpu') -> Dict[str, any]:
    """
    Convenience function to apply TTA
    
    Args:
        model: Trained model
        image_tensor: Preprocessed image
        device: Device to use
        
    Returns:
        TTA prediction results
    """
    tta_wrapper = TTAWrapper(model, device=device, num_tta=5)
    return tta_wrapper.predict_with_tta(image_tensor)
