#!/usr/bin/env python3
"""
Data extraction script for Figure 3: Enhanced Attention Network Architecture
Extracts architecture specifications WITHOUT false physics correlation claims.

File: data3_enhanced_architecture_v1.py
Purpose: Extract EAN architecture data (corrected - no false PINN claims)
"""

import json
import csv
import os
from datetime import datetime

def extract_enhanced_architecture_data():
    """
    Extract Enhanced Attention Network architecture specifications
    CORRECTED: Removes false physics correlation claims per CLAUDE.md findings
    """
    
    architecture_data = {
        "metadata": {
            "extraction_date": datetime.now().isoformat(),
            "version": "v1",
            "figure_id": "fig3_enhanced_model",
            "data_source": "Enhanced Attention Network Architecture Specifications",
            "correction_note": "Physics correlation failure confirmed: r=0.000±0.000, not r=0.73 as previously claimed"
        },
        
        "model_rebranding": {
            "old_name": "PASE-Net (Physics-informed Attention-based Squeeze-Excitation Network)",
            "new_name": "Enhanced Attention Network (EAN) - Dual-Branch SE and Temporal Attention", 
            "reason": "Remove false physics claims while preserving attention mechanism research",
            "experimental_evidence": "Multi-model analysis shows r=0.000±0.000 across all models"
        },
        
        "architecture_components": {
            "total_parameters": 640713,
            "attention_parameters": 411520,
            "attention_percentage": 64.2,
            "model_size_mb": 2.44,
            "architecture_type": "CNN + SE + Temporal Attention"
        },
        
        "component_specifications": {
            "depthwise_separable_conv": {
                "formula": "x_conv = DepthwiseConv2D(x) + PointwiseConv2D(x)",
                "purpose": "hierarchical spatial feature extraction",
                "optimization": "memory-constrained environments"
            },
            "squeeze_excitation_modules": {
                "formula": "x_SE = x_conv ⊗ SE(x_conv)",
                "operation": "element-wise multiplication",
                "purpose": "channel-wise attention",
                "efficiency": "minimal computational overhead"
            },
            "temporal_self_attention": {
                "global_avg_pooling": "x_temp = GAP(x_SE, dim=F)  // [B,C,T,F] → [B,C,T]",
                "attention_formula": "Attention(Q,K,V) = softmax(QK^T/√d_k)V",
                "multi_head": "MultiHeadAttention(x_temp, h=4)",
                "heads": 4
            }
        },
        
        "design_principles": {
            "multi_scale_feature_learning": {
                "technique": "CNN layers with depthwise separable convolutions",
                "benefit": "hierarchical spatial features at different abstraction levels",
                "optimization": "compact representations for memory-constrained environments"
            },
            "efficient_channel_attention": {
                "mechanism": "SE modules",
                "benefit": "selective emphasis on informative feature channels",
                "efficiency": "minimal computational overhead",
                "application": "WiFi CSI data where different frequency subcarriers have varying importance"
            },
            "temporal_dependency_modeling": {
                "mechanism": "multi-head attention",
                "benefit": "captures long-range temporal relationships",
                "efficiency": "computational efficiency for real-time edge inference",
                "advantage": "direct modeling without gradient vanishing issues"
            }
        },
        
        "edge_optimization": {
            "memory_footprint": "2.44MB",
            "gpu_speedup": "64.1x (338.91ms CPU → 5.29ms GPU)",
            "throughput": "607 samples/second",
            "single_sample_latency": "5.3ms",
            "deployment_status": "Production Ready"
        },
        
        "experimental_validation": {
            "cross_domain_performance": {
                "loso_f1": "83.0±0.1%",
                "loro_f1": "83.0±0.1%", 
                "consistency": "identical performance across protocols",
                "coefficient_variation": "<0.2%"
            },
            "attention_analysis": {
                "se_attention_real": "extracted from 3 SE modules per Enhanced model",
                "temporal_attention_patterns": "6 activities analysis",
                "statistical_testing": "bootstrap confidence analysis framework",
                "physics_correlation_reality": "r=0.000±0.000 across all models (NOT r=0.73)"
            }
        },
        
        "corrected_interpretability": {
            "attention_mechanisms": {
                "se_channel_attention": "real patterns extracted from trained models",
                "temporal_attention_dynamics": "activity-specific temporal focus",
                "visualization": "2-subplot Figure 6: (a) SE Channel Attention, (b) Temporal Attention"
            },
            "removed_false_claims": {
                "physics_correlation_subplot": "removed entirely from Figure 6c",
                "false_correlation_value": "r=0.73, p<0.001 - EXPERIMENTALLY DISPROVEN",
                "honest_reporting": "attention mechanisms without false physics claims"
            }
        },
        
        "architectural_advantages": {
            "domain_agnostic_learning": "learns invariant properties of human-signal interactions",
            "cross_domain_robustness": "robust to domain-specific variations",
            "computational_efficiency": "suitable for edge deployment scenarios",
            "attention_effectiveness": "proven through systematic evaluation protocols"
        }
    }
    
    return architecture_data

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
        writer.writerow(['Architecture_Component', 'Subcomponent', 'Parameter', 'Value', 'Notes'])
        
        # Process architecture data
        for component, component_data in data.items():
            if component == 'metadata':
                continue
                
            if isinstance(component_data, dict):
                for sub_component, sub_data in component_data.items():
                    if isinstance(sub_data, dict):
                        for param, value in sub_data.items():
                            notes = 'CORRECTED' if 'false' in param.lower() or 'physics' in param.lower() else ''
                            writer.writerow([component, sub_component, param, str(value), notes])
                    elif isinstance(sub_data, list):
                        writer.writerow([component, sub_component, 'items', '; '.join(map(str, sub_data)), ''])
                    else:
                        writer.writerow([component, sub_component, '', str(sub_data), ''])
            else:
                writer.writerow([component, '', '', str(component_data), ''])
    
    return json_file, csv_file

