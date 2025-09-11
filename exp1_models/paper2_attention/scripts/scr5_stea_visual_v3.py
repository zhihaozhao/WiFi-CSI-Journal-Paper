#!/usr/bin/env python3
"""
Figure 5: STEA Sim2Real Transfer Efficiency - 3 Essential Visualizations
Redesigned subplot (c) with meaningful data visualization instead of text
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Scientific visualization configuration
plt.rcParams.update({
    'font.size': 11,
    'axes.titlesize': 13,
    'axes.labelsize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'axes.titleweight': 'bold'
})

# Strategy colors and styles
STRATEGY_CONFIG = {
    'zero_shot': {'color': '#E74C3C', 'linestyle': '--', 'marker': 's', 'label': 'Zero-Shot Baseline'},
    'linear_probe': {'color': '#F39C12', 'linestyle': '-.', 'marker': '^', 'label': 'Linear Probe'}, 
    'fine_tuning': {'color': '#2E86AB', 'linestyle': '-', 'marker': 'o', 'label': 'Full Fine-Tuning'}
}

def load_stea_data():
    """Load STEA experimental data"""
    data_path = os.path.join('..', 'plots', 'data5_stea_efficiency_v1.csv')
    
    if not os.path.exists(data_path):
        print(f"Error: STEA data file not found: {data_path}")
        print("Please run data5_stea_efficiency_v1.py first")
        return None
    
    df = pd.read_csv(data_path)
    print(f"Loaded STEA data: {df.shape}")
    return df

def create_transfer_strategy_comparison(ax, df):
    """Subplot A: Transfer Strategy Comparison - Core Scientific Question"""
    
    # Plot efficiency curves for each strategy
    for strategy in ['fine_tuning', 'linear_probe']:  # Skip zero-shot for main curves
        strategy_data = df[df['strategy'] == strategy].copy()
        
        if strategy_data.empty:
            continue
            
        strategy_data = strategy_data.sort_values('label_ratio')
        
        config = STRATEGY_CONFIG[strategy]
        
        # Plot main curve with error bars
        ax.errorbar(strategy_data['label_ratio'], strategy_data['macro_f1_mean'],
                   yerr=strategy_data['macro_f1_std'],
                   color=config['color'], linestyle=config['linestyle'], 
                   marker=config['marker'], markersize=8, linewidth=2.5,
                   capsize=4, capthick=2, alpha=0.9, label=config['label'])
    
    # Add zero-shot baseline as horizontal line
    zero_shot_data = df[df['strategy'] == 'zero_shot']
    if not zero_shot_data.empty:
        zero_shot_f1 = zero_shot_data['macro_f1_mean'].iloc[0]
        zero_shot_std = zero_shot_data['macro_f1_std'].iloc[0]
        ax.axhline(y=zero_shot_f1, color=STRATEGY_CONFIG['zero_shot']['color'], 
                  linestyle='--', linewidth=2.5, alpha=0.9,
                  label=STRATEGY_CONFIG['zero_shot']['label'])
        # Add uncertainty band for zero-shot
        ax.fill_between([0, 100], [zero_shot_f1-zero_shot_std]*2, 
                       [zero_shot_f1+zero_shot_std]*2, 
                       color=STRATEGY_CONFIG['zero_shot']['color'], alpha=0.2)
    
    # Add critical thresholds
    ax.axhline(y=80, color='gray', linestyle=':', alpha=0.7, linewidth=2,
               label='80\\% Deployment Threshold')
    
    # Highlight critical 20% label point
    critical_data = df[(df['strategy'] == 'fine_tuning') & (df['label_ratio'] == 20)]
    if not critical_data.empty:
        f1_at_20 = critical_data['macro_f1_mean'].iloc[0]
        ax.plot(20, f1_at_20, 'o', color='red', markersize=12, markerfacecolor='yellow',
               markeredgecolor='red', markeredgewidth=3, zorder=10)
    
    ax.set_xlabel('Labeled Data Percentage (\\%)', fontweight='bold')
    ax.set_ylabel('Macro-F1 Score (\\%)', fontweight='bold')  
    ax.set_title('(a) Transfer Strategy Effectiveness', fontweight='bold')
    ax.legend(loc='lower right', framealpha=0.9, fontsize=9)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(-2, 105)
    ax.set_ylim(10, 90)

def create_deployment_feasibility_analysis(ax, df):
    """Subplot B: Deployment Feasibility - Cost vs Performance"""
    
    # Focus on fine-tuning strategy for deployment analysis
    fine_tuning_data = df[df['strategy'] == 'fine_tuning'].copy()
    
    if fine_tuning_data.empty:
        ax.text(0.5, 0.5, 'Fine-tuning data not available', ha='center', va='center',
               transform=ax.transAxes, fontsize=14)
        return
    
    # Create deployment feasibility plot
    x = fine_tuning_data['annotation_cost_reduction']  # % cost saved
    y = fine_tuning_data['performance_retention']      # % performance retained
    labels = fine_tuning_data['label_ratio']          # for annotations
    
    # Create scatter plot with different colors for deployment readiness
    deployment_ready = fine_tuning_data['deployment_ready']
    
    # Plot deployment-ready points
    ready_mask = deployment_ready
    if ready_mask.any():
        ax.scatter(x[ready_mask], y[ready_mask], s=200, c='green', alpha=0.8, 
                  edgecolors='black', linewidth=2, marker='o', zorder=5,
                  label='Deployment Ready (≥80\\% F1)')
    
    # Plot not-ready points
    not_ready_mask = ~deployment_ready
    if not_ready_mask.any():
        ax.scatter(x[not_ready_mask], y[not_ready_mask], s=150, c='orange', alpha=0.8, 
                  edgecolors='black', linewidth=2, marker='s', zorder=5,
                  label='Development Stage')
    
    # Annotate key points with label ratios
    for _, row in fine_tuning_data.iterrows():
        if row['label_ratio'] in [1, 5, 20, 50, 100]:  # Key points only
            ax.annotate(f"{int(row['label_ratio'])}\\%", 
                       xy=(row['annotation_cost_reduction'], row['performance_retention']),
                       xytext=(8, 8), textcoords='offset points',
                       fontsize=9, fontweight='bold',
                       bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.8),
                       ha='center')
    
    # Add reference lines
    ax.axvline(x=80, color='red', linestyle='--', alpha=0.7, linewidth=2,
              label='80\\% Cost Reduction Target')
    ax.axhline(y=95, color='blue', linestyle='--', alpha=0.7, linewidth=2,
              label='95\\% Performance Retention')
    
    ax.set_xlabel('Annotation Cost Reduction (\\%)', fontweight='bold')
    ax.set_ylabel('Performance Retention (\\% of Full Supervision)', fontweight='bold')
    ax.set_title('(b) Cost-Performance Trade-off', fontweight='bold')
    ax.legend(loc='lower left', framealpha=0.9, fontsize=9)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 100)
    ax.set_ylim(35, 105)

def create_transfer_efficiency_analysis(ax, df):
    """Subplot C: Transfer Efficiency Analysis - Learning Rate Comparison"""
    
    # Calculate transfer efficiency metrics
    strategies = ['linear_probe', 'fine_tuning']
    efficiency_data = []
    
    # Get zero-shot baseline
    zero_shot_data = df[df['strategy'] == 'zero_shot']
    zero_shot_f1 = zero_shot_data['macro_f1_mean'].iloc[0] if not zero_shot_data.empty else 15.0
    
    for strategy in strategies:
        strategy_data = df[df['strategy'] == strategy].copy()
        strategy_data = strategy_data.sort_values('label_ratio')
        
        for _, row in strategy_data.iterrows():
            if row['label_ratio'] > 0:  # Skip 0% labels
                # Calculate efficiency: (F1_gain / labels_used)
                f1_gain = row['macro_f1_mean'] - zero_shot_f1
                efficiency = f1_gain / row['label_ratio']
                
                efficiency_data.append({
                    'label_ratio': row['label_ratio'],
                    'strategy': strategy,
                    'efficiency': efficiency,
                    'f1_gain': f1_gain,
                    'macro_f1': row['macro_f1_mean']
                })
    
    efficiency_df = pd.DataFrame(efficiency_data)
    
    # Create grouped bar chart showing efficiency at different label ratios
    label_ratios = sorted(efficiency_df['label_ratio'].unique())
    x = np.arange(len(label_ratios))
    width = 0.35
    
    linear_efficiencies = []
    fine_tune_efficiencies = []
    
    for ratio in label_ratios:
        linear_data = efficiency_df[(efficiency_df['strategy'] == 'linear_probe') & 
                                  (efficiency_df['label_ratio'] == ratio)]
        fine_data = efficiency_df[(efficiency_df['strategy'] == 'fine_tuning') & 
                                (efficiency_df['label_ratio'] == ratio)]
        
        linear_eff = linear_data['efficiency'].iloc[0] if not linear_data.empty else 0
        fine_eff = fine_data['efficiency'].iloc[0] if not fine_data.empty else 0
        
        linear_efficiencies.append(linear_eff)
        fine_tune_efficiencies.append(fine_eff)
    
    # Create grouped bars
    bars1 = ax.bar(x - width/2, linear_efficiencies, width, 
                   color=STRATEGY_CONFIG['linear_probe']['color'], alpha=0.8,
                   label='Linear Probe Efficiency', edgecolor='black', linewidth=1)
    
    bars2 = ax.bar(x + width/2, fine_tune_efficiencies, width,
                   color=STRATEGY_CONFIG['fine_tuning']['color'], alpha=0.8,
                   label='Fine-Tuning Efficiency', edgecolor='black', linewidth=1)
    
    # Add value annotations on bars
    for i, (bar1, bar2) in enumerate(zip(bars1, bars2)):
        # Annotate linear probe efficiency
        ax.text(bar1.get_x() + bar1.get_width()/2., bar1.get_height() + 0.02,
               f'{linear_efficiencies[i]:.1f}', ha='center', va='bottom',
               fontsize=8, fontweight='bold')
        
        # Annotate fine-tuning efficiency  
        ax.text(bar2.get_x() + bar2.get_width()/2., bar2.get_height() + 0.02,
               f'{fine_tune_efficiencies[i]:.1f}', ha='center', va='bottom',
               fontsize=8, fontweight='bold')
    
    # Highlight most efficient point
    max_efficiency_idx = np.argmax(fine_tune_efficiencies)
    max_ratio = label_ratios[max_efficiency_idx]
    max_eff = fine_tune_efficiencies[max_efficiency_idx]
    
    # Add annotation for peak efficiency
    ax.annotate(f'Peak Efficiency\\n{max_ratio}\\% labels\\n{max_eff:.1f} F1/\\%', 
               xy=(max_efficiency_idx + width/2, max_eff), 
               xytext=(max_efficiency_idx + width/2, max_eff + 0.5),
               arrowprops=dict(arrowstyle='->', color='red', lw=2),
               ha='center', va='bottom', fontsize=9, fontweight='bold',
               bbox=dict(boxstyle="round,pad=0.3", facecolor='yellow', alpha=0.8))
    
    ax.set_xlabel('Label Percentage (\\%)', fontweight='bold')
    ax.set_ylabel('Transfer Efficiency (F1 Gain per \\% Labels)', fontweight='bold')
    ax.set_title('(c) Transfer Learning Efficiency Comparison', fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels([f'{int(ratio)}\\%' for ratio in label_ratios])
    ax.legend(loc='upper right', framealpha=0.9)
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_ylim(0, max(max(linear_efficiencies), max(fine_tune_efficiencies)) * 1.2)

def main():
    """Create essential STEA figure with meaningful visualizations"""
    
    print("=" * 70)
    print("Figure 5: STEA with 3 Essential Data Visualizations")
    print("Redesigned subplot (c) with transfer efficiency analysis")
    print("=" * 70)
    
    # Load data  
    df = load_stea_data()
    if df is None:
        return
    
    # Create comprehensive figure with 3 meaningful visualizations
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))
    
    # Generate scientific visualizations
    create_transfer_strategy_comparison(ax1, df)
    create_deployment_feasibility_analysis(ax2, df)
    create_transfer_efficiency_analysis(ax3, df)
    
    # Main title
    fig.suptitle('Figure 5: STEA Sim2Real Transfer Efficiency Assessment', 
                 fontsize=16, fontweight='bold', y=0.95)
    
    # Adjust layout
    plt.tight_layout()
    plt.subplots_adjust(top=0.88, wspace=0.25)
    
    # Save figure
    output_path = os.path.join('..', 'plots', 'fig5_stea_visual_v3.pdf')
    plt.savefig(output_path, dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print(f"STEA Figure 5 with visualizations saved: {output_path}")
    
    # PNG version
    png_path = os.path.join('..', 'plots', 'fig5_stea_visual_v3.png')
    plt.savefig(png_path, dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print(f"PNG version saved: {png_path}")
    
    print("STEA Figure 5 with meaningful visualizations completed!")
    print("Subplot (a): Transfer strategy effectiveness curves")
    print("Subplot (b): Cost-performance deployment analysis")  
    print("Subplot (c): Transfer efficiency comparison (F1 gain per % labels)")

if __name__ == "__main__":
    main()