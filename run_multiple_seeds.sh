#!/bin/bash
# Run DuoRec with multiple seeds by modifying seq.yaml directly

# Array of random seeds (5-6 different seeds for statistical significance)
SEEDS=(2020 2021 2022 2023 2024 2025)

# Output directory for results
RESULTS_DIR="./results_multiple_seeds"
mkdir -p $RESULTS_DIR

# Backup original seq.yaml
cp seq.yaml seq.yaml.backup

echo "Running DuoRec with multiple seeds..."
echo "====================================="

# Run experiment with each seed
for SEED in "${SEEDS[@]}"; do
    echo ""
    echo "Running with seed: $SEED"
    echo "-------------------"
    
    # Modify line 25 of seq.yaml to change seed
    sed -i.tmp "25s/.*/seed: ${SEED}/" seq.yaml
    rm seq.yaml.tmp 2>/dev/null  # Clean up sed backup file
    
    # Run with your full command (capture both stdout and stderr)
    python run_seq.py \
        --dataset='Amazon_Beauty' \
        --train_batch_size=256 \
        --lmd=0.1 \
        --lmd_sem=0.1 \
        --model='DuoRec' \
        --contrast='us_x' \
        --sim='dot' \
        --tau=1 \
        2>&1 | tee $RESULTS_DIR/seed_${SEED}.log
    
    echo "Completed seed: $SEED"
done

# Restore original seq.yaml
mv seq.yaml.backup seq.yaml

echo ""
echo "====================================="
echo "All runs completed!"
echo "Results saved in: $RESULTS_DIR"
echo ""
echo "To calculate statistics, run:"
echo "python calculate_statistics.py"
