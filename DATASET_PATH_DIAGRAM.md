# Dataset Path Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    RUNNING: bash duorec.sh                      │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  duorec.sh passes arguments to run_seq.py:                      │
│  --dataset='ml-1m'                                              │
│  --model='DuoRec'                                               │
│  --config_files='seq.yaml'                                      │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  run_seq.py calls run_recbole() with:                           │
│  • dataset = 'ml-1m'                                            │
│  • config_file_list = ['seq.yaml']                              │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  Config class reads seq.yaml:                                   │
│  • data_path: "./dataset/"                                      │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  configurator.py combines paths:                                │
│  • base_path = "./dataset/"                                     │
│  • dataset_name = "ml-1m"                                       │
│  • final_path = os.path.join("./dataset/", "ml-1m")            │
│                = "./dataset/ml-1m/"                             │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  Resolves to absolute path:                                     │
│  /Users/mukulgupta/Downloads/DuoRe/dataset/ml-1m/               │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  Looks for files with pattern {dataset}.{suffix}:               │
│  ✅ ml-1m.inter  (interaction data)                             │
│  ✅ ml-1m.item   (item features)                                │
│  ✅ ml-1m.user   (user features)                                │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  ✅ SUCCESS! Dataset loaded and training begins                 │
└─────────────────────────────────────────────────────────────────┘
```

## File Structure

```
/Users/mukulgupta/Downloads/DuoRe/
│
├── duorec.sh                    ← Run this!
├── run_seq.py                   ← Entry point
├── seq.yaml                     ← Config (data_path: "./dataset/")
│
├── dataset/                     ← Dataset root (from config)
│   └── ml-1m/                   ← Dataset folder (from --dataset arg)
│       ├── ml-1m.inter  ✅      ← Required: interactions
│       ├── ml-1m.item   ✅      ← Required: item features
│       └── ml-1m.user   ✅      ← Required: user features
│
├── recbole/                     ← RecBole library
│   ├── config/
│   │   └── configurator.py      ← Path resolution logic
│   └── ...
│
└── log/                         ← Training logs (created automatically)
    └── DuoRec/
        └── ml-1m/
            └── ...
```

## Path Resolution Logic (from configurator.py)

```python
# For any dataset EXCEPT 'ml-100k':
if self.dataset == 'ml-100k':
    # Special case: uses dataset_example/ml-100k
    pass
else:
    # For ml-1m and all other datasets:
    # Combines config data_path with dataset name
    self.final_config_dict['data_path'] = os.path.join(
        self.final_config_dict['data_path'],  # "./dataset/" from seq.yaml
        self.dataset                           # "ml-1m" from command line
    )
    # Result: "./dataset/ml-1m/"
```

## Why Your Setup Works

| Component | Value | Status |
|-----------|-------|--------|
| Config path | `./dataset/` | ✅ Correct |
| Dataset arg | `ml-1m` | ✅ Correct |
| Combined path | `./dataset/ml-1m/` | ✅ Correct |
| Absolute path | `/Users/mukulgupta/Downloads/DuoRe/dataset/ml-1m/` | ✅ Exists |
| Required files | `ml-1m.inter`, `ml-1m.item`, `ml-1m.user` | ✅ All present |

## What Would Break It?

❌ **Wrong**: Running from different directory
```bash
cd /Users/mukulgupta/
bash DuoRe/duorec.sh  # Won't find ./dataset/
```

❌ **Wrong**: Missing dataset files
```bash
/Users/mukulgupta/Downloads/DuoRe/dataset/ml-1m/
└── (empty)  # No .inter, .item, .user files
```

❌ **Wrong**: Wrong file names
```bash
/Users/mukulgupta/Downloads/DuoRe/dataset/ml-1m/
├── movielens.inter  # Should be ml-1m.inter
├── movielens.item   # Should be ml-1m.item
└── movielens.user   # Should be ml-1m.user
```

## Your Setup (Correct!)

✅ **Correct**: Running from project root
```bash
cd /Users/mukulgupta/Downloads/DuoRe
bash duorec.sh  # ✅ Finds ./dataset/
```

✅ **Correct**: All required files present
```bash
/Users/mukulgupta/Downloads/DuoRe/dataset/ml-1m/
├── ml-1m.inter  ✅
├── ml-1m.item   ✅
├── ml-1m.user   ✅
└── README.md    (optional)
```

✅ **Correct**: File names match dataset name
```bash
Dataset name: ml-1m
Files: ml-1m.inter, ml-1m.item, ml-1m.user  ✅
```

---

## Conclusion

🎉 **Everything is already set up correctly!**

Just run: `bash duorec.sh`

No need to move any files! 🚀
