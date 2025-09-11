#!/usr/bin/env python3
"""
Data Extraction Script for Figure 3: SRV Synthetic Robustness Validation
Extracts authentic D2 synthetic robustness data with statistical outlier handling

Purpose: Extract 668 synthetic robustness trials data for model comparison
Parameters: Class overlap (ρ), Environmental bursts (β), Label noise (η)
Focus: Performance under controlled perturbations + Calibration improvement
"""

import json
import numpy as np
import pandas as pd
import os
from pathlib import Path
import glob
from scipy import stats

def extract_d2_robustness_parameters():
    """Extract D2 synthetic robustness experiment data with parameter parsing"""
    
    script_dir = Path(__file__).parent
    d2_path = script_dir / ".." / ".." / ".." / "results_gpu" / "d2"
    
    if not d2_path.exists():
        print(f"Error: D2 directory not found: {d2_path}")
        return None
    
    print(f"Extracting SRV data from: {d2_path}")
    
    # Find all D2 experiment files
    json_files = list(d2_path.glob("*.json"))
    print(f"Found {len(json_files)} D2 synthetic robustness experiments")
    
    robustness_data = []
    
    for file_path in json_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            filename = file_path.name
            
            # Parse filename: paperA_MODEL_hard_SEED_claXXX_envXXX_labXXX.json
            # Handle conformer_lite: paperA_conformer_lite_hard_s0_...
            parts = filename.replace('.json', '').split('_')
            if len(parts) < 7:
                continue
            
            # Extract model name (handle multi-part names like conformer_lite)
            if parts[1] == 'conformer' and len(parts) > 2 and parts[2] == 'lite':
                model = 'conformer_lite'
                seed_part = parts[4]  # seed is at index 4 for conformer_lite
                robustness_params_start = 5  # parameters start at index 5
            else:
                model = parts[1]
                seed_part = parts[3]  # seed is at index 3 for other models
                robustness_params_start = 4  # parameters start at index 4
            
            seed = int(seed_part[1:])  # s0 -> 0
            
            # Parse robustness parameters
            class_overlap = float(parts[robustness_params_start].replace('cla', '').replace('p', '.'))
            env_burst = float(parts[robustness_params_start + 1].replace('env', '').replace('p', '.'))  
            label_noise = float(parts[robustness_params_start + 2].replace('lab', '').replace('p', '.'))
            
            # Extract metrics
            metrics = data.get('metrics', {})
            macro_f1 = metrics.get('macro_f1', 0)
            ece_raw = metrics.get('ece_raw', 0)
            ece_cal = metrics.get('ece_cal', 0)
            temperature = metrics.get('temperature', 1.0)
            
            # Calculate stress level (composite stress score)
            stress_score = class_overlap + env_burst + label_noise
            
            robustness_data.append({
                'filename': filename,
                'model': model,
                'seed': seed,
                'class_overlap': class_overlap,
                'env_burst': env_burst,
                'label_noise': label_noise,
                'stress_score': stress_score,
                'macro_f1': macro_f1,
                'ece_raw': ece_raw,
                'ece_cal': ece_cal,
                'ece_improvement': (ece_raw - ece_cal) / ece_raw * 100 if ece_raw > 0 else 0,
                'temperature': temperature
            })
            
        except Exception as e:
            print(f"Error processing {file_path.name}: {e}")
            continue
    
    if not robustness_data:
        return None
        
    df = pd.DataFrame(robustness_data)
    print(f"Successfully extracted {len(df)} robustness experiments")
    
    return df

def apply_statistical_outlier_handling(df):
    """Apply statistical methods to handle outliers for fair model comparison"""
    
    models = df['model'].unique()
    processed_data = []
    
    for model in models:
        model_data = df[df['model'] == model].copy()
        
        # Handle F1 score outliers using IQR method
        Q1_f1 = model_data['macro_f1'].quantile(0.25)
        Q3_f1 = model_data['macro_f1'].quantile(0.75)
        IQR_f1 = Q3_f1 - Q1_f1
        
        # Define outlier bounds
        lower_bound = Q1_f1 - 1.5 * IQR_f1
        upper_bound = Q3_f1 + 1.5 * IQR_f1
        
        # Cap outliers instead of removing (preserve all model comparisons)
        model_data['macro_f1_processed'] = model_data['macro_f1'].clip(lower_bound, upper_bound)
        
        # Handle ECE outliers (log-transform for highly skewed distributions)
        model_data['ece_raw_log'] = np.log1p(model_data['ece_raw'])
        model_data['ece_cal_log'] = np.log1p(model_data['ece_cal'])
        
        # Winsorization for temperature (handle extreme values)
        temp_5th = model_data['temperature'].quantile(0.05)
        temp_95th = model_data['temperature'].quantile(0.95)
        model_data['temperature_winsorized'] = model_data['temperature'].clip(temp_5th, temp_95th)
        
        processed_data.append(model_data)
    
    return pd.concat(processed_data, ignore_index=True)

