#!/usr/bin/env python3
"""
Data Extraction Script for Figure 2: Physics-Informed Synthetic Data Generation Framework
Extracts authentic SRV synthetic robustness data for methodological framework illustration

Purpose: Extract summary performance data for Figure 2(c) SRV results matrix
Data Source: SRV synthetic robustness experiments - same source as Figure 3 but aggregated
Focus: Model performance across noise levels for framework validation
"""

import json
import numpy as np
import pandas as pd
import os
from pathlib import Path
import glob

def extract_srv_framework_data():
    """Extract SRV experimental data for Figure 2 framework illustration"""
    
    script_dir = Path(__file__).parent
    srv_path = script_dir / ".." / ".." / ".." / "results_gpu" / "d2"
    
    if not srv_path.exists():
        print(f"Error: SRV directory not found: {srv_path}")
        return None
    
    print(f"Extracting Framework data from SRV experiments: {srv_path}")
    
    # Find all SRV experiment files
    json_files = list(srv_path.glob("*.json"))
    print(f"Found {len(json_files)} SRV experiments for framework analysis")
    
    framework_data = []
    
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
                robustness_params_start = 5  # parameters start at index 5
            else:
                model = parts[1]
                robustness_params_start = 4  # parameters start at index 4
            
            # Parse noise parameters for framework illustration
            label_noise = float(parts[robustness_params_start + 2].replace('lab', '').replace('p', '.'))
            
            # Extract performance metrics
            metrics = data.get('metrics', {})
            macro_f1 = metrics.get('macro_f1', 0)
            
            # Categorize noise levels for framework matrix
            if label_noise == 0.0:
                noise_category = "0%"
            elif label_noise <= 0.05:
                noise_category = "5%"
            elif label_noise <= 0.1:
                noise_category = "10%"
            else:
                noise_category = "15%+"
            
            framework_data.append({
                'filename': filename,
                'model': model,
                'label_noise': label_noise,
                'noise_category': noise_category,
                'macro_f1': macro_f1
            })
            
        except Exception as e:
            print(f"Error processing {file_path.name}: {e}")
            continue
    
    if not framework_data:
        return None
    
    df = pd.DataFrame(framework_data)
    print(f"Successfully extracted {len(df)} framework experiments from SRV")
    
    return df

def calculate_framework_matrix(df):
    """Calculate performance matrix for Figure 2(c) framework illustration"""
    
    models = ['enhanced', 'cnn', 'bilstm', 'conformer_lite']
    model_names = {
        'enhanced': 'PASE-Net',
        'cnn': 'CNN',
        'bilstm': 'BiLSTM', 
        'conformer_lite': 'Conformer'
    }
    
    noise_levels = ["0%", "5%", "10%", "15%+"]
    
    # Create performance matrix
    framework_matrix = []
    framework_stats = []
    
    for model in models:
        model_data = df[df['model'] == model]
        if model_data.empty:
            # Skip missing models
            continue
            
        row = []
        for noise_cat in noise_levels:
            noise_data = model_data[model_data['noise_category'] == noise_cat]
            if len(noise_data) > 0:
                mean_f1 = noise_data['macro_f1'].mean()
                std_f1 = noise_data['macro_f1'].std()
                row.append(mean_f1)
            else:
                row.append(0.0)  # No data available
        
        if any(x > 0 for x in row):  # Only include models with data
            framework_matrix.append(row)
            framework_stats.append({
                'model': model,
                'model_name': model_names[model],
                'performance_across_noise': row,
                'avg_performance': np.mean([x for x in row if x > 0])
            })
    
    return np.array(framework_matrix), framework_stats, noise_levels

def save_framework_data(df, framework_matrix, framework_stats, noise_levels):
    """Save framework data for Figure 2 generation"""
    
    script_dir = Path(__file__).parent
    
    # Save raw framework data
    raw_output = script_dir / ".." / "plots" / "data2_framework_raw.csv"
    df.to_csv(raw_output, index=False)
    
    # Save framework matrix and metadata
    framework_data = {
        'metadata': {
            'description': 'Framework data extracted from SRV synthetic experiments for Figure 2',
            'total_experiments': len(df),
            'models': [stat['model'] for stat in framework_stats],
            'noise_levels': noise_levels,
            'extraction_script': 'scripts/data2_framework_v1.py'
        },
        'performance_matrix': framework_matrix.tolist(),
        'model_statistics': framework_stats,
        'noise_categories': noise_levels
    }
    
    framework_output = script_dir / ".." / "plots" / "data2_framework_v1.json"
    with open(framework_output, 'w', encoding='utf-8') as f:
        json.dump(framework_data, f, indent=2, ensure_ascii=False)
    
    # Save CSV summary for easy access
    summary_data = []
    for i, stat in enumerate(framework_stats):
        for j, noise in enumerate(noise_levels):
            summary_data.append({
                'model': stat['model'],
                'model_name': stat['model_name'], 
                'noise_level': noise,
                'performance': framework_matrix[i][j] if i < len(framework_matrix) else 0.0
            })
    
    summary_df = pd.DataFrame(summary_data)
    summary_output = script_dir / ".." / "plots" / "data2_framework_v1.csv"
    summary_df.to_csv(summary_output, index=False)
    
    print(f"SRV framework raw data saved: {raw_output}")
    print(f"SRV framework JSON data saved: {framework_output}")
    print(f"SRV framework summary saved: {summary_output}")
    
    return framework_output

def analyze_framework_results(df, framework_stats):
    """Analyze framework experimental results"""
    
    print(f"\n{'='*60}")
    print("Figure 2 Framework Data Analysis")
    print(f"{'='*60}")
    
    print(f"Total experiments analyzed: {len(df)}")
    print(f"Models with data: {', '.join([stat['model_name'] for stat in framework_stats])}")
    
    # Noise level distribution
    noise_dist = df['noise_category'].value_counts()
    print(f"\nNoise Level Distribution:")
    for noise, count in noise_dist.items():
        print(f"  {noise}: {count} experiments")
    
    # Performance summary
    print(f"\nFramework Performance Summary:")
    for stat in framework_stats:
        avg_perf = stat['avg_performance']
        print(f"  {stat['model_name']:12s}: {avg_perf:.3f} average across noise levels")
    
    # Best performer
    if framework_stats:
        best_model = max(framework_stats, key=lambda x: x['avg_performance'])
        print(f"\nBest Framework Performance: {best_model['model_name']} ({best_model['avg_performance']:.3f})")

def main():
    """Main function for Figure 2 framework data extraction"""
    print("=" * 60)
    print("Figure 2 Physics-Informed Framework Data Extraction")
    print("Extracting SRV experiments for methodological illustration")
    print("=" * 60)
    
    # Extract framework data
    df = extract_srv_framework_data()
    if df is None:
        print("Error: Failed to extract SRV framework data")
        return
    
    # Calculate framework matrix
    framework_matrix, framework_stats, noise_levels = calculate_framework_matrix(df)
    
    # Save framework data
    output_file = save_framework_data(df, framework_matrix, framework_stats, noise_levels)
    
    # Analyze results
    analyze_framework_results(df, framework_stats)
    
    print(f"\nSRV framework data extraction completed successfully!")
    print("Next step: Run scr2_physics_modeling_v4.py to generate Figure 2")

if __name__ == "__main__":
    main()