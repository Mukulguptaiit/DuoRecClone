# Quick Start Guide - DuoRec (Updated)

## ✅ Pre-flight Check

### 1. Dataset Location - VERIFIED ✓
Your dataset is correctly placed at:
```
/Users/mukulgupta/Downloads/DuoRe/dataset/ml-1m/
├── ml-1m.inter
├── ml-1m.item
├── ml-1m.user
└── README.md
```

**No need to move anything!** The system will automatically find it.

### 2. Shell Script - FIXED ✓
Fixed a syntax error in `duorec.sh`:
- **Before**: `lmd=0.1` (missing `--`)
- **After**: `--lmd=0.1` ✓

### 3. Code Compatibility - UPDATED ✓
All NumPy and Pandas compatibility issues have been fixed.

## 🚀 How to Run

### Option 1: Using the Shell Script (Recommended)
```bash
cd /Users/mukulgupta/Downloads/DuoRe
bash duorec.sh
```

This will run with these parameters:
- Dataset: `ml-1m`
- Model: `DuoRec`
- Batch size: `256`
- Lambda: `0.1`
- Lambda semantic: `0.1`
- Contrast: `us_x`
- Similarity: `dot`
- Tau: `1`

### Option 2: Direct Python Command
```bash
cd /Users/mukulgupta/Downloads/DuoRe
python run_seq.py --dataset='ml-1m' --train_batch_size=256 --lmd=0.1 --lmd_sem=0.1 --model='DuoRec' --contrast='us_x' --sim='dot' --tau=1
```

### Option 3: Quick Test Run (1 epoch)
```bash
cd /Users/mukulgupta/Downloads/DuoRe
python run_seq.py --dataset='ml-1m' --model='DuoRec' --epochs=1
```

## 📊 What to Expect

### Successful Output Should Show:
```
INFO  Loading [ml-1m] from ./dataset/ml-1m/
INFO  ml-1m.inter loaded successfully
INFO  ml-1m.item loaded successfully  
INFO  ml-1m.user loaded successfully
INFO  [ml-1m] dataset filtering completed
INFO  Train: 575281 interactions, Valid: 6040 interactions, Test: 6040 interactions
INFO  DuoRec model initialized
INFO  Training started...
```

### Training Progress:
```
Train epoch 1:
  0%|          | 0/2247 [00:00<?, ?it/s]
 10%|█         | 225/2247 [00:10<01:30, 22.35it/s]
...
```

### Final Results (after 50 epochs):
```
INFO  best valid result: {'recall@5': 0.xxxx, 'recall@10': 0.xxxx, ...}
INFO  test result: {'recall@5': 0.xxxx, 'recall@10': 0.xxxx, ...}
INFO  Training finished!
```

## 📁 Output Files

Results will be saved to:
```
/Users/mukulgupta/Downloads/DuoRe/log/
└── DuoRec/
    └── ml-1m/
        ├── DuoRec-ml-1m-{timestamp}.log
        └── DuoRec-ml-1m-{timestamp}.pth (model checkpoint)
```

## 🔍 Dataset Path Resolution

Here's how the system finds your dataset:

1. **Config file** (`seq.yaml`): `data_path: "./dataset/"`
2. **Command line**: `--dataset='ml-1m'`
3. **Final path**: `./dataset/ml-1m/`
4. **Absolute path**: `/Users/mukulgupta/Downloads/DuoRe/dataset/ml-1m/`

The system automatically:
- Joins the `data_path` with the dataset name
- Looks for files matching the pattern: `{dataset}.inter`, `{dataset}.item`, `{dataset}.user`
- Loads: `ml-1m.inter`, `ml-1m.item`, `ml-1m.user` ✓

## 🛠️ Troubleshooting

### Issue: "Dataset not found"
**Cause**: Running from wrong directory
**Solution**: 
```bash
cd /Users/mukulgupta/Downloads/DuoRe
bash duorec.sh
```

### Issue: "Module not found" errors
**Cause**: Dependencies not installed
**Solution**:
```bash
pip install -r requirements.txt
```

### Issue: NumPy/Pandas errors
**Cause**: Old package versions
**Solution**: 
```bash
pip install --upgrade numpy>=1.20.0 pandas>=2.0.0
```

### Issue: CUDA/GPU errors
**Solution**: Install appropriate PyTorch version:
```bash
# For CUDA 11.8
pip install torch --index-url https://download.pytorch.org/whl/cu118

# For CPU only
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

## 📈 Running Different Models

### Run CL4SRec instead of DuoRec
```bash
python run_seq.py --dataset='ml-1m' --model='CL4SRec' --train_batch_size=256
```

### Try with Amazon Beauty dataset
```bash
python run_seq.py --dataset='Amazon_All_Beauty' --model='DuoRec' --train_batch_size=256
```

## ⚙️ Key Parameters

From `seq.yaml`:
- `epochs: 50` - Number of training epochs
- `train_batch_size: 256` - Batch size for training
- `learning_rate: 0.001` - Learning rate
- `MAX_ITEM_LIST_LENGTH: 50` - Maximum sequence length
- `eval_step: 1` - Evaluate every N epochs
- `stopping_step: 10` - Early stopping patience

You can override any parameter via command line:
```bash
python run_seq.py --dataset='ml-1m' --model='DuoRec' --epochs=100 --learning_rate=0.0001
```

## 🎯 Summary

✅ **Dataset location**: Correct - no changes needed
✅ **Shell script**: Fixed - ready to run
✅ **Code compatibility**: Fixed - all updated
✅ **Configuration**: Proper - paths resolve correctly

**You're all set! Just run:** `bash duorec.sh` 🚀

---

For more details, see:
- `DATASET_PATH_VERIFICATION.md` - Dataset path details
- `VERSION_COMPATIBILITY_FIXES.md` - Code changes log
- `MIGRATION_GUIDE.md` - Upgrade guide
