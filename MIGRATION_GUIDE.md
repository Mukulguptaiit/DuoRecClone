# Migration Guide for Updated DuoRec

## Overview
This repository has been updated to support modern Python, NumPy, and Pandas versions. The changes fix compatibility issues with NumPy 1.20+ and Pandas 2.0+.

## What Changed?

### 1. NumPy Type Aliases (Breaking in NumPy 1.24+)
- Replaced deprecated `np.bool`, `np.float`, `np.long` with `bool`, `np.float64`, `np.int64`
- No functional changes - only modernized type declarations

### 2. Pandas Operations (Warnings in Pandas 2.0, Breaking in Pandas 3.0)
- Fixed chained assignment with `inplace=True` 
- Changed from `df[col].method(inplace=True)` to proper assignment syntax
- No functional changes - same behavior with modern syntax

## Upgrading Your Environment

### Option 1: Create New Environment (Recommended)

```bash
# Create new conda environment
conda create -n duorec python=3.9
conda activate duorec

# Install updated requirements
pip install -r requirements.txt
```

### Option 2: Update Existing Environment

```bash
# Activate your existing environment
conda activate your_env_name

# Update numpy if needed (minimum version 1.20.0)
pip install --upgrade numpy>=1.20.0

# Ensure pandas is compatible
pip install --upgrade pandas>=1.0.5

# Install other requirements
pip install -r requirements.txt
```

## Running DuoRec

No changes to the usage! Run exactly as before:

```bash
# Run with default settings
bash duorec.sh

# Or directly with Python
python run_seq.py --dataset='ml-1m' --model='DuoRec' --train_batch_size=256
```

## Compatibility Matrix

| Package | Minimum Version | Tested With |
|---------|----------------|-------------|
| Python  | 3.8            | 3.9, 3.10, 3.11 |
| NumPy   | 1.20.0         | 1.24+, 1.26+ |
| Pandas  | 1.0.5          | 2.0+, 2.1+ |
| PyTorch | 1.7.0          | 1.7+, 2.0+ |
| SciPy   | 1.6.0          | 1.6+, 1.11+ |

## What Errors Are Fixed?

### Before (Old Code):
```
AttributeError: module 'numpy' has no attribute 'bool'.
`np.bool` was a deprecated alias for the builtin `bool`.
```

```
FutureWarning: A value is trying to be set on a copy of a DataFrame 
or Series through chained assignment using an inplace method.
```

### After (Updated Code):
✅ No errors or warnings!

## Troubleshooting

### Issue: Still getting numpy errors
**Solution**: Make sure you have NumPy 1.20 or higher:
```bash
pip install --upgrade numpy>=1.20.0
```

### Issue: Pandas warnings still appearing
**Solution**: The fixes in this repo handle all chained assignment issues. If you still see warnings, ensure you're running the updated code.

### Issue: CUDA/PyTorch compatibility
**Solution**: Install PyTorch according to your CUDA version:
```bash
# For CUDA 11.8
pip install torch --index-url https://download.pytorch.org/whl/cu118

# For CPU only
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

## Verification

To verify everything works, run a quick test:

```bash
# Test on ml-1m dataset
python run_seq.py --dataset='ml-1m' --model='DuoRec' --epochs=1

# Should complete without numpy/pandas errors
```

## Support

If you encounter any issues:
1. Check that all dependencies are at minimum required versions
2. Try creating a fresh conda/virtual environment
3. Ensure you're using the updated code (check VERSION_COMPATIBILITY_FIXES.md)

## Original Citation

```bibtex
@article{DuoRec,
  author    = {Ruihong Qiu and
               Zi Huang and
               Hongzhi Yin and
               Zijian Wang},
  title     = {Contrastive Learning for Representation Degeneration Problem in Sequential Recommendation},
  journal   = {CoRR},
  volume    = {abs/2110.05730},
  year      = {2021},
}
```
