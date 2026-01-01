"""
Grad-CAM implementation for explainable AI
"""
import torch
import torch.nn.functional as F
import numpy as np
from PIL import Image
import cv2
from typing import Tuple

from ml.models.model import BrainTumorClassifier


class GradCAM:
    """Gradient-weighted Class Activation Mapping"""
    
    def __init__(self, model: BrainTumorClassifier, target_layer: str = None):
        """
        Initialize Grad-CAM
        
        Args:
            model: The model to explain
            target_layer: Name of target layer (auto-detect if None)
        """
        self.model = model
        self.model.eval()
        
        # Auto-detect target layer (last conv layer)
        if target_layer is None:
            self.target_layer = self._get_last_conv_layer()
        else:
            self.target_layer = target_layer
        
        self.gradients = None
        self.activations = None
        
        # Register hooks
        self._register_hooks()
    
    def _get_last_conv_layer(self):
        """Find the last convolutional layer"""
        # For most models, it's in the backbone
        for name, module in self.model.backbone.named_modules():
            if isinstance(module, torch.nn.Conv2d):
                last_conv = name
        return last_conv
    
    def _register_hooks(self):
        """Register forward and backward hooks"""
        def forward_hook(module, input, output):
            self.activations = output.detach()
        
        def backward_hook(module, grad_input, grad_output):
            self.gradients = grad_output[0].detach()
        
        # Get target layer
        target_module = dict(self.model.backbone.named_modules())[self.target_layer]
        
        target_module.register_forward_hook(forward_hook)
        target_module.register_full_backward_hook(backward_hook)
    
    def generate_cam(
        self, 
        image_tensor: torch.Tensor, 
        target_class: int = None
    ) -> np.ndarray:
        """
        Generate Class Activation Map
        
        Args:
            image_tensor: Input image tensor (1, C, H, W)
            target_class: Target class for CAM (None = predicted class)
            
        Returns:
            Heatmap as numpy array
        """
        # Forward pass
        self.model.zero_grad()
        output = self.model(image_tensor)
        
        # Get target class
        if target_class is None:
            target_class = output.argmax(dim=1).item()
        
        # Backward pass
        output[0, target_class].backward()
        
        # Get gradients and activations
        gradients = self.gradients[0]  # (C, H, W)
        activations = self.activations[0]  # (C, H, W)
        
        # Global average pooling of gradients
        weights = gradients.mean(dim=(1, 2))  # (C,)
        
        # Weighted combination of activation maps
        cam = torch.zeros(activations.shape[1:], device=activations.device)
        for i, w in enumerate(weights):
            cam += w * activations[i]
        
        # ReLU
        cam = F.relu(cam)
        
        # Normalize
        cam = cam.cpu().numpy()
        cam = (cam - cam.min()) / (cam.max() - cam.min() + 1e-8)
        
        return cam
    
    def overlay_heatmap(
        self,
        original_image: Image.Image,
        heatmap: np.ndarray,
        alpha: float = 0.4,
        colormap: int = cv2.COLORMAP_JET
    ) -> Image.Image:
        """
        Overlay heatmap on original image
        
        Args:
            original_image: Original PIL Image
            heatmap: Heatmap array
            alpha: Transparency of heatmap overlay
            colormap: OpenCV colormap
            
        Returns:
            PIL Image with overlay
        """
        # Resize heatmap to match image
        img_array = np.array(original_image.convert('RGB'))
        heatmap_resized = cv2.resize(heatmap, (img_array.shape[1], img_array.shape[0]))
        
        # Apply colormap
        heatmap_colored = cv2.applyColorMap(
            np.uint8(255 * heatmap_resized), 
            colormap
        )
        heatmap_colored = cv2.cvtColor(heatmap_colored, cv2.COLOR_BGR2RGB)
        
        # Overlay
        overlayed = cv2.addWeighted(img_array, 1 - alpha, heatmap_colored, alpha, 0)
        
        return Image.fromarray(overlayed)


def generate_gradcam_visualization(
    model: BrainTumorClassifier,
    image: Image.Image,
    image_tensor: torch.Tensor,
    target_class: int = None
) -> Image.Image:
    """
    Generate Grad-CAM visualization
    
    Args:
        model: Trained model
        image: Original image
        image_tensor: Preprocessed image tensor
        target_class: Target class (None = predicted)
        
    Returns:
        PIL Image with Grad-CAM overlay
    """
    # Create Grad-CAM
    gradcam = GradCAM(model)
    
    # Generate heatmap
    heatmap = gradcam.generate_cam(image_tensor, target_class)
    
    # Overlay on original image
    result = gradcam.overlay_heatmap(image, heatmap, alpha=0.4)
    
    return result
