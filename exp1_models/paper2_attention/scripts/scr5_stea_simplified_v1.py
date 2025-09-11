#!/usr/bin/env python3
"""
Figure 5: STEA Sim2Real Transfer Efficiency - Simplified 2-Subplot Design
Eliminates redundancy and focuses on core STEA insights
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
    'zero_shot': {'color': '#E74C3C', 'linestyle': '--', 'marker': 's', 'label': 'Zero-Shot'},
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

def create_label_efficiency_curve(ax, df):
    """Subplot A: Label Efficiency Curve - Core STEA Analysis"""
    
    # Plot efficiency curves for each strategy
    for strategy in ['zero_shot', 'linear_probe', 'fine_tuning']:
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
    
    # Add critical thresholds and annotations
    # 80% deployment threshold
    ax.axhline(y=80, color='gray', linestyle=':', alpha=0.7, linewidth=2,
               label='80% Deployment Threshold')
    
    # Highlight critical 20% label point
    fine_tuning_20 = df[(df['strategy'] == 'fine_tuning') & (df['label_ratio'] == 20)]
    if not fine_tuning_20.empty:
        f1_at_20 = fine_tuning_20['macro_f1_mean'].iloc[0]
        ax.plot(20, f1_at_20, 'o', color='red', markersize=12, markerfacecolor='yellow',
               markeredgecolor='red', markeredgewidth=3, zorder=10)
        ax.annotate(f'Critical Point\\n20% labels → {f1_at_20}% F1\\n98.6% retention', 
                   xy=(20, f1_at_20), xytext=(35, f1_at_20-8),
                   arrowprops=dict(arrowstyle='->', color='red', lw=2),
                   fontsize=10, fontweight='bold', ha='center',
                   bbox=dict(boxstyle="round,pad=0.3", facecolor='lightyellow', alpha=0.9))
    
    # Full supervision reference
    full_sup = df[(df['strategy'] == 'fine_tuning') & (df['label_ratio'] == 100)]
    if not full_sup.empty:
        f1_full = full_sup['macro_f1_mean'].iloc[0]
        ax.axhline(y=f1_full, color='green', linestyle=':', alpha=0.7, linewidth=2,
                  label=f'Full Supervision ({f1_full}%)')
    
    ax.set_xlabel('Labeled Data Percentage (\\%)', fontweight='bold')
    ax.set_ylabel('Macro-F1 Score (\\%)', fontweight='bold')  
    ax.set_title('(a) STEA Label Efficiency Analysis', fontweight='bold')
    ax.legend(loc='lower right', framealpha=0.9)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(-2, 105)
    ax.set_ylim(10, 90)
    
    # Add efficiency phases annotations
    ax.annotate('Bootstrap\\nPhase', xy=(3, 25), xytext=(3, 35),
               arrowprops=dict(arrowstyle='->', alpha=0.6),
               fontsize=9, ha='center', alpha=0.7,
               bbox=dict(boxstyle="round,pad=0.2", facecolor='lightblue', alpha=0.7))
    
    ax.annotate('Steep\\nImprovement', xy=(12.5, 55), xytext=(12.5, 45),
               arrowprops=dict(arrowstyle='->', alpha=0.6),
               fontsize=9, ha='center', alpha=0.7,
               bbox=dict(boxstyle="round,pad=0.2", facecolor='lightgreen', alpha=0.7))
    
    ax.annotate('Saturation\\nPhase', xy=(75, 83), xytext=(75, 75),
               arrowprops=dict(arrowstyle='->', alpha=0.6),
               fontsize=9, ha='center', alpha=0.7,
               bbox=dict(boxstyle="round,pad=0.2", facecolor='lightyellow', alpha=0.7))

def create_cost_benefit_analysis(ax, df):
    """Subplot B: Cost-Benefit Analysis - STEA Deployment Insights"""
    
    # Focus on fine-tuning strategy for cost-benefit analysis
    fine_tuning_data = df[df['strategy'] == 'fine_tuning'].copy()
    
    if fine_tuning_data.empty:
        ax.text(0.5, 0.5, 'Fine-tuning data not available', ha='center', va='center',
               transform=ax.transAxes, fontsize=14)
        return
    
    # Create cost-benefit scatter plot
    x = fine_tuning_data['annotation_cost_reduction']  # % cost saved
    y = fine_tuning_data['performance_retention']      # % performance retained
    sizes = fine_tuning_data['label_ratio'] * 5       # Size proportional to label ratio
    
    # Color by efficiency score
    colors = fine_tuning_data['efficiency_score']
    
    scatter = ax.scatter(x, y, s=sizes, c=colors, cmap='RdYlGn', alpha=0.8, 
                        edgecolors='black', linewidth=1.5, zorder=5)
    
    # Add colorbar for efficiency score
    cbar = plt.colorbar(scatter, ax=ax, shrink=0.8)
    cbar.set_label('Efficiency Score\\n(F1 gain per \\% labels)', rotation=90, va='bottom')
    
    # Annotate key points
    for _, row in fine_tuning_data.iterrows():
        if row['label_ratio'] in [20, 100]:  # Key points only
            ax.annotate(f"{int(row['label_ratio'])}\\% labels\\n{row['macro_f1_mean']}\\% F1", 
                       xy=(row['annotation_cost_reduction'], row['performance_retention']),
                       xytext=(10, 10), textcoords='offset points',
                       fontsize=9, fontweight='bold',
                       bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8),
                       arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.2'))
    
    # Highlight optimal region (Pareto frontier)
    optimal_mask = (x >= 50) & (y >= 95)  # High cost reduction + high performance retention
    if optimal_mask.any():
        ax.fill_between([50, 100], [95, 95], [100, 100], alpha=0.2, color='green',
                       label='Optimal Region')
    
    # Add reference lines
    ax.axvline(x=80, color='red', linestyle='--', alpha=0.7, linewidth=2,
              label='80\\% Cost Reduction Target')
    ax.axhline(y=95, color='blue', linestyle='--', alpha=0.7, linewidth=2,
              label='95\\% Performance Retention')
    
    # Highlight the critical 20% point (80% cost reduction, 98.6% retention)
    critical_point = fine_tuning_data[fine_tuning_data['label_ratio'] == 20]
    if not critical_point.empty:
        ax.plot(critical_point['annotation_cost_reduction'].iloc[0], 
               critical_point['performance_retention'].iloc[0],
               'o', color='red', markersize=15, markerfacecolor='gold',
               markeredgecolor='red', markeredgewidth=3, zorder=10,
               label='Optimal Trade-off Point')
    
    ax.set_xlabel('Annotation Cost Reduction (\\%)', fontweight='bold')
    ax.set_ylabel('Performance Retention (\\% of Full Supervision)', fontweight='bold')
    ax.set_title('(b) Cost-Benefit Analysis for Deployment', fontweight='bold')
    ax.legend(loc='lower left', framealpha=0.9, fontsize=9)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 100)
    ax.set_ylim(40, 105)
    
    # Add deployment recommendation
    ax.text(0.95, 0.05, 'Recommendation:\\n20\\% labels achieve\\n98.6\\% performance\\nwith 80\\% cost savings', 
           transform=ax.transAxes, ha='right', va='bottom', fontsize=10,
           bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgreen', alpha=0.8))

def main():
    """Create simplified 2-subplot STEA figure"""
    
    print("=" * 60)
    print("Figure 5: STEA Sim2Real Transfer Efficiency - Simplified Design")
    print("2 essential subplots eliminating redundancy")
    print("=" * 60)
    
    # Load data  
    df = load_stea_data()
    if df is None:
        return
    
    # Create simplified figure with 2 subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    
    # Generate optimized visualizations
    create_label_efficiency_curve(ax1, df)
    create_cost_benefit_analysis(ax2, df)
    
    # Main title
    fig.suptitle('Figure 5: STEA Sim2Real Transfer Efficiency Analysis', 
                 fontsize=16, fontweight='bold', y=0.95)
    
    # Adjust layout
    plt.tight_layout()
    plt.subplots_adjust(top=0.88, wspace=0.25)
    
    # Save figure
    output_path = os.path.join('..', 'plots', 'fig5_stea_simplified_v1.pdf')
    plt.savefig(output_path, dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print(f"Simplified STEA Figure 5 saved: {output_path}")
    
    # PNG version
    png_path = os.path.join('..', 'plots', 'fig5_stea_simplified_v1.png')
    plt.savefig(png_path, dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print(f"PNG version saved: {png_path}")
    
    print("\\nSimplified STEA Figure 5 completed!")
    print("✓ Eliminated redundant subplots (b) and (d)")
    print("✓ Combined core insights into 2 essential visualizations")
    print("✓ Added deployment recommendations and critical point annotations")

if __name__ == "__main__":
    main()