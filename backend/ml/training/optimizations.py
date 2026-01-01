"""
Advanced Training Optimizations
Learning rate scheduling, mixed precision, and loss functions
"""

import torch
import torch.nn as nn
from torch.optim.lr_scheduler import _LRScheduler
import math


class CosineAnnealingWarmRestarts(_LRScheduler):
    """Cosine annealing with warm restarts"""
    
    def __init__(
        self,
        optimizer,
        T_0: int,
        T_mult: int = 1,
        eta_min: float = 0,
        last_epoch: int = -1
    ):
        """
        Args:
            T_0: Number of iterations for the first restart
            T_mult: Factor to increase T_i after each restart
            eta_min: Minimum learning rate
        """
        self.T_0 = T_0
        self.T_mult = T_mult
        self.eta_min = eta_min
        self.T_cur = last_epoch
        self.T_i = T_0
        super().__init__(optimizer, last_epoch)
    
    def get_lr(self):
        return [
            self.eta_min + (base_lr - self.eta_min) *
            (1 + math.cos(math.pi * self.T_cur / self.T_i)) / 2
            for base_lr in self.base_lrs
        ]
    
    def step(self, epoch=None):
        if epoch is None:
            epoch = self.last_epoch + 1
            self.T_cur = self.T_cur + 1
            if self.T_cur >= self.T_i:
                self.T_cur = 0
                self.T_i = self.T_i * self.T_mult
        else:
            self.T_cur = epoch
        self.last_epoch = math.floor(epoch)
        
        for param_group, lr in zip(self.optimizer.param_groups, self.get_lr()):
            param_group['lr'] = lr


class LabelSmoothingCrossEntropy(nn.Module):
    """Label smoothing for better generalization"""
    
    def __init__(self, smoothing: float = 0.1):
        """
        Args:
            smoothing: Label smoothing factor (0 = no smoothing, 1 = uniform)
        """
        super().__init__()
        self.smoothing = smoothing
        self.confidence = 1.0 - smoothing
    
    def forward(self, pred: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        """
        Args:
            pred: Predictions (logits)
            target: Ground truth labels
            
        Returns:
            Loss value
        """
        pred = pred.log_softmax(dim=-1)
        
        with torch.no_grad():
            true_dist = torch.zeros_like(pred)
            true_dist.fill_(self.smoothing / (pred.size(-1) - 1))
            true_dist.scatter_(1, target.unsqueeze(1), self.confidence)
        
        return torch.mean(torch.sum(-true_dist * pred, dim=-1))


class FocalLoss(nn.Module):
    """Focal loss for handling class imbalance"""
    
    def __init__(self, alpha: float = 0.25, gamma: float = 2.0):
        """
        Args:
            alpha: Weighting factor for class balance
            gamma: Focusing parameter (higher = focus more on hard examples)
        """
        super().__init__()
        self.alpha = alpha
        self.gamma = gamma
    
    def forward(self, pred: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        """
        Args:
            pred: Predictions (logits)
            target: Ground truth labels
            
        Returns:
            Loss value
        """
        ce_loss = F.cross_entropy(pred, target, reduction='none')
        p_t = torch.exp(-ce_loss)
        focal_loss = self.alpha * (1 - p_t) ** self.gamma * ce_loss
        return focal_loss.mean()


class MixedPrecisionTrainer:
    """Trainer with automatic mixed precision"""
    
    def __init__(self, model: nn.Module, optimizer: torch.optim.Optimizer, device: str = 'cuda'):
        """
        Initialize mixed precision trainer
        
        Args:
            model: PyTorch model
            optimizer: Optimizer
            device: Device to train on
        """
        self.model = model
        self.optimizer = optimizer
        self.device = device
        self.scaler = torch.cuda.amp.GradScaler()
    
    def train_step(
        self,
        images: torch.Tensor,
        labels: torch.Tensor,
        criterion: nn.Module
    ) -> float:
        """
        Single training step with mixed precision
        
        Args:
            images: Input images
            labels: Ground truth labels
            criterion: Loss function
            
        Returns:
            Loss value
        """
        self.optimizer.zero_grad()
        
        # Forward pass with autocast
        with torch.cuda.amp.autocast():
            outputs = self.model(images)
            loss = criterion(outputs, labels)
        
        # Backward pass with gradient scaling
        self.scaler.scale(loss).backward()
        self.scaler.step(self.optimizer)
        self.scaler.update()
        
        return loss.item()


def progressive_unfreeze(
    model: nn.Module,
    epoch: int,
    total_epochs: int,
    num_stages: int = 3
):
    """
    Progressively unfreeze model layers
    
    Args:
        model: PyTorch model
        epoch: Current epoch
        total_epochs: Total number of epochs
        num_stages: Number of unfreezing stages
    """
    stage_length = total_epochs // num_stages
    current_stage = min(epoch // stage_length, num_stages - 1)
    
    # Get all parameter groups
    param_groups = list(model.parameters())
    num_params = len(param_groups)
    
    # Calculate which layers to unfreeze
    layers_per_stage = num_params // num_stages
    unfreeze_up_to = (current_stage + 1) * layers_per_stage
    
    # Unfreeze layers
    for i, param in enumerate(param_groups):
        param.requires_grad = (i >= num_params - unfreeze_up_to)
    
    print(f"Epoch {epoch}: Unfroze top {unfreeze_up_to}/{num_params} parameter groups")


# Example usage
def create_optimized_training_setup(model: nn.Module, base_lr: float = 1e-4):
    """
    Create optimized training setup
    
    Args:
        model: Model to train
        base_lr: Base learning rate
        
    Returns:
        optimizer, scheduler, criterion
    """
    # Discriminative learning rates
    optimizer = torch.optim.Adam([
        {'params': model.model.parameters(), 'lr': base_lr / 10},  # Backbone
        {'params': model.classifier.parameters(), 'lr': base_lr}    # Classifier
    ])
    
    # Cosine annealing scheduler
    scheduler = CosineAnnealingWarmRestarts(
        optimizer,
        T_0=10,
        T_mult=2,
        eta_min=base_lr / 100
    )
    
    # Label smoothing loss
    criterion = LabelSmoothingCrossEntropy(smoothing=0.1)
    
    return optimizer, scheduler, criterion
