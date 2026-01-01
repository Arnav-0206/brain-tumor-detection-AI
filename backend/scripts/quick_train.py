"""
Quick training script for testing the pipeline

Usage:
    python scripts/quick_train.py
"""
import os
import sys
import json
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from pathlib import Path
import time
from tqdm import tqdm

# Add parent to path
sys.path.append(str(Path(__file__).parent.parent))

from ml.models.model import create_model
from ml.data.dataset import BrainTumorDataset, get_train_transforms, get_val_transforms

def quick_train(
    epochs=3,
    batch_size=16,
    lr=0.001,
    device='cuda' if torch.cuda.is_available() else 'cpu'
):
    """Quick training test"""
    
    print("=" * 60)
    print("🚀 Quick Training Test (3 epochs)")
    print("=" * 60)
    print(f"\nDevice: {device}")
    print(f"Epochs: {epochs}")
    print(f"Batch size: {batch_size}")
    print(f"Learning rate: {lr}\n")
    
    # Load splits
    splits_path = Path("../data/processed/splits.json")
    with open(splits_path) as f:
        splits = json.load(f)
    
    print(f"📊 Dataset sizes:")
    print(f"  Train: {len(splits['train'])}")
    print(f"  Val: {len(splits['val'])}\n")
    
    # Create datasets
    train_images = [item['image_path'] for item in splits['train']]
    train_labels = [item['label'] for item in splits['train']]
    val_images = [item['image_path'] for item in splits['val']]
    val_labels = [item['label'] for item in splits['val']]
    
    train_dataset = BrainTumorDataset(
        train_images,
        train_labels,
        transform=get_train_transforms(224)
    )
    
    val_dataset = BrainTumorDataset(
        val_images,
        val_labels,
        transform=get_val_transforms(224)
    )
    
    # Create dataloaders
    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=0,  # Windows compatibility
        pin_memory=True if device == 'cuda' else False
    )
    
    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=0,
        pin_memory=True if device == 'cuda' else False
    )
    
    print(f"✅ Dataloaders created")
    print(f"  Train batches: {len(train_loader)}")
    print(f"  Val batches: {len(val_loader)}\n")
    
    # Create model
    print("🤖 Creating EfficientNet-B4 model...")
    model = create_model(
        model_type="efficientnet_b4",
        num_classes=2,
        pretrained=True,
        device=device
    )
    
    # Loss and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    
    print("\n" + "=" * 60)
    print("Starting Training...")
    print("=" * 60 + "\n")
    
    # Training loop
    best_val_acc = 0.0
    
    for epoch in range(epochs):
        print(f"\n📈 Epoch {epoch+1}/{epochs}")
        print("-" * 40)
        
        # Training
        model.train()
        train_loss = 0.0
        train_correct = 0
        train_total = 0
        
        pbar = tqdm(train_loader, desc="Training")
        for images, labels in pbar:
            images = images.to(device)
            labels = labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item()
            _, predicted = outputs.max(1)
            train_total += labels.size(0)
            train_correct += predicted.eq(labels).sum().item()
            
            pbar.set_postfix({
                'loss': f'{loss.item():.4f}',
                'acc': f'{100.*train_correct/train_total:.2f}%'
            })
        
        train_acc = 100. * train_correct / train_total
        avg_train_loss = train_loss / len(train_loader)
        
        # Validation
        model.eval()
        val_loss = 0.0
        val_correct = 0
        val_total = 0
        
        with torch.no_grad():
            pbar = tqdm(val_loader, desc="Validation")
            for images, labels in pbar:
                images = images.to(device)
                labels = labels.to(device)
                
                outputs = model(images)
                loss = criterion(outputs, labels)
                
                val_loss += loss.item()
                _, predicted = outputs.max(1)
                val_total += labels.size(0)
                val_correct += predicted.eq(labels).sum().item()
                
                pbar.set_postfix({
                    'loss': f'{loss.item():.4f}',
                    'acc': f'{100.*val_correct/val_total:.2f}%'
                })
        
        val_acc = 100. * val_correct / val_total
        avg_val_loss = val_loss / len(val_loader)
        
        print(f"\n  Train Loss: {avg_train_loss:.4f} | Train Acc: {train_acc:.2f}%")
        print(f"  Val Loss: {avg_val_loss:.4f} | Val Acc: {val_acc:.2f}%")
        
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            print(f"  ⭐ New best validation accuracy!")
    
    print("\n" + "=" * 60)
    print("✅ Quick Test Complete!")
    print("=" * 60)
    print(f"\n🎯 Best Validation Accuracy: {best_val_acc:.2f}%")
    print("\n💡 Training pipeline works! Ready for full training.")
    print("\nTo run full training:")
    print("  python ml/training/train.py")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    quick_train()
