#!/bin/bash
# Quick estimate: Run multiple seeds with FEWER epochs
# This gives you a rough estimate of mean ± std much faster

SEEDS=(2020 2021 2022 2023 2024)
RESULTS_DIR="./results_quick_estimate"
mkdir -p $RESULTS_DIR

echo "Quick Statistical Estimate (Fewer Epochs)"
echo "=========================================="

for SEED in "${SEEDS[@]}"; do
    echo ""
    echo "Running with seed: $SEED (10 epochs only)"
    echo "-------------------"
    
    # Run with FEWER epochs for quick estimate
    python run_seq.py \
        --dataset='ml-1m' \
        --train_batch_size=256 \
        --lmd=0.1 \
        --lmd_sem=0.1 \
        --model='DuoRec' \
        --contrast='us_x' \
        --sim='dot' \
        --tau=1 \
        --seed=$SEED \
        --epochs=10 \
        --stopping_step=5 \
        | tee $RESULTS_DIR/seed_${SEED}.log
    
    echo "Completed seed: $SEED"
done

echo ""
echo "=========================================="
echo "Quick estimate completed!"
echo "Results saved in: $RESULTS_DIR"
echo ""
echo "Calculate statistics:"
python extract_metrics.py $RESULTS_DIR