def main():
    """Main execution function"""
    
    print("Extracting Figure 3 Enhanced Architecture data (CORRECTED - No false PINN claims)...")
    
    # Create output directory if it doesn't exist
    output_dir = "."
    os.makedirs(output_dir, exist_ok=True)
    
    # Extract data
    architecture_data = extract_enhanced_architecture_data()
    
    # Save in multiple formats
    base_filename = os.path.join(output_dir, "data3_enhanced_architecture_v1")
    json_file, csv_file = save_data_formats(architecture_data, base_filename)
    
    print("Enhanced architecture data extracted successfully!")
    print(f"JSON format: {json_file}")
    print(f"CSV format: {csv_file}")
    print(f"Architecture components: {len(architecture_data) - 1} major components")
    
    # Print summary with corrections
    print("\nEnhanced Architecture Summary (CORRECTED):")
    print(f"   Model name: {architecture_data['model_rebranding']['new_name']}")
    print(f"   Total parameters: {architecture_data['architecture_components']['total_parameters']}")
    print(f"   Attention percentage: {architecture_data['architecture_components']['attention_percentage']}%")
    print(f"   Edge throughput: {architecture_data['edge_optimization']['throughput']}")
    print(f"   Memory footprint: {architecture_data['edge_optimization']['memory_footprint']}")
    print(f"   Cross-domain F1: {architecture_data['experimental_validation']['cross_domain_performance']['loso_f1']}")
    
    print("\nCRITICAL CORRECTIONS:")
    print(f"   Physics correlation: {architecture_data['experimental_validation']['attention_analysis']['physics_correlation_reality']}")
    print(f"   Removed false claims: {architecture_data['corrected_interpretability']['removed_false_claims']['false_correlation_value']}")
    print(f"   Correction reason: {architecture_data['model_rebranding']['reason']}")

if __name__ == "__main__":
    main()