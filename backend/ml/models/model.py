"""
Model architectures for brain tumor detection
"""
import torch
import torch.nn as nn
import timm
from typing import Optional


class BrainTumorClassifier(nn.Module):
    """
    Brain tumor classifier using transfer learning
    
    Supports multiple architectures:
    - EfficientNet (efficientnet_b0, efficientnet_b4)
    - ResNet (resnet50, resnet101)
    - Vision Transformer (vit_base_patch16_224)
    """
    
    def __init__(
        self, 
        model_name: str = "efficientnet_b4",
        num_classes: int = 2,
        pretrained: bool = True,
        dropout: float = 0.3
    ):
        """
        Args:
            model_name: Name of the pretrained model from timm
            num_classes: Number of output classes
            pretrained: Whether to use pretrained weights
            dropout: Dropout rate
        """
        super(BrainTumorClassifier, self).__init__()
        
        self.model_name = model_name
        self.num_classes = num_classes
        
        # Load pretrained model
        self.backbone = timm.create_model(
            model_name,
            pretrained=pretrained,
            num_classes=0  # Remove classifier
        )
        
        # Get number of features from backbone
        if hasattr(self.backbone, 'num_features'):
            num_features = self.backbone.num_features
        elif hasattr(self.backbone, 'feature_info'):
            num_features = self.backbone.feature_info[-1]['num_chs']
        else:
            # Default for most models
            num_features = 1000
        
        # Custom classifier head
        self.classifier = nn.Sequential(
            nn.Dropout(dropout),
            nn.Linear(num_features, 512),
            nn.ReLU(),
            nn.BatchNorm1d(512),
            nn.Dropout(dropout / 2),
            nn.Linear(512, num_classes)
        )
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass
        
        Args:
            x: Input tensor of shape (batch_size, 3, H, W)
            
        Returns:
            Logits of shape (batch_size, num_classes)
        """
        features = self.backbone(x)
        output = self.classifier(features)
        return output
    
    def get_features(self, x: torch.Tensor) -> torch.Tensor:
        """
        Get feature embeddings (useful for visualization)
        
        Args:
            x: Input tensor
            
        Returns:
            Feature embeddings
        """
        return self.backbone(x)


def create_model(
    model_type: str = "efficientnet_b4",
    num_classes: int = 2,
    pretrained: bool = True,
    dropout: float = 0.3,
    device: str = "cuda"
) -> BrainTumorClassifier:
    """
    Create and initialize model
    
    Args:
        model_type: Type of model architecture
        num_classes: Number of classes
        pretrained: Use pretrained weights
        dropout: Dropout rate
        device: Device to put model on
        
    Returns:
        Initialized model
    """
    model = BrainTumorClassifier(
        model_name=model_type,
        num_classes=num_classes,
        pretrained=pretrained,
        dropout=dropout
    )
    
    # Move to device
    device = torch.device(device if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    
    print(f"Created {model_type} model on {device}")
    print(f"Total parameters: {sum(p.numel() for p in model.parameters()):,}")
    print(f"Trainable parameters: {sum(p.numel() for p in model.parameters() if p.requires_grad):,}")
    
    return model


def load_checkpoint(
    model: BrainTumorClassifier,
    checkpoint_path: str,
    device: str = "cuda"
) -> BrainTumorClassifier:
    """
    Load model from checkpoint
    
    Args:
        model: Model instance
        checkpoint_path: Path to checkpoint file
        device: Device to load model on
        
    Returns:
        Model with loaded weights
    """
    device = torch.device(device if torch.cuda.is_available() else "cpu")
    checkpoint = torch.load(checkpoint_path, map_location=device)
    
    if 'model_state_dict' in checkpoint:
        model.load_state_dict(checkpoint['model_state_dict'])
    else:
        model.load_state_dict(checkpoint)
    
    model.eval()
    print(f"Loaded checkpoint from {checkpoint_path}")
    
    return model
