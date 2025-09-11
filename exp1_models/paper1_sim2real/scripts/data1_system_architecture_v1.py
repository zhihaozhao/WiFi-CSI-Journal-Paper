#!/usr/bin/env python3
"""
Data extraction script for Figure 1: System Architecture Overview
Extracts architectural components and parameter specifications for system overview diagram.

File: data1_system_architecture_v1.py
Purpose: Extract system architecture data for comprehensive pipeline visualization
"""

import json
import csv
import os
from datetime import datetime

def extract_system_architecture_data():
    """
    Extract system architecture components and specifications
    Based on: Enhanced Attention Network Sim2Real Pipeline
    """
    
    # System components and specifications
    system_data = {
        "metadata": {
            "extraction_date": datetime.now().isoformat(),
            "version": "v1",
            "figure_id": "fig1_system_architecture",
            "data_source": "Enhanced Attention Network Architecture Specifications"
        },
        
        "synthetic_generation_components": {
            "multipath_modeling": {
                "technique": "Channel impulse response modeling",
                "formula": "h(t) = Σ αᵢ(t)δ(t - τᵢ(t))",
                "parameters": ["complex_amplitude", "propagation_delay"]
            },
            "human_interaction_modeling": {
                "fresnel_reflection": "Γ = (√εᵣ - 1)/(√εᵣ + 1)",
                "doppler_shift": "fₐ = (v·cos(θ)/c)·fᶜ",
                "parameters": ["velocity", "angle", "permittivity"]
            },
            "environmental_variations": {
                "room_geometry": "parameterized",
                "wall_materials": "modeled", 
                "furniture_placement": "randomized",
                "device_positions": "configurable"
            }
        },
        
        "enhanced_attention_network": {
            "architecture_type": "CNN + SE + Temporal Attention",
            "total_parameters": 640713,
            "attention_parameters": 411520,
            "attention_percentage": 64.2,
            "components": [
                "DepthwiseConv2D",
                "PointwiseConv2D", 
                "Squeeze-and-Excitation",
                "MultiHeadTemporalAttention"
            ],
            "optimization": "Edge deployment optimized"
        },
        
        "evaluation_protocols": {
            "SRV": {"configurations": 540, "focus": "synthetic robustness"},
            "CDAE": {"configurations": 40, "focus": "cross-domain adaptation"},
            "STEA": {"configurations": 56, "focus": "sim2real efficiency"},
            "Edge_Analysis": {"platform": "Xavier AGX 32G", "focus": "deployment feasibility"}
        },
        
        "edge_deployment": {
            "platform": "Xavier AGX 32G",
            "cpu": "ARM Cortex-A78AE",
            "gpu": "NVIDIA Volta (512 CUDA cores)",
            "memory": "32GB LPDDR4x",
            "cuda_memory": "31.17GB",
            "compute_capability": 7.2
        },
        
        "performance_metrics": {
            "cross_domain_f1": "83.0±0.1%",
            "loso_loro_consistency": "identical performance",
            "label_efficiency": "82.1% F1 with 20% data",
            "throughput": "607 samples/second",
            "latency": "5.3ms",
            "memory_footprint": "2.44MB"
        }
    }
    
    return system_data

def save_data_formats(data, base_filename):
    """Save data in both JSON and CSV formats"""
    
    # Save JSON format
    json_file = f"{base_filename}.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    # Save CSV format (flattened for tabular representation)
    csv_file = f"{base_filename}.csv"
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Write headers
        writer.writerow(['Component', 'Subcomponent', 'Parameter', 'Value', 'Description'])
        
        # Flatten system data for CSV
        for main_component, component_data in data.items():
            if isinstance(component_data, dict):
                for sub_component, sub_data in component_data.items():
                    if isinstance(sub_data, dict):
                        for param, value in sub_data.items():
                            writer.writerow([main_component, sub_component, param, str(value), ''])
                    else:
                        writer.writerow([main_component, sub_component, '', str(sub_data), ''])
            else:
                writer.writerow([main_component, '', '', str(component_data), ''])
    
    return json_file, csv_file

def main():
    """Main execution function"""
    
    print("Extracting Figure 1 System Architecture data...")
    
    # Create output directory if it doesn't exist
    output_dir = "."
    os.makedirs(output_dir, exist_ok=True)
    
    # Extract data
    system_data = extract_system_architecture_data()
    
    # Save in multiple formats
    base_filename = os.path.join(output_dir, "data1_system_architecture_v1")
    json_file, csv_file = save_data_formats(system_data, base_filename)
    
    print("System architecture data extracted successfully!")
    print(f"JSON format: {json_file}")
    print(f"CSV format: {csv_file}")
    print(f"Components: {len(system_data)} major components analyzed")
    
    # Print summary
    print("\nSystem Architecture Summary:")
    print(f"   • Enhanced Attention Network: {system_data['enhanced_attention_network']['total_parameters']} parameters")
    print(f"   • Attention modules: {system_data['enhanced_attention_network']['attention_percentage']}% of total parameters")
    print(f"   • Cross-domain F1: {system_data['performance_metrics']['cross_domain_f1']}")
    print(f"   • Edge throughput: {system_data['performance_metrics']['throughput']}")
    print(f"   • Memory footprint: {system_data['performance_metrics']['memory_footprint']}")

if __name__ == "__main__":
    main()