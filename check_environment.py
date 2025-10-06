#!/usr/bin/env python
"""
DuoRec Environment Diagnostic Tool
Run this to check if your environment is properly configured.
"""

import sys

print("=" * 70)
print("DuoRec Environment Diagnostic")
print("=" * 70)

# Check Python version
print(f"\n1. Python Version:")
print(f"   {sys.version}")
if sys.version_info < (3, 8):
    print("   ⚠️  WARNING: Python 3.8+ recommended")
else:
    print("   ✅ OK")

# Check PyTorch
print(f"\n2. PyTorch:")
try:
    import torch
    print(f"   Version: {torch.__version__}")
    print(f"   ✅ Installed")
except ImportError:
    print("   ❌ NOT INSTALLED - Run: pip install torch")
    sys.exit(1)

# Check CUDA availability
print(f"\n3. CUDA/GPU:")
try:
    cuda_available = torch.cuda.is_available()
    print(f"   CUDA Available: {cuda_available}")
    
    if cuda_available:
        print(f"   CUDA Version: {torch.version.cuda}")
        print(f"   GPU Count: {torch.cuda.device_count()}")
        for i in range(torch.cuda.device_count()):
            print(f"   GPU {i}: {torch.cuda.get_device_name(i)}")
        print(f"   ✅ GPU READY - Training will use GPU")
    else:
        print(f"   ⚠️  No GPU detected - Training will use CPU (slower)")
        print(f"   Tip: On Kaggle, enable GPU in Settings → Accelerator")
except Exception as e:
    print(f"   ❌ Error checking CUDA: {e}")

# Check NumPy
print(f"\n4. NumPy:")
try:
    import numpy as np
    version = np.__version__
    print(f"   Version: {version}")
    major, minor = map(int, version.split('.')[:2])
    if major >= 1 and minor >= 20:
        print(f"   ✅ Version OK (1.20+ required)")
    else:
        print(f"   ⚠️  WARNING: NumPy 1.20+ recommended (you have {version})")
except ImportError:
    print("   ❌ NOT INSTALLED - Run: pip install numpy")

# Check Pandas
print(f"\n5. Pandas:")
try:
    import pandas as pd
    version = pd.__version__
    print(f"   Version: {version}")
    print(f"   ✅ Installed")
except ImportError:
    print("   ❌ NOT INSTALLED - Run: pip install pandas")

# Check other dependencies
print(f"\n6. Other Dependencies:")
deps = [
    ('scipy', 'scipy'),
    ('sklearn', 'scikit-learn'),
    ('yaml', 'pyyaml'),
    ('tqdm', 'tqdm'),
]

for module_name, package_name in deps:
    try:
        __import__(module_name)
        print(f"   ✅ {package_name}")
    except ImportError:
        print(f"   ❌ {package_name} - Run: pip install {package_name}")

# Check dataset
print(f"\n7. Dataset Location:")
import os

dataset_path = "./dataset/ml-1m/"
if os.path.exists(dataset_path):
    print(f"   Path: {os.path.abspath(dataset_path)}")
    required_files = ['ml-1m.inter', 'ml-1m.item', 'ml-1m.user']
    for file in required_files:
        file_path = os.path.join(dataset_path, file)
        if os.path.exists(file_path):
            size_mb = os.path.getsize(file_path) / (1024 * 1024)
            print(f"   ✅ {file} ({size_mb:.2f} MB)")
        else:
            print(f"   ❌ {file} NOT FOUND")
else:
    print(f"   ❌ Dataset directory not found: {dataset_path}")
    print(f"   Current directory: {os.getcwd()}")
    print(f"   Make sure you run from the project root!")

# Check RecBole
print(f"\n8. RecBole Module:")
recbole_path = "./recbole/"
if os.path.exists(recbole_path):
    print(f"   ✅ RecBole directory found")
    # Check if fixes are applied
    seq_dataset_file = os.path.join(recbole_path, "data/dataset/sequential_dataset.py")
    if os.path.exists(seq_dataset_file):
        with open(seq_dataset_file, 'r') as f:
            content = f.read()
            if 'dtype=object' in content:
                print(f"   ✅ NumPy ragged array fix applied")
            else:
                print(f"   ⚠️  NumPy ragged array fix NOT applied")
            
            if 'dtype=bool' in content:
                print(f"   ✅ NumPy bool fix applied")
            else:
                print(f"   ⚠️  NumPy bool fix NOT applied")
else:
    print(f"   ❌ RecBole directory not found")

# Summary
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

if cuda_available:
    print("✅ Your environment is ready! GPU will be used for training.")
    print("   Estimated training time (50 epochs): ~30-45 minutes")
else:
    print("⚠️  Your environment is ready, but will use CPU.")
    print("   Estimated training time (50 epochs): ~4-6 hours")
    print("\n   To enable GPU:")
    print("   - On Kaggle: Settings → Accelerator → GPU")
    print("   - On Colab: Runtime → Change runtime type → GPU")
    print("   - On local: Install CUDA and GPU-enabled PyTorch")

print("\n" + "=" * 70)
print("Ready to run:")
print("  bash duorec.sh")
print("=" * 70)
