#!/usr/bin/env python3
"""
Figure 4: CDAE Cross-Domain Adaptation Analysis - Enhanced Version
Solving all visualization issues for SCI journal standards
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Scientific visualization configuration  
plt.rcParams.update({
    'font.size': 10,
    'axes.titlesize': 12,
    'axes.labelsize': 11,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'axes.titleweight': 'bold'
})

# Consistent model configuration
MODEL_ORDER = ['enhanced', 'cnn', 'bilstm', 'conformer']
MODEL_NAMES = {'enhanced': 'PASE-Net', 'cnn': 'CNN', 'bilstm': 'BiLSTM', 'conformer': 'Conformer'}
MODEL_COLORS = ['#2E86AB', '#A23B72', '#F18F01', '#E74C3C']

def load_experimental_data():
    """Load authentic CDAE experimental data"""
    
    summary_path = os.path.join('..', 'plots', 'data4_crossdomain_v4.csv')
    if not os.path.exists(summary_path):
        print(f"Error: CDAE data file not found: {summary_path}")
        return None
    
    df_summary = pd.read_csv(summary_path)
    print("Loaded CDAE data successfully")
    return df_summary

def create_enhanced_performance_comparison(ax, df_summary):
    """Enhanced performance comparison with pattern fills"""
    
    # Reorder data consistently
    df_ordered = df_summary.set_index('model').loc[MODEL_ORDER].reset_index()
    
    x = np.arange(len(MODEL_ORDER))
    width = 0.35
    
    # Get data
    loso_means = df_ordered['loso_mean'].values
    loro_means = df_ordered['loro_mean'].values
    loso_stds = df_ordered['loso_std'].values
    loro_stds = df_ordered['loro_std'].values
    
    # Handle Conformer outlier statistically - cap visualization but show annotation
    loso_display = loso_means.copy()
    loso_display[loso_display < 50] = 45  # Cap outlier for visualization
    
    # Create bars with different patterns
    bars1 = ax.bar(x - width/2, loso_display, width, 
                   yerr=[min(s, 5) for s in loso_stds], 
                   color=MODEL_COLORS, alpha=0.8, 
                   hatch='///', edgecolor='black', linewidth=1,
                   label='LOSO', capsize=3)
    
    bars2 = ax.bar(x + width/2, loro_means, width,
                   yerr=loro_stds,
                   color=MODEL_COLORS, alpha=0.6,
                   hatch='...', edgecolor='black', linewidth=1, 
                   label='LORO', capsize=3)
    
    # Add original values as annotations
    for i, (bar1, bar2) in enumerate(zip(bars1, bars2)):
        # Use original values for annotations
        ax.text(bar1.get_x() + bar1.get_width()/2., 
               max(bar1.get_height() + 2, 48),
               f'{loso_means[i]:.1f}%', ha='center', va='bottom', 
               fontsize=8, weight='bold')
        ax.text(bar2.get_x() + bar2.get_width()/2., bar2.get_height() + 1,
               f'{loro_means[i]:.1f}%', ha='center', va='bottom', 
               fontsize=8, weight='bold')
    
    # Special annotation for Conformer failure
    if loso_means[3] < 50:
        ax.annotate('Convergence\nFailure', 
                   xy=(x[3] - width/2, 45), xytext=(x[3] - width/2, 35),
                   arrowprops=dict(arrowstyle='->', color='red', lw=2),
                   ha='center', va='top', fontsize=9, weight='bold', color='red',
                   bbox=dict(boxstyle="round,pad=0.3", facecolor='pink', alpha=0.8))
    
    ax.set_xlabel('Model Architectures', fontweight='bold')
    ax.set_ylabel('Cross-Domain Performance (%)', fontweight='bold')
    ax.set_title('(a) Cross-Domain Performance Analysis', fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels([MODEL_NAMES[model] for model in MODEL_ORDER])
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_ylim(0, 90)

def create_domain_gap_analysis(ax, df_summary):
    """Domain gap analysis with statistical treatment"""
    
    df_ordered = df_summary.set_index('model').loc[MODEL_ORDER].reset_index()
    domain_gaps = df_ordered['domain_gap'].values
    
    # Separate normal models from outlier
    normal_gaps = domain_gaps[:3]  
    outlier_gap = domain_gaps[3]
    
    # Create split visualization
    x_normal = np.arange(3)
    x_outlier = [4]  # Separate position
    
    # Normal models
    bars_normal = ax.bar(x_normal, normal_gaps, color=MODEL_COLORS[:3], 
                        alpha=0.8, edgecolor='black', linewidth=1)
    
    # Outlier with different scale indication
    bars_outlier = ax.bar(x_outlier, [min(outlier_gap, 15)], color=MODEL_COLORS[3], 
                         alpha=0.8, edgecolor='red', linewidth=2,
                         hatch='xxx')
    
    # Add value annotations
    for i, bar in enumerate(bars_normal):
        ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.2,
               f'{normal_gaps[i]:.1f}%', ha='center', va='bottom', 
               fontsize=9, weight='bold')
    
    # Special annotation for outlier
    ax.text(4, min(outlier_gap, 15) + 1, f'{outlier_gap:.1f}%\n(Scale Break)', 
           ha='center', va='bottom', fontsize=9, weight='bold', color='red',
           bbox=dict(boxstyle="round,pad=0.3", facecolor='yellow', alpha=0.8))
    
    # Reference lines
    ax.axhline(y=1, color='green', linestyle='--', alpha=0.7, label='Excellent (<1%)')
    ax.axhline(y=5, color='orange', linestyle='--', alpha=0.7, label='Acceptable (<5%)')
    
    ax.set_xlabel('Model Architectures', fontweight='bold')
    ax.set_ylabel('LOSO-LORO Domain Gap (%)', fontweight='bold')
    ax.set_title('(b) Domain Gap Analysis with Outlier Treatment', fontweight='bold')
    ax.set_xticks(list(x_normal) + x_outlier)
    ax.set_xticklabels([MODEL_NAMES[MODEL_ORDER[i]] for i in range(4)])
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_ylim(0, 16)

def create_stability_comparison(ax, df_summary):
    """Stability comparison with coefficient of variation"""
    
    df_ordered = df_summary.set_index('model').loc[MODEL_ORDER].reset_index()
    
    # Calculate coefficient of variation for stability metric
    cv_loso = (df_ordered['loso_std'] / df_ordered['loso_mean'] * 100).values
    cv_loro = (df_ordered['loro_std'] / df_ordered['loro_mean'] * 100).values
    
    # Handle outlier
    cv_loso[cv_loso > 50] = 50  # Cap outlier visualization
    
    x = np.arange(len(MODEL_ORDER))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, cv_loso, width, color=MODEL_COLORS, 
                  alpha=0.8, hatch='|||', edgecolor='black', linewidth=1,
                  label='LOSO CV%')
    bars2 = ax.bar(x + width/2, cv_loro, width, color=MODEL_COLORS,
                  alpha=0.6, hatch='---', edgecolor='black', linewidth=1,
                  label='LORO CV%')
    
    # Add annotations
    for i, (bar1, bar2) in enumerate(zip(bars1, bars2)):
        ax.text(bar1.get_x() + bar1.get_width()/2., bar1.get_height() + 0.5,
               f'{cv_loso[i]:.1f}%', ha='center', va='bottom', 
               fontsize=8, weight='bold')
        ax.text(bar2.get_x() + bar2.get_width()/2., bar2.get_height() + 0.5,
               f'{cv_loro[i]:.1f}%', ha='center', va='bottom', 
               fontsize=8, weight='bold')
    
    # Reference line for stability threshold
    ax.axhline(y=5, color='red', linestyle='--', alpha=0.7, 
               label='Instability Threshold (5%)')
    
    ax.set_xlabel('Model Architectures', fontweight='bold')
    ax.set_ylabel('Coefficient of Variation (%)', fontweight='bold')
    ax.set_title('(c) Cross-Domain Stability Analysis', fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels([MODEL_NAMES[model] for model in MODEL_ORDER])
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_ylim(0, 55)

def main():
    """Create enhanced CDAE figure"""
    
    print("=" * 60)
    print("Enhanced Figure 4: CDAE Cross-Domain Analysis")
    print("Solving visualization issues for SCI standards")
    print("=" * 60)
    
    # Load data
    df_summary = load_experimental_data()
    if df_summary is None:
        return
    
    # Create figure
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))
    
    # Generate subplots
    create_enhanced_performance_comparison(ax1, df_summary)
    create_domain_gap_analysis(ax2, df_summary) 
    create_stability_comparison(ax3, df_summary)
    
    # Main title
    fig.suptitle('Figure 4: CDAE Cross-Domain Adaptation Analysis', 
                 fontsize=16, fontweight='bold', y=0.95)
    
    # Adjust layout
    plt.tight_layout()
    plt.subplots_adjust(top=0.85)
    
    # Save figure
    output_path = os.path.join('..', 'plots', 'fig4_cdae_enhanced_v5.pdf')
    plt.savefig(output_path, dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print(f"Enhanced Figure 4 saved: {output_path}")
    
    # PNG version
    png_path = os.path.join('..', 'plots', 'fig4_cdae_enhanced_v5.png')
    plt.savefig(png_path, dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print(f"PNG version saved: {png_path}")
    
    print("CDAE Figure 4 enhancement completed!")

if __name__ == "__main__":
    main()