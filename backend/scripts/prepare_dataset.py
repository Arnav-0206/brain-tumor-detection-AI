"""
Dataset preparation script for brain tumor detection

Usage:
    python scripts/prepare_dataset.py
"""
import os
import json
import shutil
from pathlib import Path
from collections import Counter
import random

# Add parent directory to path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from sklearn.model_selection import train_test_split


def prepare_binary_classification(
    raw_data_dir: str = "../data/raw",
    processed_data_dir: str = "../data/processed",
    test_size: float = 0.15,
    val_size: float = 0.15,
    random_seed: int = 42
):
    """
    Prepare dataset for binary classification (tumor vs no_tumor)
    
    Args:
        raw_data_dir: Directory containing raw images
        processed_data_dir: Directory to save processed splits
        test_size: Proportion for test set
        val_size: Proportion for validation set
        random_seed: Random seed for reproducibility
    """
    print("=" * 60)
    print("Brain Tumor Dataset Preparation")
    print("=" * 60)
    
    raw_path = Path(raw_data_dir)
    processed_path = Path(processed_data_dir)
    
    # Find all images
    tumor_classes = ['glioma_tumor', 'meningioma_tumor', 'pituitary_tumor', 'glioma', 'meningioma', 'pituitary']
    no_tumor_classes = ['no_tumor', 'notumor']
    
    tumor_images = []
    no_tumor_images = []
    
    print("\n📂 Scanning for images...")
    
    # Search in Training and Testing folders
    for folder in ['Training', 'Testing', 'train', 'test', '']:
        folder_path = raw_path / folder if folder else raw_path
        if not folder_path.exists():
            continue
            
        print(f"  Checking: {folder_path}")
        
        # Check tumor classes
        for tumor_class in tumor_classes:
            class_path = folder_path / tumor_class
            if class_path.exists():
                images = list(class_path.glob('*.jpg')) + list(class_path.glob('*.png')) + list(class_path.glob('*.jpeg'))
                tumor_images.extend([(str(img), 1) for img in images])
                print(f"    ✓ Found {len(images)} images in {tumor_class}")
        
        # Check no tumor classes
        for no_tumor_class in no_tumor_classes:
            class_path = folder_path / no_tumor_class
            if class_path.exists():
                images = list(class_path.glob('*.jpg')) + list(class_path.glob('*.png')) + list(class_path.glob('*.jpeg'))
                no_tumor_images.extend([(str(img), 0) for img in images])
                print(f"    ✓ Found {len(images)} images in {no_tumor_class}")
    
    # Combine all images
    all_data = tumor_images + no_tumor_images
    
    if len(all_data) == 0:
        print("\n❌ No images found! Please check:")
        print(f"   1. Raw data directory: {raw_path.absolute()}")
        print(f"   2. Folder structure matches expected format")
        print(f"   3. Images are in JPG/PNG format")
        return
    
    print(f"\n📊 Dataset Statistics:")
    print(f"  Total images: {len(all_data)}")
    print(f"  Tumor: {len(tumor_images)} ({len(tumor_images)/len(all_data)*100:.1f}%)")
    print(f"  No Tumor: {len(no_tumor_images)} ({len(no_tumor_images)/len(all_data)*100:.1f}%)")
    
    # Shuffle
    random.seed(random_seed)
    random.shuffle(all_data)
    
    # Split data
    images, labels = zip(*all_data)
    
    # First split: train+val vs test
    train_val_images, test_images, train_val_labels, test_labels = train_test_split(
        images, labels, 
        test_size=test_size, 
        stratify=labels,
        random_state=random_seed
    )
    
    # Second split: train vs val
    val_size_adjusted = val_size / (1 - test_size)
    train_images, val_images, train_labels, val_labels = train_test_split(
        train_val_images, train_val_labels,
        test_size=val_size_adjusted,
        stratify=train_val_labels,
        random_state=random_seed
    )
    
    # Create splits dictionary
    splits = {
        'train': [
            {'image_path': img, 'label': label}
            for img, label in zip(train_images, train_labels)
        ],
        'val': [
            {'image_path': img, 'label': label}
            for img, label in zip(val_images, val_labels)
        ],
        'test': [
            {'image_path': img, 'label': label}
            for img, label in zip(test_images, test_labels)
        ]
    }
    
    # Save splits
    processed_path.mkdir(parents=True, exist_ok=True)
    splits_file = processed_path / 'splits.json'
    
    with open(splits_file, 'w') as f:
        json.dump(splits, f, indent=2)
    
    print(f"\n✅ Splits created successfully!")
    print(f"  Train: {len(train_images)} images")
    print(f"  Val: {len(val_images)} images")
    print(f"  Test: {len(test_images)} images")
    print(f"\n  Saved to: {splits_file.absolute()}")
    
    # Calculate class weights
    train_label_counts = Counter(train_labels)
    total_train = len(train_labels)
    class_weights = {
        0: total_train / (2 * train_label_counts[0]),  # no_tumor
        1: total_train / (2 * train_label_counts[1])   # tumor
    }
    
    print(f"\n⚖️ Class Weights (for balanced training):")
    print(f"  No Tumor (0): {class_weights[0]:.3f}")
    print(f"  Tumor (1): {class_weights[1]:.3f}")
    
    # Save class weights
    weights_file = processed_path / 'class_weights.json'
    with open(weights_file, 'w') as f:
        json.dump(class_weights, f, indent=2)
    
    print(f"  Saved to: {weights_file.absolute()}")
    
    print("\n" + "=" * 60)
    print("✅ Dataset preparation complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("  1. Review the splits.json file")
    print("  2. Run training: python ml/training/train.py")
    print("=" * 60)


if __name__ == "__main__":
    prepare_binary_classification()
