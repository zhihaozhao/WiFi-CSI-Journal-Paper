#!/usr/bin/env python3
"""
Data extraction script for Figure 4: Experimental Protocols Overview
Extracts evaluation protocol specifications and configuration data.

File: data4_experimental_protocols_v1.py
Purpose: Extract systematic evaluation protocols data
"""

import json
import csv
import os
from datetime import datetime

def extract_experimental_protocols_data():
    """
    Extract experimental protocols and evaluation configurations
    Based on: SRV, CDAE, STEA, and Edge Deployment Analysis protocols
    """
    
    protocols_data = {
        "metadata": {
            "extraction_date": datetime.now().isoformat(),
            "version": "v1", 
            "figure_id": "fig4_experimental_protocols",
            "data_source": "Systematic Evaluation Protocols Specifications"
        },
        
        "evaluation_protocols": {
            "SRV": {
                "name": "Synthetic Robustness Validation",
                "configurations": 540,
                "focus": "synthetic robustness across noise, class overlap, and difficulty conditions",
                "parameters": {
                    "noise_levels": [0.0, 0.4, 0.8],
                    "class_overlap": [0.0, 0.4, 0.8],
                    "label_noise": [0.0, 0.05, 0.1], 
                    "difficulty_levels": ["easy", "medium", "hard"]
                }
            },
            "CDAE": {
                "name": "Cross-Domain Adaptation Evaluation", 
                "configurations": 40,
                "focus": "LOSO/LORO generalization validation",
                "protocols": {
                    "LOSO": "Leave-One-Subject-Out (subject shift)",
                    "LORO": "Leave-One-Room-Out (environment shift)"
                },
                "objective": "precise attribution of performance variations to domain shift phenomena"
            },
            "STEA": {
                "name": "Sim2Real Transfer Efficiency Assessment",
                "configurations": 56, 
                "focus": "Sim2Real label efficiency quantification",
                "efficiency_curve": {
                    "bootstrap_phase": "1% - synthetic pretraining vs zero-shot baseline",
                    "rapid_improvement": "5% - performance jumps to 78.0±1.6% F1", 
                    "convergence_phase": "≥20% - performance stabilizes at 82.1±0.3% F1"
                },
                "target_performance": "82.1% F1 using only 20% labeled real data"
            },
            "Edge_Deployment_Analysis": {
                "name": "Edge Deployment Characterization",
                "platform": "Xavier AGX 32G",
                "focus": "practical edge deployment feasibility",
                "batch_sizes": [1, 4, 8],
                "metrics": ["throughput", "latency", "memory optimization"]
            }
        },
        
        "integrated_evaluation_framework": {
            "total_configurations": 640, # 540 + 40 + 56 + edge analysis
            "evaluation_dimensions": [
                "accuracy", "cross-domain robustness", "label efficiency", 
                "computational efficiency", "memory constraints", "real-time inference"
            ],
            "hardware_platforms": ["Xavier AGX 32G"],
            "systematic_assessment": "from synthetic generation to practical deployment"
        },
        
        "benchmark_datasets": {
            "SenseFi_datasets": {
                "UT_HAR": {"classes": 7, "environment": "controlled indoor"},
                "NTU_Fi_HAR": {"classes": 6, "environment": "multiple room configurations"},  
                "NTU_Fi_HumanID": {"classes": 14, "task": "person identification"},
                "Widar": {"classes": 22, "task": "fine-grained hand gesture recognition"}
            }
        },
        
        "model_architectures": {
            "Enhanced_Attention_Network": "CNN + SE + Temporal Attention (proposed)",
            "CNN": "convolutional neural network baseline",
            "BiLSTM": "bidirectional LSTM temporal modeling", 
            "Conformer_lite": "lightweight Conformer architecture variant",
            "parameter_alignment": "within ±10% for fair comparison"
        },
        
        "edge_hardware_configuration": {
            "platform": "Xavier AGX 32G",
            "cpu": "ARM Cortex-A78AE",
            "gpu": "NVIDIA Volta GPU (512 CUDA cores)",
            "memory": "32GB LPDDR4x",
            "cuda_memory": "31.17GB", 
            "compute_capability": 7.2,
            "deployment_environment": "realistic edge deployment"
        },
        
        "key_performance_targets": {
            "cross_domain_consistency": "83.0±0.1% F1 across LOSO/LORO",
            "label_efficiency": "82.1% F1 with 20% real data (80% cost reduction)",
            "edge_throughput": "607 samples/second", 
            "edge_latency": "5.3ms single-sample",
            "memory_footprint": "2.44MB",
            "gpu_speedup": "64.1x acceleration"
        }
    }
    
    return protocols_data

def save_data_formats(data, base_filename):
    """Save data in both JSON and CSV formats"""
    
    # Save JSON format
    json_file = f"{base_filename}.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    # Save CSV format
    csv_file = f"{base_filename}.csv"
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Write headers
        writer.writerow(['Protocol_Category', 'Protocol_Name', 'Parameter', 'Value', 'Description'])
        
        # Process protocols data
        for category, category_data in data.items():
            if category == 'metadata':
                continue
                
            if isinstance(category_data, dict):
                for protocol, protocol_data in category_data.items():
                    if isinstance(protocol_data, dict):
                        for param, value in protocol_data.items():
                            description = param.replace('_', ' ').title()
                            writer.writerow([category, protocol, param, str(value), description])
                    else:
                        writer.writerow([category, protocol, '', str(protocol_data), ''])
            else:
                writer.writerow([category, '', '', str(category_data), ''])
    
    return json_file, csv_file

def main():
    """Main execution function"""
    
    print("Extracting Figure 4 Experimental Protocols data...")
    
    # Create output directory if it doesn't exist
    output_dir = "."
    os.makedirs(output_dir, exist_ok=True)
    
    # Extract data
    protocols_data = extract_experimental_protocols_data()
    
    # Save in multiple formats
    base_filename = os.path.join(output_dir, "data4_experimental_protocols_v1")
    json_file, csv_file = save_data_formats(protocols_data, base_filename)
    
    print("Experimental protocols data extracted successfully!")
    print(f"JSON format: {json_file}")
    print(f"CSV format: {csv_file}")
    print(f"Protocol categories: {len(protocols_data) - 1} major categories")
    
    # Print summary
    print("\nExperimental Protocols Summary:")
    srv_configs = protocols_data['evaluation_protocols']['SRV']['configurations']
    cdae_configs = protocols_data['evaluation_protocols']['CDAE']['configurations']
    stea_configs = protocols_data['evaluation_protocols']['STEA']['configurations']
    total_configs = protocols_data['integrated_evaluation_framework']['total_configurations']
    
    print(f"   SRV: {srv_configs} configurations")
    print(f"   CDAE: {cdae_configs} configurations") 
    print(f"   STEA: {stea_configs} configurations")
    print(f"   Total: {total_configs} evaluation configurations")
    print(f"   Target performance: {protocols_data['key_performance_targets']['label_efficiency']}")
    print(f"   Edge platform: {protocols_data['edge_hardware_configuration']['platform']}")

if __name__ == "__main__":
    main()