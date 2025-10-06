# 🎯 Why Is It Running on CPU? - Quick Answer

## TL;DR

**The code automatically uses GPU if available.** It's running on CPU because:

1. ❌ PyTorch cannot detect a GPU on your system, OR
2. ❌ You're running on a CPU-only kernel (like Kaggle CPU), OR
3. ❌ PyTorch wasn't installed with CUDA support

## 🔍 Quick Check

Run this command:

```bash
python -c "import torch; print('GPU Available:', torch.cuda.is_available())"
```

**Result:**
- `GPU Available: True` → GPU will be used ✅
- `GPU Available: False` → CPU will be used (need to fix) ⚠️

## 🚀 Quick Fixes

### On Kaggle:
1. Click **Settings** (right sidebar)
2. Change **Accelerator** from "None" to **"GPU T4 x2"**
3. Save and restart

### On Google Colab:
1. **Runtime** → **Change runtime type**
2. Select **GPU** 
3. Save

### On Local Machine with NVIDIA GPU:
```bash
# Install GPU-enabled PyTorch (for CUDA 11.8)
pip uninstall torch
pip install torch --index-url https://download.pytorch.org/whl/cu118
```

### If You Don't Have a GPU:
```bash
# Just accept CPU mode - it will work, just slower
python run_seq.py --dataset='ml-1m' --model='DuoRec' --use_gpu=False
```

## 📊 Speed Comparison

| Device | Time (50 epochs) |
|--------|------------------|
| CPU | ~4-6 hours ⏰ |
| GPU (T4) | ~30-45 minutes ⚡ |
| GPU (P100) | ~20-30 minutes ⚡⚡ |

## 🔧 Diagnostic Tool

Run this to check your setup:

```bash
python check_environment.py
```

This will show:
- ✅ Python version
- ✅ PyTorch version
- ✅ GPU availability
- ✅ All dependencies
- ✅ Dataset location
- ✅ Applied fixes

## 📖 Detailed Guide

For complete GPU configuration instructions, see:
- **GPU_CONFIGURATION_GUIDE.md** - Full GPU setup guide

## ⚙️ How It Works

The code checks GPU in `recbole/config/configurator.py`:

```python
# Automatically selects device
device = torch.device("cuda" if torch.cuda.is_available() and use_gpu else "cpu")
```

**Config settings (seq.yaml):**
```yaml
use_gpu: True      # Try to use GPU (default: True)
gpu_id: 0          # Which GPU to use (default: 0)
```

**You don't need to change anything** - it auto-detects!

## 🎉 Summary

1. **Check GPU**: `python -c "import torch; print(torch.cuda.is_available())"`
2. **If False on Kaggle**: Enable GPU in Settings
3. **If False locally**: Install GPU-enabled PyTorch
4. **If no GPU**: Training still works on CPU (just slower)

The code is already configured correctly - you just need to ensure GPU is available! 🚀

---

**Quick Commands:**

```bash
# Check if GPU is available
python check_environment.py

# Run with auto-detection (uses GPU if available)
bash duorec.sh

# Force CPU mode
python run_seq.py --dataset='ml-1m' --model='DuoRec' --use_gpu=False
```
