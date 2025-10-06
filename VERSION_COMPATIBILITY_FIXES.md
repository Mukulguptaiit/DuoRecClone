# Version Compatibility Fixes

This document summarizes all changes made to ensure compatibility with modern Python, NumPy, and Pandas versions.

## Date: October 4, 2025

## Issues Fixed

### 1. NumPy Ragged Array Creation
**Problem**: NumPy 1.19+ raises `ValueError` when creating arrays from sequences of different lengths without specifying `dtype=object`

**Error Message**:
```
ValueError: setting an array element with a sequence. The requested array has an 
inhomogeneous shape after 1 dimensions. The detected shape was (981491,) + inhomogeneous part.
```

**Solution**: Explicitly specify `dtype=object` when creating arrays with variable-length subarrays

#### Files Modified:
- `recbole/data/dataset/sequential_dataset.py`
  - Line 104: `np.array(same_target_index)` → `np.array(same_target_index, dtype=object)`

### 2. NumPy Deprecated Type Aliases
**Problem**: NumPy 1.20+ deprecated type aliases like `np.bool`, `np.int`, `np.float`, `np.long`

**Solution**: Replaced all deprecated aliases with their proper equivalents:
- `np.bool` → `bool` (Python builtin)
- `np.float` → `np.float64`
- `np.long` → `np.int64`

#### Files Modified:
- `recbole/data/dataset/sequential_dataset.py`
  - Line 88: `dtype=np.bool` → `dtype=bool`
  - Line 125: `dtype=np.bool` → `dtype=bool`

- `recbole/data/dataset/dataset.py`
  - Line 502: `dtype=np.float` → `dtype=np.float64`

- `recbole/evaluator/metrics.py`
  - Line 58: `dtype=np.float` → `dtype=np.float64`
  - Line 84: `.astype(np.float)` → `.astype(np.float64)`
  - Line 86: `dtype=np.float` → `dtype=np.float64`
  - Line 135: `dtype=np.float` → `dtype=np.float64`
  - Line 141: `dtype=np.float` → `dtype=np.float64`
  - Line 194: `dtype=np.bool` → `dtype=bool`

- `recbole/model/abstract_recommender.py`
  - Line 221: `dtype=np.long` → `dtype=np.int64`

- `recbole/model/layers.py`
  - Line 596: `dtype=np.long` → `dtype=np.int64`
  - Line 936: `dtype=np.long` → `dtype=np.int64`

### 2. Pandas Chained Assignment with `inplace=True`
**Problem**: Pandas 3.0 will remove support for chained assignment with inplace operations like `df[col].fillna(inplace=True)`

**Solution**: Changed chained assignments to proper assignment syntax:
- `feat[field].fillna(value, inplace=True)` → `feat.loc[:, field] = feat[field].fillna(value)`

#### Files Modified:
- `recbole/data/dataset/dataset.py`
  - Line 498: `feat[field].fillna(value=0, inplace=True)` → `feat.loc[:, field] = feat[field].fillna(value=0)`
  - Line 500: `feat[field].fillna(value=feat[field].mean(), inplace=True)` → `feat.loc[:, field] = feat[field].fillna(value=feat[field].mean())`
  - Line 402: `df[field].fillna(value='', inplace=True)` → `df.loc[:, field] = df[field].fillna(value='')`

## Compatibility

These changes ensure compatibility with:
- **Python**: 3.8+
- **NumPy**: 1.20+ (including 1.24+ which removed deprecated aliases)
- **Pandas**: 2.0+ (preparing for Pandas 3.0 changes)
- **PyTorch**: 1.7+ (as specified in requirements.txt)

## Testing

After applying these fixes, the code should run without:
1. `AttributeError: module 'numpy' has no attribute 'bool'`
2. `FutureWarning` messages about pandas chained assignment
3. Deprecation warnings from NumPy

## Notes

- All DataFrame-level `inplace=True` operations (like `df.drop(inplace=True)`, `df.sort_values(inplace=True)`) were left unchanged as they are not affected by the pandas warning
- Only chained assignment operations (accessing a column then calling inplace methods) were modified
- The fixes maintain backward compatibility with the original behavior while using the recommended modern syntax
