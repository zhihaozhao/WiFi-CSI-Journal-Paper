#!/usr/bin/env python3
"""
Figure 1: System Architecture Overview
Enhanced Attention Network Synthetic WiFi CSI Data Generation Framework
IEEE IoTJ Paper - WiFi CSI HAR (CORRECTED - No false PINN claims)
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch, Rectangle
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
from pathlib import Path

# Set publication-ready style
# plt.style.use('seaborn-v0_8-paper')  # Commented out for compatibility

# Configure for IEEE IoTJ standards
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman'],
    'font.size': 12,
    'axes.labelsize': 13,
    'axes.titlesize': 15,
    'xtick.labelsize': 11,
    'ytick.labelsize': 11,
    'legend.fontsize': 11,
    'figure.titlesize': 16,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.1
})

def create_rounded_box(ax, xy, width, height, label, color, text_color='black', fontsize=12):
    """Create a rounded rectangle with text"""
    box = FancyBboxPatch(
        xy, width, height,
        boxstyle="round,pad=0.02",
        facecolor=color,
        edgecolor='black',
        linewidth=1.5,
        alpha=0.8
    )
    ax.add_patch(box)
    
    # Add text in the center
    center_x = xy[0] + width/2
    center_y = xy[1] + height/2
    ax.text(center_x, center_y, label, 
           ha='center', va='center', 
           fontsize=fontsize, fontweight='bold',
           color=text_color, wrap=True)
    
    return box

def create_arrow(ax, start, end, color='black', width=2):
    """Create an arrow between two points"""
    arrow = ConnectionPatch(start, end, "data", "data",
                          arrowstyle="->", shrinkA=5, shrinkB=5,
                          mutation_scale=20, fc=color, ec=color, linewidth=width)
    ax.add_patch(arrow)
    return arrow

def create_system_architecture():
    """
    Create comprehensive system architecture diagram
    """
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # Define colors for different components
    colors = {
        'input': '#E8F4FD',        # Light blue
        'physics': '#D4EDDA',      # Light green  
        'synthesis': '#FFF3CD',    # Light yellow
        'model': '#F8D7DA',        # Light red
        'evaluation': '#E2E3E5',   # Light gray
        'output': '#D1ECF1'        # Light cyan
    }
    
    # Title
    ax.text(7, 9.5, 'Physics-Guided Synthetic WiFi CSI Data Generation Framework', 
           ha='center', va='center', fontsize=18, fontweight='bold')
    
    # === Input Data Layer ===
    create_rounded_box(ax, (0.5, 8), 2.5, 0.8, 
                      'Real WiFi CSI\nBenchmark Data\n(SenseFi)', 
                      colors['input'], fontsize=12)
    
    # === Physics Modeling Layer ===
    ax.text(1, 7.5, 'Physics Modeling Layer', fontsize=14, fontweight='bold', color='darkgreen')
    
    # Multipath Effects
    create_rounded_box(ax, (0.2, 6.5), 1.8, 0.6, 
                      'Multipath\nPropagation', 
                      colors['physics'], fontsize=12)
    
    # Human Body Interaction
    create_rounded_box(ax, (2.2, 6.5), 1.8, 0.6, 
                      'Human Body\nInteraction', 
                      colors['physics'], fontsize=12)
    
    # Environmental Variations
    create_rounded_box(ax, (4.2, 6.5), 1.8, 0.6, 
                      'Environmental\nVariations', 
                      colors['physics'], fontsize=12)
    
    # === Synthetic Data Generation ===
    create_rounded_box(ax, (2.5, 5), 3, 0.8, 
                      'Physics-Guided\nSynthetic CSI Generator\n(Parameterized)', 
                      colors['synthesis'], fontsize=13)
    
    # Generated datasets
    create_rounded_box(ax, (0.5, 3.8), 1.5, 0.6, 
                      'Synthetic\nRobustness (540)', 
                      colors['synthesis'], fontsize=11)
    
    create_rounded_box(ax, (2.2, 3.8), 1.5, 0.6, 
                      'CDAE Protocol\n40 Configs', 
                      colors['synthesis'], fontsize=11)
    
    create_rounded_box(ax, (3.9, 3.8), 1.5, 0.6, 
                      'STEA Protocol\n56 Configs', 
                      colors['synthesis'], fontsize=11)
    
    # === Model Architecture ===
    ax.text(8.5, 8.5, 'Enhanced Model Architecture', fontsize=14, fontweight='bold', color='darkred')
    
    # CNN Feature Extraction (left)
    create_rounded_box(ax, (7, 7.8), 1.8, 0.5, 
                      'CNN Feature\nExtraction', 
                      colors['model'], fontsize=11)
    
    # SE Module (middle)
    create_rounded_box(ax, (9.2, 7.8), 1.8, 0.5, 
                      'Squeeze-Excitation\nModule', 
                      colors['model'], fontsize=11)
    
    # Temporal Attention (right)
    create_rounded_box(ax, (11.4, 7.8), 2, 0.5, 
                      'Temporal Self-Attention\nMechanism', 
                      colors['model'], fontsize=11)
    
    # Enhanced Model Architecture Container (bottom, non-overlapping)
    create_rounded_box(ax, (7, 7), 6.5, 0.6, 
                      'Enhanced Attention Network (EAN): CNN + SE + Temporal Attention', 
                      colors['model'], fontsize=12)
    
    # === Sim2Real Transfer Learning ===
    create_rounded_box(ax, (7, 6), 4, 0.6, 
                      'Sim2Real Transfer Learning\n(Zero-shot, Linear Probe, Fine-tune, Temp Scaling)', 
                      colors['model'], fontsize=11)
    
    # === Trustworthy Evaluation ===
    ax.text(8.5, 5, 'Trustworthy Evaluation Protocols', fontsize=14, fontweight='bold', color='darkslategray')
    
    # Calibration Analysis
    create_rounded_box(ax, (6.5, 4.2), 1.8, 0.5, 
                      'Calibration\nAnalysis (ECE)', 
                      colors['evaluation'], fontsize=11)
    
    # Cross-Domain Robustness
    create_rounded_box(ax, (8.5, 4.2), 2, 0.5, 
                      'Cross-Domain\nRobustness', 
                      colors['evaluation'], fontsize=11)
    
    # Statistical Significance
    create_rounded_box(ax, (10.8, 4.2), 1.8, 0.5, 
                      'Statistical\nSignificance', 
                      colors['evaluation'], fontsize=11)
    
    # === Output Results ===
    create_rounded_box(ax, (4, 3.2), 6, 0.8, 
                      'Key Results: 83.0±0.1% F1 Cross-Domain Consistency\n82.1% F1 @ 20% Labels (80% Cost Reduction)', 
                      colors['output'], fontsize=13)
    
    # === Add Arrows ===
    # Input to physics modeling
    create_arrow(ax, (1.75, 8), (3, 7.1), color='blue', width=2)
    
    # Physics components to generator
    create_arrow(ax, (1.1, 6.5), (3.5, 5.8), color='green', width=1.5)
    create_arrow(ax, (3.1, 6.5), (4, 5.8), color='green', width=1.5)
    create_arrow(ax, (5.1, 6.5), (4.5, 5.8), color='green', width=1.5)
    
    # Generator to datasets
    create_arrow(ax, (3.2, 5), (1.2, 4.4), color='orange', width=1.5)
    create_arrow(ax, (4, 5), (2.9, 4.4), color='orange', width=1.5)
    create_arrow(ax, (4.8, 5), (4.6, 4.4), color='orange', width=1.5)
    
    # Real data and synthetic to model
    create_arrow(ax, (2.5, 8), (8.5, 7.3), color='purple', width=2)
    create_arrow(ax, (5.5, 4.1), (7.5, 5.2), color='orange', width=2)
    
    # Model components flow
    create_arrow(ax, (8.4, 6.8), (8.8, 6.5), color='red', width=1.5)
    create_arrow(ax, (10.4, 6.8), (10.8, 6.5), color='red', width=1.5)
    create_arrow(ax, (9.5, 6), (9, 5.3), color='red', width=2)
    
    # Transfer to evaluation
    create_arrow(ax, (9, 4.5), (9, 3.3), color='darkred', width=2)
    
    # Evaluation to results
    create_arrow(ax, (9, 2.8), (7, 2.3), color='darkslategray', width=2)
    
    # === Add Legend ===
    legend_elements = [
        mpatches.Rectangle((0, 0), 1, 1, facecolor=colors['input'], label='Input Data'),
        mpatches.Rectangle((0, 0), 1, 1, facecolor=colors['physics'], label='Physics Modeling'),
        mpatches.Rectangle((0, 0), 1, 1, facecolor=colors['synthesis'], label='Data Synthesis'),
        mpatches.Rectangle((0, 0), 1, 1, facecolor=colors['model'], label='Model Architecture'),
        mpatches.Rectangle((0, 0), 1, 1, facecolor=colors['evaluation'], label='Evaluation'),
        mpatches.Rectangle((0, 0), 1, 1, facecolor=colors['output'], label='Results')
    ]
    
    ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.98, 0.98), 
             framealpha=0.9, fontsize=11)
    
    # === Add Key Innovation Highlights ===
    # Highlight box for key innovations
    highlight_box = Rectangle((6.5, 6.5), 7.5, 1.5, 
                            linewidth=3, edgecolor='gold', 
                            facecolor='none', linestyle='--', alpha=0.8)
    ax.add_patch(highlight_box)
    
    ax.text(10.2, 8.1, '🔥 Key Innovations', fontsize=13, fontweight='bold', 
           color='darkorange', ha='center')
    
    # Performance metrics box
    perf_box = Rectangle((3.5, 1), 7, 1.3, 
                        linewidth=2, edgecolor='darkblue', 
                        facecolor='none', linestyle='-', alpha=0.6)
    ax.add_patch(perf_box)
    
    # Set axis properties
    ax.set_xlim(0, 14)
    ax.set_ylim(0.5, 10)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Add subtle grid for better organization
    for i in range(1, 14):
        ax.axvline(x=i, color='lightgray', alpha=0.3, linewidth=0.5)
    for i in range(1, 10):
        ax.axhline(y=i, color='lightgray', alpha=0.3, linewidth=0.5)
    
    plt.tight_layout()
    
    return fig, ax

def create_detailed_data_flow():
    """
    Create detailed data flow diagram
    """
    fig, ax = plt.subplots(figsize=(12, 8))
    
    ax.text(6, 7.5, 'Detailed Data Flow and Processing Pipeline', 
           ha='center', va='center', fontsize=14, fontweight='bold')
    
    # Data flow stages
    stages = [
        {'pos': (1, 6.5), 'size': (2, 0.6), 'label': 'Raw CSI Data\nCollection', 'color': '#E8F4FD'},
        {'pos': (1, 5.5), 'size': (2, 0.6), 'label': 'Preprocessing &\nNormalization', 'color': '#D4EDDA'},
        {'pos': (1, 4.5), 'size': (2, 0.6), 'label': 'Physics Parameter\nExtraction', 'color': '#FFF3CD'},
        {'pos': (4.5, 6), 'size': (3, 0.8), 'label': 'Synthetic Data Generation\n(Multi-Parameter Control)', 'color': '#F8D7DA'},
        {'pos': (4.5, 4.5), 'size': (3, 0.8), 'label': 'Enhanced Model Training\n(CNN+SE+Attention)', 'color': '#E2E3E5'},
        {'pos': (9, 6), 'size': (2.5, 0.8), 'label': 'Cross-Domain\nEvaluation', 'color': '#D1ECF1'},
        {'pos': (9, 4.5), 'size': (2.5, 0.8), 'label': 'Transfer Learning\n(Sim2Real)', 'color': '#F0D0D0'}
    ]
    
    # Create boxes and arrows
    for i, stage in enumerate(stages):
        create_rounded_box(ax, stage['pos'], stage['size'][0], stage['size'][1], 
                          stage['label'], stage['color'], fontsize=9)
        
        if i < 3:  # Vertical arrows for preprocessing stages
            if i < 2:
                create_arrow(ax, (stage['pos'][0] + stage['size'][0]/2, stage['pos'][1]), 
                           (stage['pos'][0] + stage['size'][0]/2, stage['pos'][1] - 0.4), 
                           color='blue', width=1.5)
        elif i == 3:  # Arrow from preprocessing to generation
            create_arrow(ax, (3.1, 5), (4.5, 6.2), color='green', width=2)
        elif i == 4:  # Arrow from generation to training
            create_arrow(ax, (6, 6), (6, 5.3), color='red', width=2)
        elif i >= 5:  # Arrows to evaluation stages
            if i == 5:
                create_arrow(ax, (7.5, 5.2), (9, 6.2), color='purple', width=2)
            elif i == 6:
                create_arrow(ax, (7.5, 4.8), (9, 4.8), color='orange', width=2)
    
    # Add performance metrics
    ax.text(6, 3, 'Performance Results', ha='center', fontsize=12, fontweight='bold', color='darkblue')
    
    # Results boxes
    results = [
        {'pos': (1, 2), 'label': 'CDAE Protocol:\n83.0±0.1% F1\n(LOSO/LORO)', 'color': '#C8E6C9'},
        {'pos': (4, 2), 'label': 'STEA Protocol:\n82.1% F1 @ 20%\n(80% Cost Reduction)', 'color': '#FFECB3'},
        {'pos': (8, 2), 'label': 'Calibration:\nECE = 0.0072\n(Well-calibrated)', 'color': '#E1F5FE'}
    ]
    
    for result in results:
        create_rounded_box(ax, result['pos'], 2.5, 0.8, result['label'], result['color'], fontsize=9)
    
    ax.set_xlim(0, 12.5)
    ax.set_ylim(1.5, 8)
    ax.set_aspect('equal')
    ax.axis('off')
    
    plt.tight_layout()
    
    return fig, ax

def export_architecture_data():
    """
    Export architecture diagram data for other tools
    """
    # Component specifications
    components_data = {
        'Layer': ['Input', 'Physics_Modeling', 'Synthesis', 'Model_Architecture', 'Evaluation', 'Output'],
        'Component_Count': [1, 3, 3, 4, 3, 1],
        'Key_Innovation': ['Benchmark_Data', 'Physics_Guided', 'Multi_Protocol', 'Enhanced_Architecture', 'Trustworthy', 'Breakthrough_Results'],
        'Color_Code': ['#E8F4FD', '#D4EDDA', '#FFF3CD', '#F8D7DA', '#E2E3E5', '#D1ECF1']
    }
    
    import pandas as pd
    components_df = pd.DataFrame(components_data)
    components_df.to_csv('figure1_architecture_components.csv', index=False)
    
    # Performance metrics
    metrics_data = {
        'Protocol': ['CDAE_LOSO', 'CDAE_LORO', 'STEA_20%', 'STEA_Full'],
        'F1_Score': [0.830, 0.830, 0.821, 0.833],
        'Consistency': ['CV<0.2%', 'CV<0.2%', 'High', 'Baseline'],
        'Innovation': ['Cross_Subject', 'Cross_Environment', 'Label_Efficient', 'Full_Supervision']
    }
    
    metrics_df = pd.DataFrame(metrics_data)
    metrics_df.to_csv('figure1_performance_metrics.csv', index=False)
    
    print("\nFigure 1 Data Export Complete:")
    print("- figure1_architecture_components.csv - System components")
    print("- figure1_performance_metrics.csv - Key performance metrics")

if __name__ == "__main__":
    print("Generating Figure 1: System Architecture Overview...")
    print("Enhanced Attention Network Synthetic WiFi CSI Framework")
    
    # Load data from our extraction
    import json
    try:
        with open('data1_system_architecture_v1.json', 'r', encoding='utf-8') as f:
            arch_data = json.load(f)
        print("Loaded architecture data successfully")
    except FileNotFoundError:
        print("Warning: Architecture data file not found, using default parameters")
        arch_data = None

    REPO = Path(__file__).resolve().parents[2]
    FIGS = REPO / "paper" / "figures"
    FIGS.mkdir(parents=True, exist_ok=True)

    # Generate main architecture diagram
    fig1, ax1 = create_system_architecture()

    # Generate detailed data flow
    fig2, ax2 = create_detailed_data_flow()

    # Save figures to plots directory
    plots_dir = Path("../plots")
    plots_dir.mkdir(exist_ok=True)
    
    output_files = [
        (plots_dir / 'fig1_system_architecture_v1.pdf', fig1),
        (plots_dir / 'fig1_system_architecture_v1.png', fig1)
    ]

    for filename, fig in output_files:
        fig.savefig(str(filename), dpi=300, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        print(f"Saved: {filename}")

    # Export data
    export_architecture_data()

    # Display plots
    plt.show()

    print("\nFigure 1 Generation Complete!")
    print("System architecture diagram ready")
    print("Features: Complete framework overview with Enhanced Attention Network")