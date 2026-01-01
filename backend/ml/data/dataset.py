"""
Data loading and preprocessing utilities for brain tumor detection
"""
import os
import torch
from torch.utils.data import Dataset, DataLoader
from PIL import Image
import numpy as np
from typing import Tuple, Optional, List
import albumentations as A
from albumentations.pytorch import ToTensorV2


class BrainTumorDataset(Dataset):
    """Custom dataset for brain tumor MRI images"""
    
    def __init__(
        self, 
        image_paths: List[str], 
        labels: List[int], 
        transform=None
    ):
        """
        Args:
            image_paths: List of paths to MRI images
            labels: List of labels (0 for no tumor, 1 for tumor)
            transform: Albumentations transform to apply
        """
        self.image_paths = image_paths
        self.labels = labels
        self.transform = transform
    
    def __len__(self) -> int:
        return len(self.image_paths)
    
    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, int]:
        # Load image
        img_path = self.image_paths[idx]
        image = Image.open(img_path).convert('RGB')
        image = np.array(image)
        
        # Apply transforms
        if self.transform:
            augmented = self.transform(image=image)
            image = augmented['image']
        
        label = self.labels[idx]
        return image, label


def get_train_transforms(image_size: int = 224) -> A.Compose:
    """Get training transforms with data augmentation"""
    return A.Compose([
        A.Resize(image_size, image_size),
        A.HorizontalFlip(p=0.5),
        A.VerticalFlip(p=0.3),
        A.RandomRotate90(p=0.5),
        A.ShiftScaleRotate(shift_limit=0.1, scale_limit=0.1, rotate_limit=15, p=0.5),
        A.RandomBrightnessContrast(brightness_limit=0.2, contrast_limit=0.2, p=0.5),
        A.GaussNoise(var_limit=(10.0, 50.0), p=0.3),
        A.GaussianBlur(blur_limit=(3, 5), p=0.2),
        A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ToTensorV2(),
    ])


def get_val_transforms(image_size: int = 224) -> A.Compose:
    """Get validation/test transforms (no augmentation)"""
    return A.Compose([
        A.Resize(image_size, image_size),
        A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ToTensorV2(),
    ])


def get_inference_transform(image_size: int = 224) -> A.Compose:
    """Get transform for inference (single image prediction)"""
    return get_val_transforms(image_size)
