#!/usr/bin/env python3
"""
Figure 2: Physics-Guided Framework with Enhanced Model Architecture
Saves: paper/paper1_sim2real/plots/fig2_physics_guided_framework.pdf

Final version for paper submission - clean and accurate
"""
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import matplotlib.patheffects as pe

plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'DejaVu Serif'],
    'font.size': 11,
    'axes.titlesize': 14,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight'
})

def box(ax, x, y, w, h, label, fc, fontsize=10):
    rect = FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.02', facecolor=fc,
                          edgecolor='black', linewidth=1.2, alpha=0.95)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h/2, label, ha='center', va='center', 
            fontsize=fontsize, color='black', wrap=True, weight='normal')

def arrow(ax, x1, y1, x2, y2, color='black'):
    cp = ConnectionPatch((x1, y1), (x2, y2), 'data', 'data', arrowstyle='->',
                         mutation_scale=12, fc=color, ec=color, linewidth=1.5)
    ax.add_patch(cp)

def create_fig2():
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(10, 9.5, 'Physics-Guided Sim2Real Framework with Edge Deployment Integration', 
            ha='center', va='center', fontsize=16, weight='bold', color='black')
    
    # Left side - Framework pipeline
    left_x = 1
    box_w = 2.5
    box_h = 1.2
    
    # Pipeline boxes
    pipeline_boxes = [
        (left_x, 7.5, "Data Acquisition\n(Raw CSI\nStreams)", '#E6F2FF'),
        (left_x, 6.1, "Preprocessing\n(Sync, Denoise,\nNormalization)", '#E6F2FF'),
        (left_x, 4.7, "Physics Modeling\n(Multipath, Human,\nEnvironment)", '#D5F5E3'),
        (left_x, 3.3, "Parameterized Synthesis\n(Scenario + Channel\nControl)", '#FDEBD0'),
        (left_x, 1.9, "Enhanced Model\n(CNN + SE + Temporal\nAttention)", '#FADBD8'),
        (left_x, 0.5, "Calibrated\nOutput", '#E8DAEF')
    ]
    
    for i, (x, y, label, color) in enumerate(pipeline_boxes):
        box(ax, x, y, box_w, box_h, label, color, fontsize=10)
        if i < len(pipeline_boxes) - 1:
            arrow(ax, x + box_w/2, y - 0.1, x + box_w/2, y - 0.3)
    
    # Right side - Enhanced Model Architecture  
    model_x = 6
    model_y = 0.1
    model_w = 10 #12
    model_h = 8.8
    
    # Model container
    model_rect = FancyBboxPatch((model_x, model_y), model_w, model_h, 
                               boxstyle='round,pad=0.1', facecolor='#F8F9FA',
                               edgecolor='black', linewidth=2, alpha=0.9, linestyle='--')
    ax.add_patch(model_rect)
    ax.text(model_x + model_w/2, model_y + model_h - 0.3, 'Enhanced Model Architecture', 
            ha='center', va='center', fontsize=14, weight='bold', color='black')
    
    # Model components (vertical flow)
    comp_w = 4.2  # Increased width to prevent parameter overlap
    comp_h = 0.8
    comp_x = model_x + (model_w - comp_w) / 2 + 1
    
    components = [
        (comp_x, 7.3, "Input CSI\n[B, 128, 52]", '#E6F2FF'),
        (comp_x, 6.2, "Stem Layer\nConv2d(1→160), BN + SiLU\n1,760 params", '#FDEBD0'),
        (comp_x, 5.1, "Block1: DepthwiseSeparable\n160→160 + SE(r=12)\n31,693 params", '#FDEBD0'),
        (comp_x, 4.0, "Block2: DepthwiseSeparable\n160→320 + SE(r=12)\n70,266 params", '#FDEBD0'),
        (comp_x, 2.9, "Block3: DepthwiseSeparable\n320→320 + SE(r=12)\n122,906 params", '#FDEBD0'),
        (comp_x, 1.8, "Temporal Attention\nMultiHead(320, heads=4)\n411,520 params", '#E8DAEF')
    ]
    
    for i, (x, y, label, color) in enumerate(components):
        box(ax, x, y, comp_w, comp_h, label, color, fontsize=9)
        if i < len(components) - 1:
            arrow(ax, x + comp_w/2, y - 0.05, x + comp_w/2, y - 0.15)
    
    # Parameter summary box (moved to avoid overlap)
    param_x = model_x #+ 1
    param_y = 0.2
    param_w = 3.6 #5
    param_h = 1.2
    param_text = ("Total Parameters: 640,713\nMemory: 2.44 MB\nEdge Ready: Production")
    box(ax, param_x, param_y, param_w, param_h, param_text, '#E3F2FD', fontsize=10)
    
    # Final classifier
    box(ax, comp_x, 0.7, comp_w, comp_h, "Classifier\nLinear(320→8)\n2,568 params", '#D5F5E3', fontsize=9)
    arrow(ax, comp_x + comp_w/2, 1.75, comp_x + comp_w/2, 1.55)
    
    # Connect pipeline to model
    arrow(ax, left_x + box_w, 2.5, model_x - 0.2, 4.5)
    
    # Performance metrics box
    perf_x = model_x #+ 8.4 #7
    perf_y = 1.6 #0.2
    perf_w = 3.6 #4
    perf_h = 1.2
    perf_text = ("GPU Speedup: 64.1×\nThroughput: 607 sps\nLatency: 5.29 ms")
    box(ax, perf_x, perf_y, perf_w, perf_h, perf_text, '#E8F5E8', fontsize=10)
    
    return fig

if __name__ == '__main__':
    plots_dir = Path("../plots")
    plots_dir.mkdir(exist_ok=True)
    
    fig = create_fig2()
    out = plots_dir / 'fig2_physics_guided_framework_v1.pdf'
    fig.savefig(str(out), dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    
    out_png = plots_dir / 'fig2_physics_guided_framework_v1.png'
    fig.savefig(str(out_png), dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    
    print(f'Saved Figure 2: {out}')
    print(f'Saved Figure 2: {out_png}')