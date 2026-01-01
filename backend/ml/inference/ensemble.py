"""
Model Ensemble System for improved accuracy and confidence
Combines predictions from multiple models for more robust results
"""

import torch
import torch.nn.functional as F
from typing import List, Dict, Tuple
import numpy as np
from pathlib import Path

from ml.models.model import BrainTumorClassifier


class ModelEnsemble:
    """Ensemble of multiple models for improved predictions"""
    
    def __init__(
        self,
        model_configs: List[Dict],
        device: str = 'cpu',
        weights: List[float] = None
    ):
        """
        Initialize model ensemble
        
        Args:
            model_configs: List of model configuration dictionaries
                Each config should have: 'model_type', 'model_path', 'weight'
            device: Device to run inference on
            weights: Optional custom weights for each model (auto-normalized)
        """
        self.device = torch.device(device if torch.cuda.is_available() else 'cpu')
        self.models = []
        self.model_names = []
        
        # Load all models
        for i, config in enumerate(model_configs):
            model_type = config.get('model_type', 'efficientnet_b4')
            model_path = config.get('model_path')
            
            # Create model
            model = BrainTumorClassifier(
                model_name=model_type,
                num_classes=2,
                pretrained=False
            )
            
            # Load weights if path exists
            if model_path and Path(model_path).exists():
                checkpoint = torch.load(model_path, map_location=self.device)
                if 'model_state_dict' in checkpoint:
                    model.load_state_dict(checkpoint['model_state_dict'])
                else:
                    model.load_state_dict(checkpoint)
                print(f"✓ Loaded {model_type} from {model_path}")
            else:
                print(f"⚠ Using pretrained {model_type} (no fine-tuned weights found)")
            
            model = model.to(self.device)
            model.eval()
            
            self.models.append(model)
            self.model_names.append(model_type)
        
        # Set or normalize weights
        if weights is None:
            self.weights = [1.0 / len(self.models)] * len(self.models)
        else:
            total = sum(weights)
            self.weights = [w / total for w in weights]
        
        print(f"\n🎯 Ensemble created with {len(self.models)} models:")
        for name, weight in zip(self.model_names, self.weights):
            print(f"   - {name}: weight={weight:.3f}")
    
    @torch.no_grad()
    def predict(self, image_tensor: torch.Tensor) -> Dict:
        """
        Run ensemble prediction
        
        Args:
            image_tensor: Preprocessed image tensor (1, C, H, W)
            
        Returns:
            Dictionary with ensemble prediction results
        """
        image_tensor = image_tensor.to(self.device)
        
        all_predictions = []
        all_confidences = []
        all_probs = []
        
        # Get predictions from all models
        for model, weight in zip(self.models, self.weights):
            outputs = model(image_tensor)
            probs = F.softmax(outputs, dim=1)
            
            # Weight the probabilities
            weighted_probs = probs * weight
            
            pred_class = torch.argmax(probs, dim=1).item()
            confidence = probs[0, pred_class].item()
            
            all_predictions.append(pred_class)
            all_confidences.append(confidence)
            all_probs.append(weighted_probs[0].cpu().numpy())
        
        # Weighted average of probabilities
        avg_probs = np.sum(all_probs, axis=0)
        final_pred = np.argmax(avg_probs)
        final_confidence = avg_probs[final_pred]
        
        # Calculate agreement (how many models agreed)
        agreement = all_predictions.count(final_pred) / len(all_predictions)
        
        # Calculate uncertainty (std dev of probabilities)
        prob_std = np.std([probs[final_pred] for probs in all_probs])
        
        return {
            'prediction': 'tumor' if final_pred == 1 else 'no_tumor',
            'confidence': float(final_confidence),
            'ensemble_agreement': float(agreement),
            'ensemble_size': len(self.models),
            'uncertainty': float(prob_std),
            'individual_predictions': all_predictions,
            'individual_confidences': all_confidences,
            'model_names': self.model_names,
            'average_probabilities': avg_probs.tolist()
        }
    
    def get_model_statistics(self) -> Dict:
        """Get statistics about the ensemble"""
        return {
            'num_models': len(self.models),
            'model_types': self.model_names,
            'weights': self.weights,
            'device': str(self.device)
        }


class VotingEnsemble:
    """Simple majority voting ensemble"""
    
    def __init__(self, model_configs: List[Dict], device: str = 'cpu'):
        """Initialize voting ensemble"""
        self.ensemble = ModelEnsemble(model_configs, device)
    
    @torch.no_grad()
    def predict(self, image_tensor: torch.Tensor) -> Dict:
        """Run voting-based prediction"""
        result = self.ensemble.predict(image_tensor)
        
        # Count votes
        predictions = result['individual_predictions']
        votes = {0: predictions.count(0), 1: predictions.count(1)}
        
        # Majority vote
        final_pred = max(votes, key=votes.get)
        confidence = votes[final_pred] / len(predictions)
        
        return {
            'prediction': 'tumor' if final_pred == 1 else 'no_tumor',
            'confidence': float(confidence),
            'votes': votes,
            'total_models': len(predictions),
            'unanimous': all(p == final_pred for p in predictions)
        }


# Predefined ensemble configurations
def get_default_ensemble_config() -> List[Dict]:
    """Get default ensemble configuration"""
    base_path = Path(__file__).parent.parent.parent / 'models'
    
    return [
        {
            'model_type': 'efficientnet_b4',
            'model_path': str(base_path / 'brain_tumor_model.pth'),
            'weight': 1.0
        },
        {
            'model_type': 'efficientnet_b7',
            'model_path': str(base_path / 'efficientnet_b7_model.pth'),
            'weight': 1.2  # Slightly higher weight for larger model
        },
        {
            'model_type': 'resnet152',
            'model_path': str(base_path / 'resnet152_model.pth'),
            'weight': 0.8  # Lower weight for different architecture
        }
    ]


def create_ensemble(
    model_configs: List[Dict] = None,
    device: str = 'cpu',
    use_voting: bool = False
) -> ModelEnsemble:
    """
    Convenience function to create ensemble
    
    Args:
        model_configs: Model configurations or None for default
        device: Device to use
        use_voting: Use voting instead of weighted average
        
    Returns:
        Ensemble model
    """
    if model_configs is None:
        model_configs = get_default_ensemble_config()
    
    if use_voting:
        return VotingEnsemble(model_configs, device)
    else:
        return ModelEnsemble(model_configs, device)
