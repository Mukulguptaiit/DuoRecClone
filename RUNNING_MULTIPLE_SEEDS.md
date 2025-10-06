# How to Get Statistical Results (Mean ± Std) in DuoRec

## Why Multiple Seeds?

Research papers report results like: **HR@10: 0.4523 ±0.0030**

This requires running the model **multiple times** with different random seeds and calculating:
- **Mean**: Average performance across runs
- **Std**: Standard deviation (variance in results)

## Quick Start

### Option 1: Local/Interactive Run (for testing)

```bash
# Make script executable
chmod +x run_multiple_seeds.sh

# Run experiments with 5 different seeds
bash run_multiple_seeds.sh

# Calculate statistics
python extract_metrics.py
```

### Option 2: HPC Batch Job (recommended)

```bash
# Submit job to run all 5 seeds automatically
qsub run_multiseed.pbs

# Check progress
qstat -u tt1221351

# Once done, results will be in:
cat results_multiple_seeds/statistics_summary.txt
```

## What Gets Run

The script runs your model 5 times with seeds:
- 2020
- 2021
- 2022
- 2023
- 2024

Each run produces a separate log file in `results_multiple_seeds/`

## Expected Output

```
RESULTS: Mean ± Standard Deviation
======================================================================
recall@5            : 0.1234 ± 0.0012  (n=5)
recall@10           : 0.2345 ± 0.0023  (n=5)
ndcg@5              : 0.3456 ± 0.0034  (n=5)
ndcg@10             : 0.4567 ± 0.0045  (n=5)
...
```

## Customization

### Change Number of Seeds

Edit `run_multiple_seeds.sh` or `run_multiseed.pbs`:

```bash
# Use 3 seeds (faster)
SEEDS=(2020 2021 2022)

# Use 10 seeds (more robust, slower)
SEEDS=(2020 2021 2022 2023 2024 2025 2026 2027 2028 2029)
```

### Change Model Parameters

Edit the python command in the scripts:

```bash
python run_seq.py \
    --dataset='ml-1m' \
    --train_batch_size=256 \
    --lmd=0.1 \              # Change hyperparameters
    --lmd_sem=0.1 \
    --model='DuoRec' \
    --contrast='us_x' \
    --sim='dot' \
    --tau=1 \
    --seed=$SEED             # This varies across runs
```

## Time Estimates (on HPC Skylake node)

- **1 seed**: ~1-2 hours (depends on dataset size)
- **5 seeds**: ~5-10 hours
- **Walltime requested**: 24 hours (safe buffer)

## Tips

1. **Start with 3 seeds** for quick testing
2. **Use 5 seeds** for paper results (standard in research)
3. **Use 10 seeds** for final submission (more robust)
4. **Run on batch job** - don't use interactive session for this
5. **Check one run first** before running all seeds

## Troubleshooting

### No metrics found

The script looks for RecBole's test output. If metrics aren't found:

1. Check a log file manually:
   ```bash
   cat results_multiple_seeds/seed_2020.log
   ```

2. Look for lines like:
   - `test result: {'recall@10': 0.1234, ...}`
   - `recall@10 : 0.1234`

3. Adjust regex pattern in `extract_metrics.py` if needed

### Out of memory

Reduce batch size in the command:
```bash
--train_batch_size=128  # Instead of 256
```

### Job timeout

Increase walltime in PBS script:
```bash
#PBS -l walltime=48:00:00  # 48 hours instead of 24
```
