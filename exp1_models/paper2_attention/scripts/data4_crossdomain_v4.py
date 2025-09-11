#!/usr/bin/env python3
"""
Data Extraction Script for Figure 4: CDAE Cross-Domain Adaptation Results
基于真实实验数据从results_gpu/d3/目录提取LOSO和LORO跨域性能数据

This script extracts authentic experimental data for paper2_pase_net Figure 4 CDAE cross-domain results.
Follows CLAUDE.md authenticity-first principle - NO hardcoding, only real experimental data.
"""

import json
import numpy as np
import pandas as pd
import os
from pathlib import Path

def extract_cross_domain_data():
    """从results_gpu/d3/目录提取真实的LOSO/LORO实验数据"""
    
    # 设置路径 - 从当前脚本位置向上找到results_gpu
    script_dir = Path(__file__).parent
    results_base = script_dir / ".." / ".." / ".." / "results_gpu" / "d3"
    
    if not results_base.exists():
        print(f"错误：实验结果目录不存在: {results_base}")
        return None
    
    print(f"从实验结果目录提取数据: {results_base}")
    
    # 提取LOSO数据
    loso_data = extract_protocol_data(results_base / "loso", "loso")
    
    # 提取LORO数据
    loro_data = extract_protocol_data(results_base / "loro", "loro")
    
    # 合并数据和计算统计信息
    combined_data = combine_and_analyze(loso_data, loro_data)
    
    # 保存提取的数据
    output_path = script_dir / ".." / "plots" / "data4_crossdomain_v4.csv"
    raw_output_path = script_dir / ".." / "plots" / "data4_crossdomain_v4_raw.csv"
    
    save_processed_data(combined_data, output_path)
    save_raw_data(loso_data, loro_data, raw_output_path)
    
    return combined_data

def extract_protocol_data(protocol_path, protocol_name):
    """从指定协议目录提取实验数据"""
    
    if not protocol_path.exists():
        print(f"警告：{protocol_name}目录不存在: {protocol_path}")
        return {}
    
    # 查找所有实验结果文件
    pattern = f"{protocol_name}_*.json"
    result_files = list(protocol_path.glob(pattern))
    
    print(f"\n从{protocol_name}目录找到{len(result_files)}个实验文件:")
    
    data = {}
    
    for file_path in result_files:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                result = json.load(f)
            
            # 从文件名提取模型名和种子
            filename = file_path.name
            parts = filename.replace('.json', '').split('_')
            
            if len(parts) < 3:
                continue
            
            # 处理模型名（考虑conformer_lite情况）
            if parts[1] == 'conformer' and len(parts) >= 4:
                model = 'conformer'
                seed = int(parts[3].replace('seed', ''))
            else:
                model = parts[1]
                seed = int(parts[2].replace('seed', ''))
            
            # 提取macro F1分数
            if 'aggregate_stats' in result and 'macro_f1' in result['aggregate_stats']:
                f1_score = result['aggregate_stats']['macro_f1'].get('mean', 0) * 100
                
                # 检查收敛性（F1 < 50%认为是收敛失败）
                convergence_success = 1 if f1_score >= 50 else 0
                
                if model not in data:
                    data[model] = []
                
                data[model].append({
                    'seed': seed,
                    'f1_score': f1_score,
                    'convergence_success': convergence_success,
                    'filename': filename
                })
                
                status = "成功" if convergence_success else "失败"
                print(f"  {filename}: {model} 种子{seed} -> {f1_score:.2f}% ({status})")
            
        except Exception as e:
            print(f"  错误读取 {file_path.name}: {str(e)}")
            continue
    
    return data

