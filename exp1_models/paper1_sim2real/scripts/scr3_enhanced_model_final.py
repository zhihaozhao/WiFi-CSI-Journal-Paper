#!/usr/bin/env python3
"""
Figure 3: Enhanced Model Architecture with 3-Segment Arrows and Detailed Attention Parameters
- 3-segment orthogonal arrows (vertical-horizontal-vertical)
- Detailed attention parameters in boxes
- Dashed boxes around encoder and decoder sections
- All code in English
"""
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, ConnectionPatch, Rectangle

plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'DejaVu Serif'],
    'font.size': 10,
    'axes.titlesize': 14,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight'
})

def create_box(ax, x, y, w, h, label, color, fontsize=10):
    """Create a rounded rectangle box with text"""
    rect = FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.03', 
                          facecolor=color, edgecolor='black', linewidth=1.3, alpha=0.95)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h/2, label, ha='center', va='center', 
            fontsize=fontsize, color='black', wrap=True)

def create_dashed_box(ax, x, y, w, h, label, color='lightgray'):
    """Create a dashed rectangle box for grouping"""
    rect = Rectangle((x, y), w, h, facecolor=color, edgecolor='blue', 
                    linewidth=2, alpha=0.15, linestyle='--')
    ax.add_patch(rect)
    # Label at top-left corner
    ax.text(x + 0.2, y + h - 0.2, label, ha='left', va='top', 
            fontsize=12, color='blue', weight='bold')

def create_three_segment_arrow(ax, x1, y1, x2, y2, color='black', gap=0.3):
    """Create 3-segment orthogonal arrow: vertical-horizontal-vertical"""
    
    # Calculate intermediate points with gap to avoid overlap
    mid_y1 = y1 - gap  # First vertical segment end (with gap)
    mid_y2 = y2 + gap  # Second vertical segment start (with gap)
    
    # Segment 1: Vertical down (from start point)
    line1 = ConnectionPatch((x1, y1), (x1, mid_y1), 'data', 'data', 
                           arrowstyle='-', mutation_scale=15, 
                           fc=color, ec=color, linewidth=1.8)
    ax.add_patch(line1)
    
    # Segment 2: Horizontal (between verticals)
    line2 = ConnectionPatch((x1, mid_y1), (x2, mid_y2), 'data', 'data', 
                           arrowstyle='-', mutation_scale=15, 
                           fc=color, ec=color, linewidth=1.8)
    ax.add_patch(line2)
    
    # Segment 3: Vertical up to target (with arrow)
    line3 = ConnectionPatch((x2, mid_y2), (x2, y2), 'data', 'data', 
                           arrowstyle='->', mutation_scale=15, 
                           fc=color, ec=color, linewidth=1.8)
    ax.add_patch(line3)

def create_straight_arrow(ax, x1, y1, x2, y2, color='black'):
    """Create straight arrow for same-row connections"""
    arrow = ConnectionPatch((x1, y1), (x2, y2), 'data', 'data', 
                           arrowstyle='->', mutation_scale=15, 
                           fc=color, ec=color, linewidth=1.8)
    ax.add_patch(arrow)

