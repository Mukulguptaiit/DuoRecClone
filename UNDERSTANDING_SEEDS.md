# Understanding Multiple Seeds and Quick Estimates

## What Multiple Seeds Actually Do

### The Randomness in Neural Networks

```python
# What changes with different seeds:
torch.manual_seed(2020)  # Seed 1
model = DuoRec()         
# - Random weight initialization
# - Random dropout masks  
# - Random batch shuffling
# Result: Recall@10 = 0.4520

torch.manual_seed(2021)  # Seed 2  
model = DuoRec()         
# - DIFFERENT random weights
# - DIFFERENT dropout masks
# - DIFFERENT batch order
# Result: Recall@10 = 0.4535
```

### Why It Matters

**Without multiple seeds:**
```
Your paper: "Our model achieves Recall@10 = 0.4535"
Reviewer: "Is this just lucky initialization?"
Reviewer: "I got 0.4510 when I tried to reproduce"
```

**With multiple seeds:**
```
Your paper: "Our model achieves Recall@10 = 0.4522 ±0.0010"
Reviewer: "Good! The result is stable and reproducible"
```

## Two Strategies: Full vs Quick Estimate

### Strategy 1: Full Training (For Final Results)

```bash
# Run each seed to convergence (50 epochs)
qsub run_multiseed.pbs
```

**Pros:**
- ✅ Best possible performance
- ✅ Publishable results
- ✅ Real convergence

**Cons:**
- ❌ Takes ~10-15 hours (5 seeds × 2-3 hours each)
- ❌ Uses lots of compute time

**Use when:**
- Final paper results
- Comparing to baselines
- Publishing/submitting

---

### Strategy 2: Quick Estimate (For Development)

```bash
# Run each seed with fewer epochs (10 instead of 50)
qsub run_quick_estimate.pbs
```

**Pros:**
- ✅ Much faster (~2-3 hours total)
- ✅ Good enough for rough estimates
- ✅ Tells you if std is reasonable

**Cons:**
- ❌ Lower absolute performance (not converged)
- ❌ Can't use for final paper

**Use when:**
- Testing hyperparameters
- Comparing different model variants
- Sanity checking before full run

---

## Comparison Example

### Full Training (50 epochs):
```
Time per seed: 2-3 hours
Total time: 10-15 hours

Results:
  recall@10  : 0.4522 ± 0.0010  (converged)
  ndcg@10    : 0.3456 ± 0.0012  (converged)
```

### Quick Estimate (10 epochs):
```
Time per seed: 20-30 minutes
Total time: 2-3 hours

Results:
  recall@10  : 0.4200 ± 0.0015  (not converged, but std is similar!)
  ndcg@10    : 0.3100 ± 0.0018  (not converged, but std is similar!)
```

**Key insight:** The **standard deviation** is often **similar** between quick and full runs!
- If quick estimate shows std=0.0015, full training will likely be ~0.0010-0.0020
- If quick estimate shows std=0.0500 (high variance), full training won't fix it

---

## Recommended Workflow

### Phase 1: Development (Use Quick Estimates)

```bash
# Test different hyperparameters quickly
# Dropout 0.1
qsub run_quick_estimate.pbs

# Dropout 0.3  
# (modify script)
qsub run_quick_estimate.pbs

# Compare: Which has better mean AND lower std?
```

### Phase 2: Final Evaluation (Use Full Training)

```bash
# Once you found best hyperparameters, do full training
qsub run_multiseed.pbs

# Use these results in your paper
```

---

## How Many Epochs Are Enough?

### For Quick Estimate:
```yaml
epochs: 10              # Very quick, rough estimate
stopping_step: 5        # Stop early if no improvement
```
**Time:** ~20-30 min per seed

### For Development:
```yaml
epochs: 20              # Reasonable performance
stopping_step: 10       # Standard early stopping
```
**Time:** ~45-60 min per seed

### For Final Results:
```yaml
epochs: 50              # Full convergence
stopping_step: 10       # Conservative stopping
```
**Time:** ~2-3 hours per seed

---

## Real Example from Research

### From DuoRec Paper (Qiu et al.):

> "We report the average results of 5 runs with different random seeds."

Translation: They ran their model **5 times**, each with:
- Different random initialization
- Different dropout patterns
- Same hyperparameters

Then reported: **HR@10: 0.0743 (±0.0003)**

This means:
- Run 1: 0.0741
- Run 2: 0.0745
- Run 3: 0.0743
- Run 4: 0.0742
- Run 5: 0.0744
- Mean: 0.0743, Std: 0.0003

**Low std = Stable model! 🎉**

---

## Practical Tips

### 1. Start with 3 seeds for quick testing
```bash
SEEDS=(2020 2021 2022)  # Just 3
```

### 2. Use 5 seeds for paper (standard)
```bash
SEEDS=(2020 2021 2022 2023 2024)  # 5 is standard
```

### 3. Use quick estimates during development
```bash
# Try many hyperparameters quickly
for DROPOUT in 0.1 0.3 0.5; do
    # Run with 10 epochs, 3 seeds
    # Takes ~1 hour instead of ~10 hours
done
```

### 4. Do full runs only for final results
```bash
# Found best hyperparameters? Now do full run
qsub run_multiseed.pbs  # 50 epochs, 5 seeds
```

---

## What if std is too high?

```
recall@10: 0.4522 ± 0.0500  ← High variance! 😟
```

**Possible reasons:**
1. **Model is unstable** - Try lower learning rate
2. **Dataset is small** - Normal for small datasets
3. **Too much randomness** - Reduce dropout
4. **Not converged** - Train longer

**Solutions:**
```bash
# Try these one at a time:
--learning_rate=0.0005   # Lower LR (was 0.001)
--epochs=100             # Train longer
--hidden_dropout_prob=0.1  # Less dropout
```

Then re-run quick estimate to see if std improved.

---

## Summary

| Aspect | Quick Estimate | Full Training |
|--------|---------------|---------------|
| **Epochs** | 10-20 | 50+ |
| **Time** | 2-3 hours | 10-15 hours |
| **Use Case** | Development, testing | Final paper results |
| **Accuracy** | Lower (not converged) | Higher (converged) |
| **Std Estimate** | Good indicator | Definitive |

**Rule of thumb:** 
- Use quick estimates to narrow down choices
- Use full training for final comparison
- Always report full training results in papers
