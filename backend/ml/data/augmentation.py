"""
Advanced Data Augmentation for training
Uses albumentations for state-of-the-art augmentation techniques
"""

import albumentations as A
from albumentations.pytorch import ToTensorV2
import numpy as np
import cv2
from typing import Dict, Tuple
import torch


class AdvancedAugmentation:
    """Advanced augmentation pipeline for training"""
    
    def __init__(self, image_size: int = 224, mode: str = 'train'):
        """
        Initialize augmentation pipeline
        
        Args:
            image_size: Target image size
            mode: 'train', 'val', or 'test'
        """
        self.image_size = image_size
        self.mode = mode
        
        if mode == 'train':
            self.transform = self._get_train_transform()
        else:
            self.transform = self._get_val_transform()
    
    def _get_train_transform(self) -> A.Compose:
        """Get training augmentations"""
        return A.Compose([
            # Geometric transformations
            A.Resize(self.image_size, self.image_size),
            A.HorizontalFlip(p=0.5),
            A.VerticalFlip(p=0.3),
            A.Rotate(limit=15, p=0.5),
            A.ShiftScaleRotate(
                shift_limit=0.1,
                scale_limit=0.1,
                rotate_limit=15,
                p=0.5
            ),
            
            # Advanced spatial transforms
            A.ElasticTransform(
                alpha=1,
                sigma=50,
                alpha_affine=50,
                p=0.3
            ),
            A.GridDistortion(
                num_steps=5,
                distort_limit=0.3,
                p=0.3
            ),
            A.OpticalDistortion(
                distort_limit=0.5,
                shift_limit=0.5,
                p=0.3
            ),
            
            # Image quality augmentations
            A.CLAHE(clip_limit=2.0, p=0.5),  # Contrast enhancement
            A.RandomBrightnessContrast(
                brightness_limit=0.2,
                contrast_limit=0.2,
                p=0.5
            ),
            A.RandomGamma(gamma_limit=(80, 120), p=0.3),
            
            # Noise and blur
            A.GaussNoise(var_limit=(10.0, 50.0), p=0.3),
            A.GaussianBlur(blur_limit=(3, 7), p=0.2),
            A.MotionBlur(blur_limit=7, p=0.2),
            
            # Color augmentations
            A.HueSaturationValue(
                hue_shift_limit=10,
                sat_shift_limit=20,
                val_shift_limit=10,
                p=0.3
            ),
            A.RGBShift(
                r_shift_limit=15,
                g_shift_limit=15,
                b_shift_limit=15,
                p=0.3
            ),
            
            # Advanced techniques
            A.CoarseDropout(
                max_holes=8,
                max_height=32,
                max_width=32,
                min_holes=1,
                p=0.3
            ),
            
            # Normalization
            A.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225],
            ),
            ToTensorV2(),
        ])
    
    def _get_val_transform(self) -> A.Compose:
        """Get validation/test augmentations"""
        return A.Compose([
            A.Resize(self.image_size, self.image_size),
            A.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225],
            ),
            ToTensorV2(),
        ])
    
    def __call__(self, image: np.ndarray, **kwargs) -> Dict:
        """
        Apply augmentation
        
        Args:
            image: Input image as numpy array
            
        Returns:
            Augmented image dictionary
        """
        return self.transform(image=image, **kwargs)


class MixUpAugmentation:
    """MixUp data augmentation"""
    
    def __init__(self, alpha: float = 0.2):
        """
        Initialize MixUp
        
        Args:
            alpha: Beta distribution parameter
        """
        self.alpha = alpha
    
    def __call__(
        self,
        image1: torch.Tensor,
        label1: torch.Tensor,
        image2: torch.Tensor,
        label2: torch.Tensor
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Apply MixUp augmentation
        
        Args:
            image1, label1: First sample
            image2, label2: Second sample
            
        Returns:
            Mixed image and label
        """
        if self.alpha > 0:
            lam = np.random.beta(self.alpha, self.alpha)
        else:
            lam = 1
        
        # Mix images
        mixed_image = lam * image1 + (1 - lam) * image2
        
        # Mix labels (convert to one-hot if needed)
        if len(label1.shape) == 0:  # Single class label
            num_classes = 2  # Binary classification
            label1_onehot = torch.zeros(num_classes)
            label1_onehot[label1] = 1
            label2_onehot = torch.zeros(num_classes)
            label2_onehot[label2] = 1
            mixed_label = lam * label1_onehot + (1 - lam) * label2_onehot
        else:
            mixed_label = lam * label1 + (1 - lam) * label2
        
        return mixed_image, mixed_label


class CutMixAugmentation:
    """CutMix data augmentation"""
    
    def __init__(self, alpha: float = 1.0):
        """
        Initialize CutMix
        
        Args:
            alpha: Beta distribution parameter
        """
        self.alpha = alpha
    
    def _rand_bbox(self, size: Tuple, lam: float) -> Tuple[int, int, int, int]:
        """Generate random bounding box"""
        W = size[2]
        H = size[3]
        cut_rat = np.sqrt(1.0 - lam)
        cut_w = int(W * cut_rat)
        cut_h = int(H * cut_rat)
        
        # Uniform sampling
        cx = np.random.randint(W)
        cy = np.random.randint(H)
        
        bbx1 = np.clip(cx - cut_w // 2, 0, W)
        bby1 = np.clip(cy - cut_h // 2, 0, H)
        bbx2 = np.clip(cx + cut_w // 2, 0, W)
        bby2 = np.clip(cy + cut_h // 2, 0, H)
        
        return bbx1, bby1, bbx2, bby2
    
    def __call__(
        self,
        image1: torch.Tensor,
        label1: torch.Tensor,
        image2: torch.Tensor,
        label2: torch.Tensor
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Apply CutMix augmentation
        
        Args:
            image1, label1: First sample
            image2, label2: Second sample
            
        Returns:
            Mixed image and label
        """
        if self.alpha > 0:
            lam = np.random.beta(self.alpha, self.alpha)
        else:
            lam = 1
        
        # Get bounding box
        bbx1, bby1, bbx2, bby2 = self._rand_bbox(image1.size(), lam)
        
        # Cut and paste
        mixed_image = image1.clone()
        mixed_image[:, :, bbx1:bbx2, bby1:bby2] = image2[:, :, bbx1:bbx2, bby1:bby2]
        
        # Adjust lambda based on actual cut area
        lam = 1 - ((bbx2 - bbx1) * (bby2 - bby1) / (image1.size()[-1] * image1.size()[-2]))
        
        # Mix labels
        if len(label1.shape) == 0:
            num_classes = 2
            label1_onehot = torch.zeros(num_classes)
            label1_onehot[label1] = 1
            label2_onehot = torch.zeros(num_classes)
            label2_onehot[label2] = 1
            mixed_label = lam * label1_onehot + (1 - lam) * label2_onehot
        else:
            mixed_label = lam * label1 + (1 - lam) * label2
        
        return mixed_image, mixed_label


def get_augmentation(image_size: int = 224, mode: str = 'train') -> AdvancedAugmentation:
    """
    Get augmentation pipeline
    
    Args:
        image_size: Target image size
        mode: 'train', 'val', or 'test'
        
    Returns:
        Augmentation pipeline
    """
    return AdvancedAugmentation(image_size=image_size, mode=mode)
