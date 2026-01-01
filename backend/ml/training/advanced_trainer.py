"""
Training script with advanced augmentation
Demonstrates how to use the augmentation pipeline for training
"""

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import numpy as np
from typing import Dict
import time

from ml.data.augmentation import (
    get_augmentation,
    MixUpAugmentation,
    CutMixAugmentation
)


class AdvancedTrainer:
    """Trainer with advanced augmentation techniques"""
    
    def __init__(
        self,
        model: nn.Module,
        device: str = 'cuda',
        use_mixup: bool = True,
        use_cutmix: bool = True,
        mixup_alpha: float = 0.2,
        cutmix_alpha: float = 1.0,
        augmentation_prob: float = 0.5
    ):
        """
        Initialize trainer
        
        Args:
            model: PyTorch model
            device: Device to train on
            use_mixup: Whether to use MixUp
            use_cutmix: Whether to use CutMix
            mixup_alpha: MixUp parameter
            cutmix_alpha: CutMix parameter
            augmentation_prob: Probability of applying mix augmentation
        """
        self.model = model.to(device)
        self.device = device
        self.use_mixup = use_mixup
        self.use_cutmix = use_cutmix
        self.augmentation_prob = augmentation_prob
        
        if use_mixup:
            self.mixup = MixUpAugmentation(alpha=mixup_alpha)
        if use_cutmix:
            self.cutmix = CutMixAugmentation(alpha=cutmix_alpha)
    
    def train_epoch(
        self,
        train_loader: DataLoader,
        optimizer: torch.optim.Optimizer,
        criterion: nn.Module,
        epoch: int
    ) -> Dict[str, float]:
        """
        Train for one epoch with augmentation
        
        Args:
            train_loader: Training data loader
            optimizer: Optimizer
            criterion: Loss function
            epoch: Current epoch
            
        Returns:
            Training metrics
        """
        self.model.train()
        total_loss = 0
        correct = 0
        total = 0
        
        for batch_idx, (images, labels) in enumerate(train_loader):
            images = images.to(self.device)
            labels = labels.to(self.device)
            
            # Randomly apply MixUp or CutMix
            if np.random.rand() < self.augmentation_prob:
                # Get random indices for mixing
                indices = torch.randperm(images.size(0))
                images2 = images[indices]
                labels2 = labels[indices]
                
                # Randomly choose between MixUp and CutMix
                if self.use_mixup and self.use_cutmix:
                    if np.random.rand() < 0.5:
                        images, labels = self.mixup(images, labels, images2, labels2)
                    else:
                        images, labels = self.cutmix(images, labels, images2, labels2)
                elif self.use_mixup:
                    images, labels = self.mixup(images, labels, images2, labels2)
                elif self.use_cutmix:
                    images, labels = self.cutmix(images, labels, images2, labels2)
            
            # Forward pass
            optimizer.zero_grad()
            outputs = self.model(images)
            
            # Handle mixed labels
            if len(labels.shape) > 1:  # Soft labels from MixUp/CutMix
                loss = -torch.sum(labels * torch.log_softmax(outputs, dim=1), dim=1).mean()
            else:  # Hard labels
                loss = criterion(outputs, labels)
            
            # Backward pass
            loss.backward()
            optimizer.step()
            
            # Statistics
            total_loss += loss.item()
            if len(labels.shape) == 1:  # Only calculate accuracy for hard labels
                pred = outputs.argmax(dim=1)
                correct += pred.eq(labels).sum().item()
                total += labels.size(0)
        
        metrics = {
            'loss': total_loss / len(train_loader),
            'accuracy': correct / total if total > 0 else 0
        }
        
        return metrics


# Example usage for training
def example_training():
    """Example of how to use advanced augmentation for training"""
    
    # 1. Create model
    from ml.models.model import BrainTumorClassifier
    model = BrainTumorClassifier(model_name='efficientnet_b4', num_classes=2)
    
    # 2. Create data loaders with advanced augmentation
    from ml.data.dataset import BrainTumorDataset
    
    train_transform = get_augmentation(image_size=224, mode='train')
    val_transform = get_augmentation(image_size=224, mode='val')
    
    # 3. Create trainer with MixUp and CutMix
    trainer = AdvancedTrainer(
        model=model,
        device='cuda',
        use_mixup=True,
        use_cutmix=True,
        mixup_alpha=0.2,
        cutmix_alpha=1.0,
        augmentation_prob=0.5
    )
    
    # 4. Train
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)
    criterion = nn.CrossEntropyLoss()
    
    print("Training with advanced augmentation:")
    print("- Albumentations: CLAHE, ElasticTransform, GridDistortion, etc.")
    print("- MixUp: alpha=0.2")
    print("- CutMix: alpha=1.0")
    print("- Augmentation probability: 50%")
