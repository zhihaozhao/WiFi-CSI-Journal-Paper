#!/usr/bin/env python3
"""
Data extraction script for Figure 2: Synthetic Data Generation Framework
Extracts framework components and parameterization for comprehensive visualization.

File: data2_synthetic_framework_v1.py
Purpose: Extract synthetic data generation framework specifications
"""

import json
import csv
import os
import numpy as np
from datetime import datetime

def extract_synthetic_framework_data():
    """
    Extract synthetic data generation framework specifications
    Based on: Comprehensive Synthetic Data Generation Framework
    """
    
    framework_data = {
        "metadata": {
            "extraction_date": datetime.now().isoformat(),
            "version": "v1",
            "figure_id": "fig2_physics_guided_framework", 
            "data_source": "Synthetic CSI Data Generation Framework Specifications"
        },
        
        "signal_model_foundation": {
            "csi_representation": "H(f,t) = A(f,t) * exp(j*Φ(f,t))",
            "system_parameters": {
                "N_tx": "transmit antennas",
                "N_rx": "receive antennas", 
                "N_sc": "subcarriers",
                "ofdm_structure": "multiple subcarriers"
            }
        },
        
        "multipath_propagation": {
            "model": "h(t) = Σ αᵢ(t)δ(t - τᵢ(t))",
            "components": {
                "alpha_i": "complex amplitude i-th path",
                "tau_i": "delay i-th path", 
                "N_paths": "number of propagation paths"
            },
            "phenomena": ["reflections", "diffractions", "scattering"],
            "sources": ["walls", "furniture", "objects"]
        },
        
        "human_body_interaction": {
            "fresnel_reflection": {
                "formula": "Γ = (√εᵣ - 1)/(√εᵣ + 1)",
                "parameter": "εᵣ = relative permittivity human tissue"
            },
            "doppler_effect": {
                "formula": "fₐ = (v·cos(θ)/c)·fᶜ",
                "parameters": {
                    "v": "velocity",
                    "theta": "angle between velocity and signal path",
                    "c": "speed of light",
                    "f_c": "carrier frequency"
                }
            },
            "mechanisms": ["absorption", "scattering", "time_varying_perturbations"]
        },
        
        "environmental_modeling": {
            "variations": {
                "room_geometry": "parameterized dimensions",
                "wall_materials": "material property modeling",
                "furniture_placement": "randomized configurations",
                "device_positions": "configurable locations"
            },
            "noise_model": "H_observed(f,t) = H_ideal(f,t) + N(f,t) + I(f,t)",
            "noise_components": {
                "N(f,t)": "thermal noise and hardware imperfections",
                "I(f,t)": "co-channel interference patterns"
            }
        },
        
        "parameterized_generation": {
            "formula": "X_synth, y_synth = G(θ_activity, θ_env, θ_signal, θ_noise)",
            "parameter_categories": {
                "activity_parameters": [
                    "activity_type", "duration", "movement_patterns", "num_subjects"
                ],
                "environmental_parameters": [
                    "room_dimensions", "wall_materials", "furniture_layout", "device_positions" 
                ],
                "signal_parameters": [
                    "carrier_frequency", "bandwidth", "antenna_configuration", "transmission_power"
                ],
                "noise_parameters": [
                    "SNR_levels", "interference_patterns", "hardware_imperfections"
                ],
                "difficulty_parameters": [
                    "class_overlap", "label_noise", "environmental_variability"
                ]
            }
        },
        
        "multi_level_caching": {
            "disk_caching": {
                "format": ".pkl files",
                "identifier": "MD5-based unique identifiers",
                "purpose": "reuse across experiments"
            },
            "memory_caching": {
                "policy": "LRU eviction",
                "purpose": "accelerate data loading during training"
            },
            "performance_improvement": "reduces generation time from minutes to seconds"
        },
        
        "framework_validation": {
            "sim2real_performance": {
                "f1_score": "82.1% with 20% real data",
                "efficiency_gain": "80% labeling cost reduction"  
            },
            "edge_compatibility": "maintained computational efficiency",
            "evaluation_protocols": 540  # configurations across SRV
        },
        
        "generation_configurations": {
            "time_steps": [32, 64, 128],
            "feature_dimensions": [30, 52, 90], 
            "difficulty_levels": ["easy", "medium", "hard"],
            "noise_parameters": {
                "class_overlap": [0.0, 0.4, 0.8],
                "label_noise": [0.0, 0.05, 0.1]
            },
            "environmental_variations": {
                "burst_rates": [0.0, 0.1, 0.2],
                "gain_drift": "modeled"
            }
        }
    }
    
    return framework_data

def save_data_formats(data, base_filename):
    """Save data in both JSON and CSV formats"""
    
    # Save JSON format
    json_file = f"{base_filename}.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    # Save CSV format for framework components
    csv_file = f"{base_filename}.csv"
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Write headers
        writer.writerow(['Framework_Component', 'Subcomponent', 'Parameter', 'Value', 'Formula'])
        
        # Specific processing for framework data
        for component, component_data in data.items():
            if component == 'metadata':
                continue
                
            if isinstance(component_data, dict):
                for sub_component, sub_data in component_data.items():
                    if isinstance(sub_data, dict):
                        for param, value in sub_data.items():
                            formula = value if 'formula' in param.lower() or any(op in str(value) for op in ['=', '+', '*', '/', '(', ')']) else ''
                            writer.writerow([component, sub_component, param, str(value), formula])
                    elif isinstance(sub_data, list):
                        writer.writerow([component, sub_component, 'items', '; '.join(map(str, sub_data)), ''])
                    else:
                        writer.writerow([component, sub_component, '', str(sub_data), ''])
            else:
                writer.writerow([component, '', '', str(component_data), ''])
    
    return json_file, csv_file

def main():
    """Main execution function"""
    
    print("Extracting Figure 2 Synthetic Framework data...")
    
    # Create output directory if it doesn't exist
    output_dir = "."
    os.makedirs(output_dir, exist_ok=True)
    
    # Extract data
    framework_data = extract_synthetic_framework_data()
    
    # Save in multiple formats
    base_filename = os.path.join(output_dir, "data2_synthetic_framework_v1")
    json_file, csv_file = save_data_formats(framework_data, base_filename)
    
    print("Synthetic framework data extracted successfully!")
    print(f"JSON format: {json_file}")
    print(f"CSV format: {csv_file}")
    print(f"Framework components: {len(framework_data) - 1} major components")  # -1 for metadata
    
    # Print summary  
    print("\nSynthetic Framework Summary:")
    print(f"   Parameter categories: {len(framework_data['parameterized_generation']['parameter_categories'])}")
    print(f"   Generation configurations: {framework_data['framework_validation']['evaluation_protocols']} total")
    print(f"   Sim2Real F1 score: {framework_data['framework_validation']['sim2real_performance']['f1_score']}")
    print(f"   Efficiency gain: {framework_data['framework_validation']['sim2real_performance']['efficiency_gain']}")
    print(f"   Time steps range: {framework_data['generation_configurations']['time_steps']}")
    print(f"   Feature dimensions: {framework_data['generation_configurations']['feature_dimensions']}")

if __name__ == "__main__":
    main()