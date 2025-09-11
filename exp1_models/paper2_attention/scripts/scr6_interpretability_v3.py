#!/usr/bin/env python3
"""
Figure 6 Generation Script: EAN Interpretability Analysis
Creates comprehensive interpretability visualization with 2 subplots:
(a) SE Channel Attention Patterns - Real frequency-domain selectivity
(b) Temporal Attention Dynamics - Real temporal focusing patterns

Based on authentic experimental results, removes false physics correlation claims
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
import seaborn as sns
import json
from pathlib import Path
from matplotlib.patches import Rectangle
from matplotlib.colors import LinearSegmentedColormap

# Configure matplotlib for publication quality
plt.rcParams.update({
    'font.size': 11,
    'font.family': 'serif',
    'font.serif': ['Times New Roman'],
    'axes.linewidth': 0.8,
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.figsize': [12, 6],
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.1
})

class Figure6Generator:
    """Generate Figure 6: EAN Interpretability Analysis"""
    
    def __init__(self):
        self.activities = ['walking', 'sitting', 'standing', 'falling', 'picking_up', 'lying_down']
        self.activity_colors = {
            'walking': '#1f77b4',      # Blue
            'sitting': '#ff7f0e',      # Orange  
            'standing': '#2ca02c',     # Green
            'falling': '#d62728',      # Red
            'picking_up': '#9467bd',   # Purple
            'lying_down': '#8c564b'    # Brown
        }
        self.activity_labels = {
            'walking': 'Walking',
            'sitting': 'Sitting',
            'standing': 'Standing', 
            'falling': 'Falling',
            'picking_up': 'Picking Up',
            'lying_down': 'Lying Down'
        }
        
    def load_data(self):
        """Load interpretability data"""
        data_path = Path('../plots/data6_interpretability_real.json')
        
        if data_path.exists():
            print(f"Loading data from {data_path}")
            with open(data_path, 'r') as f:
                return json.load(f)
        else:
            print("Data not found, generating from extraction script...")
            # Import and run data extraction
            from data6_interpretability_real import Figure6DataExtractor
            extractor = Figure6DataExtractor()
            return extractor.extract_figure6_data()
    
    def create_se_attention_subplot(self, ax, data):
        """Create subplot (a): SE Channel Attention Patterns"""
        print("Creating SE Channel Attention subplot...")
        
        se_patterns = data['se_patterns']
        F = 52  # Number of subcarriers
        
        # Create heatmap data
        heatmap_data = np.zeros((len(self.activities), F))
        activity_names = []
        
        for i, activity in enumerate(self.activities):
            if activity in se_patterns:
                weights = np.array(se_patterns[activity][:F])
                # Normalize each activity pattern for better visualization
                weights = (weights - weights.min()) / (weights.max() - weights.min() + 1e-8)
                heatmap_data[i, :] = weights
                activity_names.append(self.activity_labels[activity])
            else:
                activity_names.append(self.activity_labels[activity])
        
        # Create custom colormap (blue to white to red)
        colors = ['#1e3a8a', '#3b82f6', '#bfdbfe', '#fecaca', '#f87171', '#dc2626']
        n_bins = 256
        cmap = LinearSegmentedColormap.from_list('attention', colors, N=n_bins)
        
        # Create heatmap
        im = ax.imshow(heatmap_data, aspect='auto', cmap=cmap, interpolation='bilinear')
        
        # Customize axes
        ax.set_xlabel('Subcarrier Index', fontweight='bold')
        ax.set_ylabel('Activity Type', fontweight='bold') 
        ax.set_title('(a) SE Channel Attention Patterns', fontweight='bold')
        
        # Set ticks
        ax.set_xticks(np.arange(0, F, 10))
        ax.set_xticklabels(np.arange(0, F, 10))
        ax.set_yticks(np.arange(len(activity_names)))
        ax.set_yticklabels(activity_names)
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        cbar.set_label('Attention Weight', rotation=270, labelpad=15, fontweight='bold')
        
        # Add frequency band annotations
        # Low frequencies (0-15): Static components
        ax.add_patch(Rectangle((0, -0.5), 15, len(activity_names), 
                              fill=False, edgecolor='gray', linestyle='--', alpha=0.7))
        ax.text(7.5, len(activity_names) + 0.3, 'Static\nComponents', 
                ha='center', va='bottom', fontsize=9, color='gray')
        
        # Mid frequencies (15-35): Motion sensitivity  
        ax.add_patch(Rectangle((15, -0.5), 20, len(activity_names),
                              fill=False, edgecolor='green', linestyle='--', alpha=0.7))
        ax.text(25, len(activity_names) + 0.3, 'Motion\nSensitive', 
                ha='center', va='bottom', fontsize=9, color='green')
        
        # High frequencies (35-52): Fine-grained patterns
        ax.add_patch(Rectangle((35, -0.5), 17, len(activity_names),
                              fill=False, edgecolor='purple', linestyle='--', alpha=0.7))
        ax.text(43.5, len(activity_names) + 0.3, 'Fine-grained\nPatterns', 
                ha='center', va='bottom', fontsize=9, color='purple')
    
    def create_temporal_attention_subplot(self, ax, data):
        """Create subplot (b): Temporal Attention Dynamics"""
        print("Creating Temporal Attention Dynamics subplot...")
        
        temporal_patterns = data['temporal_patterns']
        T = 128  # Time steps
        time_axis = np.linspace(0, 4, T)  # 4-second window
        
        # Plot attention patterns for each activity
        for activity in self.activities:
            if activity in temporal_patterns:
                attention_weights = np.array(temporal_patterns[activity][:T])
                # Smooth the pattern for better visualization
                attention_weights = self.smooth_signal(attention_weights, window=5)
                
                ax.plot(time_axis, attention_weights, 
                       color=self.activity_colors[activity],
                       linewidth=2.5, 
                       label=self.activity_labels[activity],
                       alpha=0.8)
        
        # Customize axes
        ax.set_xlabel('Time (seconds)', fontweight='bold')
        ax.set_ylabel('Attention Weight', fontweight='bold')
        ax.set_title('(b) Temporal Attention Dynamics', fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.set_xlim(0, 4)
        ax.set_ylim(0, 1)
        
        # Add legend
        legend = ax.legend(loc='upper right', frameon=True, fancybox=True, shadow=True)
        legend.get_frame().set_alpha(0.9)
        
        # Add activity phase annotations
        # Early phase (0-1s): Preparation/initialization
        ax.axvspan(0, 1, alpha=0.1, color='blue', label='_nolegend_')
        ax.text(0.5, 0.95, 'Initialization', ha='center', va='top', 
                fontsize=9, color='blue', alpha=0.7)
        
        # Middle phase (1-3s): Main activity execution
        ax.axvspan(1, 3, alpha=0.1, color='green', label='_nolegend_')
        ax.text(2, 0.95, 'Activity Execution', ha='center', va='top',
                fontsize=9, color='green', alpha=0.7)
        
        # Late phase (3-4s): Completion/stabilization
        ax.axvspan(3, 4, alpha=0.1, color='orange', label='_nolegend_')
        ax.text(3.5, 0.95, 'Stabilization', ha='center', va='top',
                fontsize=9, color='orange', alpha=0.7)
    
    def smooth_signal(self, signal, window=5):
        """Apply simple moving average smoothing"""
        if len(signal) < window:
            return signal
        
        smoothed = np.convolve(signal, np.ones(window)/window, mode='same')
        # Fix edge effects
        smoothed[:window//2] = signal[:window//2]
        smoothed[-(window//2):] = signal[-(window//2):]
        return smoothed
    
    def generate_figure6(self):
        """Generate complete Figure 6"""
        print("=" * 70)
        print("GENERATING FIGURE 6: EAN INTERPRETABILITY ANALYSIS")
        print("Authentic attention patterns without false physics claims")
        print("=" * 70)
        
        # Load data
        data = self.load_data()
        
        # Create figure with 2 subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Create subplots
        self.create_se_attention_subplot(ax1, data)
        self.create_temporal_attention_subplot(ax2, data)
        
        # Adjust layout
        plt.tight_layout()
        plt.subplots_adjust(top=0.92, bottom=0.1, left=0.08, right=0.95, hspace=0.3, wspace=0.3)
        
        # Add main title
        fig.suptitle('EAN Interpretability Analysis: Dual-Branch Attention Mechanisms', 
                    fontsize=14, fontweight='bold', y=0.98)
        
        # Save figure
        output_dir = Path('../plots')
        output_dir.mkdir(exist_ok=True)
        
        # Save as high-resolution PDF and PNG
        pdf_path = output_dir / 'fig6_interpretability_v3.pdf'
        png_path = output_dir / 'fig6_interpretability_v3.png'
        
        plt.savefig(str(pdf_path), format='pdf', dpi=300, bbox_inches='tight')
        plt.savefig(str(png_path), format='png', dpi=300, bbox_inches='tight')
        
        print(f"\n[SUCCESS] Figure 6 generated successfully!")
        print(f"Saved to: {output_dir}")
        print(f"Files:")
        print(f"   - {pdf_path.name} (PDF - publication quality)")
        print(f"   - {png_path.name} (PNG - presentation quality)")
        
        # Display the figure (disabled for CLI environment)
        # plt.show()
        
        return fig

def main():
    """Generate Figure 6"""
    generator = Figure6Generator()
    fig = generator.generate_figure6()
    return fig

if __name__ == "__main__":
    main()