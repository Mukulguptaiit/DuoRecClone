# GPU/CPU Configuration Guide

## Why is it Running on CPU?

The code automatically detects whether GPU is available using this logic (from `configurator.py`):

```python
def _init_device(self):
    use_gpu = self.final_config_dict['use_gpu']
    if use_gpu:
        os.environ["CUDA_VISIBLE_DEVICES"] = str(self.final_config_dict['gpu_id'])
    self.final_config_dict['device'] = torch.device("cuda" if torch.cuda.is_available() and use_gpu else "cpu")
```

**It runs on CPU if:**
1. `torch.cuda.is_available()` returns `False` (no GPU detected), OR
2. `use_gpu` is set to `False` in config

## Check GPU Availability

Run this to check if PyTorch can see your GPU:

```bash
python -c "import torch; print('CUDA available:', torch.cuda.is_available()); print('CUDA version:', torch.version.cuda); print('GPU count:', torch.cuda.device_count()); print('GPU name:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'No GPU')"
```

### Expected Output:

**With GPU:**
```
CUDA available: True
CUDA version: 11.8
GPU count: 1
GPU name: Tesla T4
```

**Without GPU (like on Kaggle CPU kernel):**
```
CUDA available: False
CUDA version: None
GPU count: 0
GPU name: No GPU
```

## Configuration Settings

### Default Settings (from `overall.yaml`):
```yaml
gpu_id: 0          # Which GPU to use (0, 1, 2, etc.)
use_gpu: True      # Whether to try using GPU
```

### Your Settings (from `seq.yaml`):
Currently inherits defaults - `use_gpu: True`

## Solutions to Enable GPU

### Solution 1: Verify GPU-enabled PyTorch is Installed

If you're on a system with NVIDIA GPU, you need PyTorch compiled with CUDA support.

**Check your PyTorch installation:**
```bash
python -c "import torch; print(torch.__version__); print('Built with CUDA:', torch.cuda.is_available())"
```

**If it shows CUDA available: False, reinstall PyTorch with CUDA:**

For CUDA 11.8:
```bash
pip uninstall torch
pip install torch --index-url https://download.pytorch.org/whl/cu118
```

For CUDA 12.1:
```bash
pip uninstall torch
pip install torch --index-url https://download.pytorch.org/whl/cu121
```

For CPU only (if no GPU):
```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

### Solution 2: Enable GPU in Kaggle/Colab

**On Kaggle:**
1. Click **"Settings"** on the right sidebar
2. Under **"Accelerator"**, select **"GPU T4 x2"** or **"GPU P100"**
3. Click **"Save"**
4. The notebook will restart with GPU enabled

**On Google Colab:**
1. Go to **Runtime** → **Change runtime type**
2. Select **"GPU"** under Hardware accelerator
3. Click **"Save"**

### Solution 3: Force CPU Mode (if no GPU available)

If you don't have a GPU, you can explicitly set CPU mode to avoid confusion:

**Add to `seq.yaml`:**
```yaml
use_gpu: False
```

**Or via command line:**
```bash
python run_seq.py --dataset='ml-1m' --model='DuoRec' --use_gpu=False
```

### Solution 4: Specify GPU ID

If you have multiple GPUs, specify which one to use:

**In `seq.yaml`:**
```yaml
gpu_id: 0          # Use first GPU
# gpu_id: 1        # Use second GPU
```

**Or via command line:**
```bash
python run_seq.py --dataset='ml-1m' --model='DuoRec' --gpu_id=0
```

## Verify GPU Usage During Training

When GPU is properly configured, you should see in the logs:

```
INFO  device: cuda
INFO  CUDA is available: True
```

During training, you can monitor GPU usage:

**On Linux/WSL:**
```bash
# In another terminal
watch -n 1 nvidia-smi
```

**On Kaggle:**
```bash
# In a code cell
!nvidia-smi
```

## Performance Comparison

| Setup | Approximate Time (50 epochs, ml-1m) |
|-------|-------------------------------------|
| CPU (8 cores) | ~4-6 hours |
| GPU (Tesla T4) | ~30-45 minutes |
| GPU (Tesla P100) | ~20-30 minutes |
| GPU (RTX 3090) | ~15-20 minutes |

## Troubleshooting

### Issue: "CUDA out of memory"

**Solution 1: Reduce batch size**
```yaml
train_batch_size: 128    # Reduce from 256
eval_batch_size: 128     # Reduce from 256
```

**Solution 2: Reduce sequence length**
```yaml
MAX_ITEM_LIST_LENGTH: 30  # Reduce from 50
```

### Issue: "RuntimeError: No CUDA GPUs are available"

**Causes:**
1. No GPU on the system
2. GPU drivers not installed
3. PyTorch not compiled with CUDA
4. Wrong CUDA version

**Solution:**
Check NVIDIA driver and CUDA:
```bash
nvidia-smi                    # Check if GPU is detected
nvcc --version                # Check CUDA version
```

Then install matching PyTorch version.

### Issue: PyTorch version mismatch with CUDA

**Check versions:**
```bash
nvcc --version                          # Shows CUDA version
python -c "import torch; print(torch.version.cuda)"  # Shows PyTorch CUDA version
```

**They should match** (e.g., both 11.8 or both 12.1)

If they don't match, reinstall PyTorch with correct CUDA version.

## Quick Start Commands

### With GPU (default):
```bash
bash duorec.sh
```

### Force CPU:
```bash
python run_seq.py --dataset='ml-1m' --model='DuoRec' --use_gpu=False
```

### Specify GPU:
```bash
python run_seq.py --dataset='ml-1m' --model='DuoRec' --gpu_id=0
```

### Check Device During Run:
```bash
python run_seq.py --dataset='ml-1m' --model='DuoRec' --epochs=1 | grep -i "device\|cuda\|gpu"
```

## Summary

The code **automatically uses GPU if available**. If it's running on CPU:

1. ✅ **Check**: `python -c "import torch; print(torch.cuda.is_available())"`
2. ✅ **If False**: Install GPU-enabled PyTorch
3. ✅ **On Kaggle**: Enable GPU accelerator in settings
4. ✅ **If no GPU**: Set `use_gpu: False` to avoid confusion

The training will work on both CPU and GPU - GPU is just much faster! 🚀