def create_enhanced_model_figure():
    """Create Figure 3 with 3-segment arrows and detailed attention parameters"""
    
    fig, ax = plt.subplots(figsize=(22, 18))
    ax.set_xlim(0, 26)
    ax.set_ylim(0, 20)
    ax.axis('off')

    # Title
    ax.text(13, 19.2, 'Enhanced Model Architecture with Edge Optimization Integration', 
            ha='center', va='center', fontsize=16, weight='bold', color='black')
    ax.text(13, 18.6, 'Component relationships and optimization strategies with SE and Attention modules as key elements', 
            ha='center', va='center', fontsize=12, color='#1976D2')

    # Layout parameters
    box_width = 3.4
    box_height = 1.2
    horizontal_gap = 0.8
    vertical_gap = 0.8
    
    # Starting positions
    start_x = 1.5
    start_y = 17.0

    # Define all components with detailed attention parameters
    components = [
        # Row 1: Input and Stem (3 components)
        ("Input CSI\n[B, 128, 52]\nBatch × Time × Frequency", '#E3F2FD', 12),
        ("Stem Conv2D\n1→160, 3×3, s=(2,1)\n[B, 160, 64, 52]", '#FFF3E0', 10),
        ("Stem BN+SiLU\n[B, 160, 64, 52]\n→[B, 160, 64, 52]", '#FFF8E1', 10),
        
        # Row 2: Block1 (2 components)
        ("Block1 DepthwiseConv\n160→160, 3×3, s=1\n[B, 160, 64, 52]", '#E8F5E8', 10),
        ("Block1 SE\nr=12, 160→13→160\n[B, 160, 64, 52]", '#FFEBEE', 10),
        
        # Row 3: Block2 (2 components)
        ("Block2 DepthwiseConv\n160→320, 3×3, s=(2,1)\n[B, 320, 32, 52]", '#E8F5E8', 10),
        ("Block2 SE\nr=12, 320→26→320\n[B, 320, 32, 52]", '#FFEBEE', 10),
        
        # Row 4: Block3 (2 components)
        ("Block3 DepthwiseConv\n320→320, 3×3, s=1\n[B, 320, 32, 52]", '#E8F5E8', 10),
        ("Block3 SE\nr=12, 320→26→320\n[B, 320, 32, 52]", '#FFEBEE', 10),
        
        # Row 5: Encoder section (2 components)
        ("GAP (F-dim)\nPool F=52→1\n[B, 320, 32]", '#F3E5F5', 10),
        ("LayerNorm\nNormalization\n[32, B, 320]\n640 params", '#F3E5F5', 10),
        
        # Row 6: Decoder section (3 components)  
        ("Q,K,V Generation\nProjections\n[32, B, 960]\n308,160 params", '#E8F5E8', 10),
        ("Self-Attention\nMultiHead(h=4)\n[32, B, 320]src", '#E8F5E8', 10),
        ("Output Projection\nLinear + Dropout\n[B, 320, 32]\n102,720 params", '#E8F5E8', 10),
        
        # Row 7: Final output (2 components)
        ("Global Pooling\nAdaptiveAvgPool1d(1)\n[B, 320]", '#E1F5FE', 10),
        ("Classifier\nLinear(320→8)\n[B, 8]\n2,568 params", '#D5F5E3', 10),
    ]

    # Layout configuration: components per row and positions
    row_configs = [
        (0, 3, start_y, 5), #8),          # Row 1: 3 components
        (3, 2, start_y - 2, 4),   # Row 2: 2 components
        (5, 2, start_y - 4, 4),   # Row 3: 2 components
        (7, 2, start_y - 6, 4),   # Row 4: 2 components
        (9, 2, start_y - 8.5, 4),  # Row 5: 2 encoder components
        (11, 3, start_y - 11, 5), #6), # Row 6: 3 decoder components
        (14, 2, start_y - 13.5, 4), # Row 7: 2 output components
    ]

    # Store component positions for arrow drawing
    component_positions = []
    
    # Draw all components
    for row_start_idx, row_count, row_y, layout_width in row_configs:
        # Calculate starting x for centering the row
        total_width = row_count * box_width + (row_count - 1) * horizontal_gap
        available_space = layout_width * (box_width + horizontal_gap)
        row_start_x = start_x + (available_space - total_width) / 2
        
        for i in range(row_count):
            comp_idx = row_start_idx + i
            if comp_idx < len(components):
                label, color, fontsize = components[comp_idx]
                x = row_start_x + i * (box_width + horizontal_gap)
                y = row_y
                
                create_box(ax, x, y, box_width, box_height, label, color, fontsize)
                component_positions.append((x + box_width/2, y + box_height/2))

    # Add dashed boxes for encoder and decoder sections
    # Encoder box (around GAP and LayerNorm)
    encoder_x = start_x + 3.5 #2
    encoder_y = start_y - 8.5 #11.2
    encoder_w = 10 #8
    encoder_h = 2.2 #2.0
    create_dashed_box(ax, encoder_x, encoder_y, encoder_w, encoder_h, 'ENCODER', '#E3F2FD')
    
    # Decoder box (around Q,K,V Generation, Self-Attention, Output Projection)
    decoder_x = start_x + 3.5 #1
    decoder_y = start_y - 10.9 #13.7
    decoder_w = 14 #12
    decoder_h = 2.2 #2.0
    create_dashed_box(ax, decoder_x, decoder_y, decoder_w, decoder_h, 'DECODER', '#F0F8FF')

    # Define arrow connections with 3-segment arrows for cross-row connections
    arrow_connections = [
        # Row 1: horizontal connections
        (0, 1), (1, 2),
        # Cross-row: 3-segment arrows
        (2, 3),   # Stem BN+SiLU to Block1 DepthwiseConv
        (4, 5),   # Block1 SE to Block2 DepthwiseConv
        (6, 7),   # Block2 SE to Block3 DepthwiseConv
        (8, 9),   # Block3 SE to GAP
        (10, 11), # LayerNorm to Q,K,V Generation
        (13, 14), # Output Projection to Global Pooling
        # Same-row: horizontal arrows
        (3, 4), (5, 6), (7, 8), (9, 10), (11, 12), (12, 13), (14, 15)
    ]
    
    # Draw arrows - ensuring proper 3-segment routing
    for start_idx, end_idx in arrow_connections:
        if start_idx < len(component_positions) and end_idx < len(component_positions):
            x1, y1 = component_positions[start_idx]
            x2, y2 = component_positions[end_idx]
            
            # Same row: straight arrow with proper clearance
            if abs(y1 - y2) < 0.5:
                create_straight_arrow(ax, x1 + box_width/2, y1, x2 - box_width/2, y2)
            else:
                # Different rows: 3-segment arrow with proper connection points
                start_x = x1
                start_y = y1 - box_height/2 - 0.1  # Add clearance from box bottom
                end_x = x2
                end_y = y2 + box_height/2 + 0.1    # Add clearance from box top
                create_three_segment_arrow(ax, start_x, start_y, end_x, end_y, gap=0.4)

    # Parameter information panel (right side)
    param_panel_x = 19 #19.5
    param_panel_w = 5.5
    param_panel_h = 1.0
    
    param_info = [
        ("Total Parameters\n640,713", '#E3F2FD'),
        ("Stem: 1,760 params\n(0.3%)", '#FFF8E1'),
        ("Block1: 31,693 params\n(4.9%)", '#F1F8E9'),
        ("Block2: 70,266 params\n(11.0%)", '#F1F8E9'),
        ("Block3: 122,906 params\n(19.2%)", '#F1F8E9'),
        ("Attention: 411,520 params\n(64.2%) - Major", '#F3E5F5'),
        ("Classifier: 2,568 params\n(0.4%)", '#E8F5E8')
    ]
    
    for i, (text, color) in enumerate(param_info):
        y = start_y - i * 1.3 + 10
        create_box(ax, param_panel_x, y, param_panel_w, param_panel_h, text, color, 10)

    # Bottom explanations - properly spaced
    # Attention encoding/decoding process
    attention_y = 10.3 #3.0
    attention_text = ("Attention Encoding: GAP(F-dim) → Permute → LayerNorm (640 params)\n"
                     "Attention Decoding: Q,K,V Gen (308,160 params) → Self-Attn → Output Proj (102,720 params)")
    
    ax.text(13, attention_y, attention_text, ha='center', va='center', fontsize=11,
            bbox=dict(boxstyle="round,pad=0.4", facecolor='#F3E5F5', 
                     edgecolor='blue', alpha=0.7))

    # Architecture and performance details
    details_y = 7.8 #1.8
    details_text = ("SE Module: GAP → FC(C/r) → ReLU → FC(C) → Sigmoid | "
                   "DepthwiseSeparable: DW Conv + PW Conv + BN + SiLU\n"
                   "Edge Performance: GPU Speedup 64.1×, Throughput 607 samples/sec, Latency 5.29ms")
    
    ax.text(13.6, details_y, details_text, ha='center', va='center', fontsize=10,
            bbox=dict(boxstyle="round,pad=0.4", facecolor='#F5F5F5', 
                     edgecolor='gray', alpha=0.7))

    # Training configuration
    training_text = ("Training: AdamW, lr=3e-4, batch=64; Sim2Real with 20% labels\n"
                    "Metrics: LOSO/LORO Macro-F1, ECE calibration, Stability Index, Deployment Readiness")
    
    ax.text(13, 5.4, training_text, ha='center', va='center', fontsize=11,
            bbox=dict(boxstyle="round,pad=0.4", facecolor='#F8F9FA', 
                     edgecolor='gray', alpha=0.7))

    print("Enhanced Model Figure created with 3-segment arrows and attention parameters")
    return fig

if __name__ == '__main__':
    # Set up output path
    plots_dir = Path("../plots")
    plots_dir.mkdir(exist_ok=True)

    # Generate figure
    fig = create_enhanced_model_figure()
    output_file = plots_dir / 'fig3_enhanced_model_v1.pdf'
    output_png = plots_dir / 'fig3_enhanced_model_v1.png'
    
    fig.savefig(str(output_file), dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    fig.savefig(str(output_png), dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    print(f'Figure saved: {output_file}')
    print(f'Figure saved: {output_png}')