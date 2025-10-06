#!/usr/bin/env python
"""
Calculate mean and standard deviation of metrics across multiple runs
"""
import re
import os
import numpy as np
from collections import defaultdict

def parse_log_file(log_file):
    """Parse a log file and extract test metrics"""
    metrics = {}
    
    with open(log_file, 'r') as f:
        content = f.read()
        
        # Look for test results - pattern like "Recall@10 : 0.1234"
        # Adjust regex pattern based on actual RecBole output format
        patterns = [
            r'(\w+@\d+)\s*:\s*([\d.]+)',  # Format: "Recall@10 : 0.1234"
            r'(\w+@\d+)\s*=\s*([\d.]+)',  # Format: "Recall@10 = 0.1234"
            r'test result:\s*{([^}]+)}',   # Format: test result: {'Recall@10': 0.1234}
        ]
        
        # Try to find test results section
        for pattern in patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                if len(match.groups()) == 2:
                    metric_name = match.group(1)
                    metric_value = float(match.group(2))
                    metrics[metric_name] = metric_value
    
    return metrics

def calculate_statistics(results_dir='./results_multiple_seeds'):
    """Calculate mean and std across all seed runs"""
    
    # Find all log files
    log_files = [f for f in os.listdir(results_dir) if f.endswith('.log')]
    
    if not log_files:
        print(f"No log files found in {results_dir}")
        return
    
    print(f"Found {len(log_files)} log files")
    print("=" * 60)
    
    # Collect metrics from all runs
    all_metrics = defaultdict(list)
    
    for log_file in sorted(log_files):
        log_path = os.path.join(results_dir, log_file)
        seed = log_file.replace('seed_', '').replace('.log', '')
        
        print(f"\nProcessing: {log_file}")
        metrics = parse_log_file(log_path)
        
        if metrics:
            print(f"  Seed {seed} metrics:")
            for metric, value in sorted(metrics.items()):
                print(f"    {metric}: {value:.4f}")
                all_metrics[metric].append(value)
        else:
            print(f"  Warning: No metrics found in {log_file}")
    
    # Calculate statistics
    print("\n" + "=" * 60)
    print("FINAL RESULTS (Mean ± Std)")
    print("=" * 60)
    
    results_table = []
    
    for metric in sorted(all_metrics.keys()):
        values = np.array(all_metrics[metric])
        mean = np.mean(values)
        std = np.std(values, ddof=1)  # Sample std deviation
        
        results_table.append({
            'metric': metric,
            'mean': mean,
            'std': std,
            'n_runs': len(values)
        })
        
        print(f"{metric:15s}: {mean:.4f} ± {std:.4f}  (n={len(values)})")
    
    # Save to file
    output_file = os.path.join(results_dir, 'statistics_summary.txt')
    with open(output_file, 'w') as f:
        f.write("DuoRec Results - Multiple Seeds Statistics\n")
        f.write("=" * 60 + "\n\n")
        
        for result in results_table:
            f.write(f"{result['metric']:15s}: {result['mean']:.4f} ± {result['std']:.4f}  (n={result['n_runs']})\n")
        
        f.write("\n" + "=" * 60 + "\n")
        f.write("Individual Run Values:\n\n")
        
        for metric in sorted(all_metrics.keys()):
            f.write(f"{metric}: {all_metrics[metric]}\n")
    
    print(f"\nResults saved to: {output_file}")
    
    return results_table

if __name__ == '__main__':
    import sys
    
    # Allow custom results directory
    results_dir = sys.argv[1] if len(sys.argv) > 1 else './results_multiple_seeds'
    
    if not os.path.exists(results_dir):
        print(f"Error: Directory {results_dir} does not exist")
        print("Please run 'bash run_multiple_seeds.sh' first")
        sys.exit(1)
    
    calculate_statistics(results_dir)