def calculate_robustness_statistics(df):
    """Calculate comprehensive robustness statistics for visualization"""
    
    # Group by model and calculate aggregate statistics
    model_stats = []
    
    for model in df['model'].unique():
        model_data = df[df['model'] == model]
        
        # Performance statistics
        f1_mean = model_data['macro_f1_processed'].mean()
        f1_std = model_data['macro_f1_processed'].std()
        f1_min = model_data['macro_f1_processed'].min()
        
        # Calibration statistics
        ece_improvement_mean = model_data['ece_improvement'].mean()
        ece_raw_median = model_data['ece_raw'].median()
        ece_cal_median = model_data['ece_cal'].median()
        
        # Robustness under high stress
        high_stress_data = model_data[model_data['stress_score'] > model_data['stress_score'].quantile(0.8)]
        high_stress_f1 = high_stress_data['macro_f1_processed'].mean() if len(high_stress_data) > 0 else f1_mean
        
        # Temperature scaling effectiveness
        temp_median = model_data['temperature_winsorized'].median()
        temp_std = model_data['temperature_winsorized'].std()
        
        model_stats.append({
            'model': model,
            'model_name': {'enhanced': 'PASE-Net', 'cnn': 'CNN', 'bilstm': 'BiLSTM', 'conformer_lite': 'Conformer'}.get(model, model),
            'f1_mean': f1_mean,
            'f1_std': f1_std,
            'f1_min': f1_min,
            'f1_high_stress': high_stress_f1,
            'ece_improvement': ece_improvement_mean,
            'ece_raw_median': ece_raw_median,
            'ece_cal_median': ece_cal_median,
            'temperature_median': temp_median,
            'temperature_std': temp_std,
            'robustness_score': high_stress_f1 * (1 + ece_improvement_mean/100)  # Composite score
        })
    
    return pd.DataFrame(model_stats)

def save_srv_data(df_raw, df_stats):
    """Save SRV robustness data for figure generation"""
    
    script_dir = Path(__file__).parent
    
    # Save processed raw data
    raw_output = script_dir / ".." / "plots" / "data3_srv_robustness_raw.csv"
    df_raw.to_csv(raw_output, index=False)
    
    # Save model statistics
    stats_output = script_dir / ".." / "plots" / "data3_srv_robustness_v4.csv"
    df_stats.to_csv(stats_output, index=False)
    
    print(f"Raw robustness data saved: {raw_output}")
    print(f"Model statistics saved: {stats_output}")
    
    return stats_output

def analyze_srv_results(df_raw, df_stats):
    """Analyze SRV experimental results"""
    
    print(f"\n{'='*60}")
    print("SRV Synthetic Robustness Validation Analysis")
    print(f"{'='*60}")
    
    print(f"Total experiments analyzed: {len(df_raw)}")
    print(f"Models: {', '.join(df_stats['model_name'].tolist())}")
    
    # Parameter ranges
    print(f"\nStress Parameter Ranges:")
    print(f"Class Overlap (ρ): {df_raw['class_overlap'].min():.1f} - {df_raw['class_overlap'].max():.1f}")
    print(f"Environmental Burst (β): {df_raw['env_burst'].min():.1f} - {df_raw['env_burst'].max():.1f}")
    print(f"Label Noise (η): {df_raw['label_noise'].min():.2f} - {df_raw['label_noise'].max():.2f}")
    
    # Performance summary
    print(f"\nModel Performance Summary:")
    for _, row in df_stats.iterrows():
        print(f"{row['model_name']:12s}: F1={row['f1_mean']:.1f}±{row['f1_std']:.2f}% "
              f"HighStress={row['f1_high_stress']:.1f}% ECE↓{row['ece_improvement']:.1f}%")
    
    # Best performers
    best_overall = df_stats.loc[df_stats['robustness_score'].idxmax(), 'model_name']
    best_calibration = df_stats.loc[df_stats['ece_improvement'].idxmax(), 'model_name']
    
    print(f"\nBest Overall Robustness: {best_overall}")
    print(f"Best Calibration Improvement: {best_calibration}")

def main():
    """Main function for SRV data extraction"""
    print("=" * 60)
    print("SRV Synthetic Robustness Validation Data Extraction")
    print("Extracting D2 experiments with statistical outlier handling")
    print("=" * 60)
    
    # Extract raw robustness data
    df_raw = extract_d2_robustness_parameters()
    if df_raw is None:
        print("Error: Failed to extract D2 robustness data")
        return
    
    # Apply statistical outlier handling
    df_processed = apply_statistical_outlier_handling(df_raw)
    
    # Calculate model statistics
    df_stats = calculate_robustness_statistics(df_processed)
    
    # Save data
    output_file = save_srv_data(df_processed, df_stats)
    
    # Analyze results
    analyze_srv_results(df_processed, df_stats)
    
    print(f"\nSRV data extraction completed successfully!")
    print("Next step: Run scr3_srv_robustness_v4.py to generate Figure 3")

if __name__ == "__main__":
    main()