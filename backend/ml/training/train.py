"""
Full training script for brain tumor detection

This will train for 20-30 epochs with early stopping for best results.

Usage:
    cd backend
    python ml/training/train.py
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
import matplotlib.pyplot as plt

# Add parent to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from ml.models.model import create_model
from ml.data.dataset import BrainTumorDataset, get_train_transforms, get_val_transforms

def train_full_model(
    epochs=25,
    batch_size=16,
    lr=0.0001,
    patience=5,
    device='cuda' if torch.cuda.is_available() else 'cpu',
    save_dir='ml/checkpoints'
):
    """Full training with early stopping and checkpointing"""
    
    print("=" * 70)
    print("🚀 FULL MODEL TRAINING - Brain Tumor Detection")
    print("=" * 70)
    print(f"\nConfiguration:")
    print(f"  Device: {device}")
    print(f"  Max Epochs: {epochs}")
    print(f"  Batch Size: {batch_size}")
    print(f"  Learning Rate: {lr}")
    print(f"  Early Stopping Patience: {patience}")
    print(f"  Save Directory: {save_dir}\n")
    
    # Create save directory
    Path(save_dir).mkdir(parents=True, exist_ok=True)
    
    # Load splits
    splits_path = Path("../data/processed/splits.json")
    print(f"📂 Loading dataset splits from: {splits_path}")
    with open(splits_path) as f:
        splits = json.load(f)
    
    print(f"\n📊 Dataset Statistics:")
    print(f"  Training samples: {len(splits['train'])}")
    print(f"  Validation samples: {len(splits['val'])}")
    print(f"  Test samples: {len(splits['test'])}\n")
    
    # Load class weights
    weights_path = Path("../data/processed/class_weights.json")
    with open(weights_path) as f:
        class_weights_dict = json.load(f)
    class_weights = torch.tensor([class_weights_dict['0'], class_weights_dict['1']]).to(device)
    print(f"⚖️ Class Weights: {class_weights.tolist()}\n")
    
    # Create datasets
    train_images = [item['image_path'] for item in splits['train']]
    train_labels = [item['label'] for item in splits['train']]
    val_images = [item['image_path'] for item in splits['val']]
    val_labels = [item['label'] for item in splits['val']]
    
    print("🔄 Creating datasets with augmentation...")
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
        num_workers=0,
        pin_memory=True if device == 'cuda' else False
    )
    
    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=0,
        pin_memory=True if device == 'cuda' else False
    )
    
    print(f"✅ Dataloaders created:")
    print(f"  Train batches per epoch: {len(train_loader)}")
    print(f"  Validation batches: {len(val_loader)}\n")
    
    # Create model
    print("🤖 Creating EfficientNet-B4 model with pretrained weights...")
    model = create_model(
        model_type="efficientnet_b4",
        num_classes=2,
        pretrained=True,
        dropout=0.3,
        device=device
    )
    
    # Loss and optimizer
    criterion = nn.CrossEntropyLoss(weight=class_weights)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, mode='max', factor=0.5, patience=3
    )
    
    print(f"\n✅ Training setup complete!")
    print(f"  Loss: CrossEntropyLoss with class weights")
    print(f"  Optimizer: Adam (lr={lr})")
    print(f"  LR Scheduler: ReduceLROnPlateau\n")
    
    # Training variables
    best_val_acc = 0.0
    best_epoch = 0
    patience_counter = 0
    history = {
        'train_loss': [],
        'train_acc': [],
        'val_loss': [],
        'val_acc': [],
        'lr': []
    }
    
    print("=" * 70)
    print("STARTING TRAINING")
    print("=" * 70 + "\n")
    
    # Training loop
    for epoch in range(epochs):
        epoch_start = time.time()
        current_lr = optimizer.param_groups[0]['lr']
        
        print(f"\n{'='*70}")
        print(f"📈 Epoch {epoch+1}/{epochs} | LR: {current_lr:.6f}")
        print(f"{'='*70}\n")
        
        # TRAINING PHASE
        model.train()
        train_loss = 0.0
        train_correct = 0
        train_total = 0
        
        pbar = tqdm(train_loader, desc=f"Training Epoch {epoch+1}")
        for batch_idx, (images, labels) in enumerate(pbar):
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
            
            # Update progress bar
            current_acc = 100. * train_correct / train_total
            pbar.set_postfix({
                'loss': f'{loss.item():.4f}',
                'acc': f'{current_acc:.2f}%'
            })
        
        avg_train_loss = train_loss / len(train_loader)
        train_acc = 100. * train_correct / train_total
        
        # VALIDATION PHASE
        model.eval()
        val_loss = 0.0
        val_correct = 0
        val_total = 0
        
        with torch.no_grad():
            pbar = tqdm(val_loader, desc=f"Validation Epoch {epoch+1}")
            for images, labels in pbar:
                images = images.to(device)
                labels = labels.to(device)
                
                outputs = model(images)
                loss = criterion(outputs, labels)
                
                val_loss += loss.item()
                _, predicted = outputs.max(1)
                val_total += labels.size(0)
                val_correct += predicted.eq(labels).sum().item()
                
                current_val_acc = 100. * val_correct / val_total
                pbar.set_postfix({
                    'loss': f'{loss.item():.4f}',
                    'acc': f'{current_val_acc:.2f}%'
                })
        
        avg_val_loss = val_loss / len(val_loader)
        val_acc = 100. * val_correct / val_total
        
        # Update learning rate
        scheduler.step(val_acc)
        
        # Log metrics
        history['train_loss'].append(avg_train_loss)
        history['train_acc'].append(train_acc)
        history['val_loss'].append(avg_val_loss)
        history['val_acc'].append(val_acc)
        history['lr'].append(current_lr)
        
        epoch_time = time.time() - epoch_start
        
        # Print epoch summary
        print(f"\n{'─'*70}")
        print(f"  Train Loss: {avg_train_loss:.4f} | Train Acc: {train_acc:.2f}%")
        print(f"  Val Loss: {avg_val_loss:.4f} | Val Acc: {val_acc:.2f}%")
        print(f"  Time: {epoch_time:.1f}s")
        print(f"{'─'*70}")
        
        # Save best model
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            best_epoch = epoch + 1
            patience_counter = 0
            
            # Save checkpoint
            checkpoint_path = Path(save_dir) / 'best_model.pth'
            torch.save({
                'epoch': epoch + 1,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'val_acc': val_acc,
                'train_acc': train_acc,
                'history': history
            }, checkpoint_path)
            
            print(f"  ⭐ NEW BEST! Saved checkpoint to: {checkpoint_path}")
            print(f"  Best Val Acc: {best_val_acc:.2f}%")
        else:
            patience_counter += 1
            print(f"  Patience: {patience_counter}/{patience} (Best: {best_val_acc:.2f}% at epoch {best_epoch})")
        
        # Early stopping
        if patience_counter >= patience:
            print(f"\n⏹️ Early stopping triggered! No improvement for {patience} epochs.")
            break
    
    # Training complete
    print("\n" + "=" * 70)
    print("✅ TRAINING COMPLETE!")
    print("=" * 70)
    print(f"\n🏆 Best Results:")
    print(f"  Best Validation Accuracy: {best_val_acc:.2f}%")
    print(f"  Achieved at Epoch: {best_epoch}")
    print(f"  Model saved at: {Path(save_dir) / 'best_model.pth'}")
    
    # Save training history
    history_path = Path(save_dir) / 'training_history.json'
    with open(history_path, 'w') as f:
        json.dump(history, f, indent=2)
    print(f"  Training history saved: {history_path}")
    
    # Plot training curves
    try:
        plot_training_curves(history, save_dir)
        print(f"  Training curves saved: {Path(save_dir) / 'training_curves.png'}")
    except Exception as e:
        print(f"  Warning: Could not save plots: {e}")
    
    print("\n" + "=" * 70)
    print("🎉 Model training finished successfully!")
    print("=" * 70)
    print("\n📝 Next steps:")
    print("  1. Check training curves in ml/checkpoints/")
    print("  2. Update backend/.env MODEL_PATH=ml/checkpoints/best_model.pth")
    print("  3. Restart backend server")
    print("  4. Test predictions on frontend!")
    print("=" * 70 + "\n")

def plot_training_curves(history, save_dir):
    """Plot and save training curves"""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
    
    epochs = range(1, len(history['train_loss']) + 1)
    
    # Loss
    ax1.plot(epochs, history['train_loss'], 'b-', label='Train Loss')
    ax1.plot(epochs, history['val_loss'], 'r-', label='Val Loss')
    ax1.set_title('Training and Validation Loss')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Loss')
    ax1.legend()
    ax1.grid(True)
    
    # Accuracy
    ax2.plot(epochs, history['train_acc'], 'b-', label='Train Acc')
    ax2.plot(epochs, history['val_acc'], 'r-', label='Val Acc')
    ax2.set_title('Training and Validation Accuracy')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Accuracy (%)')
    ax2.legend()
    ax2.grid(True)
    
    # Learning Rate
    ax3.plot(epochs, history['lr'], 'g-')
    ax3.set_title('Learning Rate Schedule')
    ax3.set_xlabel('Epoch')
    ax3.set_ylabel('Learning Rate')
    ax3.set_yscale('log')
    ax3.grid(True)
    
    # Best metrics
    best_val_acc = max(history['val_acc'])
    best_epoch = history['val_acc'].index(best_val_acc) + 1
    ax4.text(0.5, 0.7, f"Best Validation Accuracy:", ha='center', fontsize=14, weight='bold')
    ax4.text(0.5, 0.5, f"{best_val_acc:.2f}%", ha='center', fontsize=24, weight='bold', color='green')
    ax4.text(0.5, 0.3, f"at Epoch {best_epoch}", ha='center', fontsize=12)
    ax4.axis('off')
    
    plt.tight_layout()
    plt.savefig(Path(save_dir) / 'training_curves.png', dpi=150)
    plt.close()

if __name__ == "__main__":
    train_full_model()
