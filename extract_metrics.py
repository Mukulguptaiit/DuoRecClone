#!/usr/bin/env python
"""
Simple script to extract test metrics from RecBole log files
and calculate mean ± std across multiple runs
"""
import re
import os
import glob

def extract_metrics_from_log(log_file):
    """Extract test metrics from RecBole log file"""
    metrics = {}
    
    with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
        # RecBole typically outputs test results in this format:
        # test result: {'recall@10': 0.1234, 'ndcg@10': 0.5678, ...}
        # OR
        # recall@10 : 0.1234
        # ndcg@10   : 0.5678
        
        # Try to find dictionary format first
        dict_match = re.search(r'test result[:\s]+{([^}]+)}', content, re.IGNORECASE)
        if dict_match:
            dict_str = dict_match.group(1)
            # Parse the dictionary
            metric_pairs = re.findall(r"['\"]?(\w+@\d+)['\"]?\s*:\s*([\d.]+)", dict_str)
            for metric_name, value in metric_pairs:
                metrics[metric_name.lower()] = float(value)
        
        # Also try line-by-line format
        if not metrics:
            lines = content.split('\n')
            for line in lines:
                match = re.match(r'\s*(\w+@\d+)\s*[:=]\s*([\d.]+)', line)
                if match:
                    metric_name = match.group(1).lower()
                    value = float(match.group(2))
                    metrics[metric_name] = value
    
    return metrics

def calculate_stats(results_dir='./results_multiple_seeds'):
    """Calculate mean and std for all metrics"""
    
    # Find all seed log files
    log_pattern = os.path.join(results_dir, 'seed_*.log')
    log_files = glob.glob(log_pattern)
    
    if not log_files:
        print(f"No log files found matching: {log_pattern}")
        return
    
    log_files.sort()
    print(f"Found {len(log_files)} log files\n")
    
    # Collect all metrics
    all_runs = []
    
    for log_file in log_files:
        seed = os.path.basename(log_file).replace('seed_', '').replace('.log', '')
        metrics = extract_metrics_from_log(log_file)
        
        if metrics:
            all_runs.append({'seed': seed, 'metrics': metrics})
            print(f"Seed {seed}: {len(metrics)} metrics found")
    
    if not all_runs:
        print("No metrics found in any log file!")
        return
    
    # Organize by metric name
    metric_values = {}
    for run in all_runs:
        for metric, value in run['metrics'].items():
            if metric not in metric_values:
                metric_values[metric] = []
            metric_values[metric].append(value)
    
    # Calculate statistics
    print("\n" + "="*70)
    print("RESULTS: Mean ± Standard Deviation")
    print("="*70)
    
    results = []
    for metric in sorted(metric_values.keys()):
        values = metric_values[metric]
        
        if len(values) < 2:
            mean = values[0]
            std = 0.0
        else:
            import statistics
            mean = statistics.mean(values)
            std = statistics.stdev(values)  # Sample std deviation
        
        results.append((metric, mean, std, len(values)))
        print(f"{metric:20s}: {mean:.4f} ± {std:.4f}  (n={len(values)})")
    
    # Save to file
    output_file = os.path.join(results_dir, 'statistics_summary.txt')
    with open(output_file, 'w') as f:
        f.write("DuoRec Multi-Seed Results\n")
        f.write("="*70 + "\n\n")
        
        for metric, mean, std, n in results:
            f.write(f"{metric:20s}: {mean:.4f} ± {std:.4f}  (n={n})\n")
        
        f.write("\n" + "="*70 + "\n")
        f.write("Individual Values:\n\n")
        
        for metric in sorted(metric_values.keys()):
            values_str = ", ".join([f"{v:.4f}" for v in metric_values[metric]])
            f.write(f"{metric}: [{values_str}]\n")
    
    print(f"\nResults saved to: {output_file}")

if __name__ == '__main__':
    import sys
    results_dir = sys.argv[1] if len(sys.argv) > 1 else './results_multiple_seeds'
    
    if not os.path.exists(results_dir):
        print(f"Directory not found: {results_dir}")
        print("Run experiments first with: bash run_multiple_seeds.sh")
        sys.exit(1)
    
    calculate_stats(results_dir)