def combine_and_analyze(loso_data, loro_data):
    """合并LOSO和LORO数据并计算统计指标"""
    
    models = ['enhanced', 'cnn', 'bilstm', 'conformer']
    model_names = {
        'enhanced': 'PASE-Net',
        'cnn': 'CNN', 
        'bilstm': 'BiLSTM',
        'conformer': 'Conformer'
    }
    
    combined_results = []
    
    print(f"\n{'='*60}")
    print("跨域性能数据分析汇总")
    print(f"{'='*60}")
    
    for model in models:
        loso_scores = [item['f1_score'] for item in loso_data.get(model, [])]
        loro_scores = [item['f1_score'] for item in loro_data.get(model, [])]
        
        loso_failures = sum(1 for item in loso_data.get(model, []) if item['convergence_success'] == 0)
        loro_failures = sum(1 for item in loro_data.get(model, []) if item['convergence_success'] == 0)
        
        if loso_scores and loro_scores:
            loso_mean = np.mean(loso_scores)
            loso_std = np.std(loso_scores, ddof=1)
            loro_mean = np.mean(loro_scores)
            loro_std = np.std(loro_scores, ddof=1)
            domain_gap = abs(loso_mean - loro_mean)
            
            # 稳定性评估
            loso_cv = (loso_std / loso_mean * 100) if loso_mean > 0 else float('inf')
            loro_cv = (loro_std / loro_mean * 100) if loro_mean > 0 else float('inf')
            
            if loso_failures > 0 or loro_failures > 0:
                stability = "Unstable"
            elif max(loso_cv, loro_cv) < 2.0 and domain_gap < 1.0:
                stability = "Excellent"
            elif max(loso_cv, loro_cv) < 5.0 and domain_gap < 5.0:
                stability = "Good"
            else:
                stability = "Moderate"
            
            combined_results.append({
                'model': model,
                'model_name': model_names[model],
                'loso_mean': loso_mean,
                'loso_std': loso_std,
                'loso_failures': loso_failures,
                'loro_mean': loro_mean, 
                'loro_std': loro_std,
                'loro_failures': loro_failures,
                'domain_gap': domain_gap,
                'stability_status': stability
            })
            
            print(f"{model_names[model]:12s}: LOSO={loso_mean:.1f}±{loso_std:.1f}% LORO={loro_mean:.1f}±{loro_std:.1f}% Gap={domain_gap:.1f}% ({stability})")
            
            if loso_failures > 0:
                print(f"              警告: LOSO收敛失败 {loso_failures}/5 种子")
            if loro_failures > 0:
                print(f"              警告: LORO收敛失败 {loro_failures}/5 种子")
        else:
            print(f"{model_names[model]:12s}: 数据缺失")
    
    return combined_results

def save_processed_data(data, output_path):
    """保存处理后的汇总数据"""
    
    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False)
    print(f"\n汇总统计数据保存至: {output_path}")

def save_raw_data(loso_data, loro_data, output_path):
    """保存原始实验数据"""
    
    raw_records = []
    
    # 添加LOSO数据
    for model, results in loso_data.items():
        model_name = {'enhanced': 'PASE-Net', 'cnn': 'CNN', 'bilstm': 'BiLSTM', 'conformer': 'Conformer'}[model]
        for result in results:
            raw_records.append({
                'model': model,
                'model_name': model_name,
                'seed': result['seed'],
                'protocol': 'LOSO',
                'f1_score': result['f1_score'],
                'convergence_success': result['convergence_success']
            })
    
    # 添加LORO数据
    for model, results in loro_data.items():
        model_name = {'enhanced': 'PASE-Net', 'cnn': 'CNN', 'bilstm': 'BiLSTM', 'conformer': 'Conformer'}[model]
        for result in results:
            raw_records.append({
                'model': model,
                'model_name': model_name,
                'seed': result['seed'],
                'protocol': 'LORO',
                'f1_score': result['f1_score'],
                'convergence_success': result['convergence_success']
            })
    
    df = pd.DataFrame(raw_records)
    df.to_csv(output_path, index=False)
    print(f"原始实验数据保存至: {output_path}")

def main():
    """主函数"""
    print("=" * 60)
    print("Paper2 PaseNet 图4数据提取脚本")
    print("基于真实实验结果，禁止硬编码数据")
    print("=" * 60)
    
    data = extract_cross_domain_data()
    
    if data:
        print(f"\n✅ 数据提取完成！共处理{len(data)}个模型的跨域性能数据")
        print("下一步: 运行 scr4_crossdomain_v4.py 生成图4")
    else:
        print("\n❌ 数据提取失败")

if __name__ == "__main__":
    main()