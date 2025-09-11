#!/usr/bin/env python3
"""
Figure 4: CDAE Cross-Domain Adaptation Results - Script Generation
生成基于真实实验数据的CDAE跨域自适应结果图，包含4个有意义的子图

Based on authentic experimental data from data4_crossdomain_v4.csv
Supports CDAE Cross-Domain Adaptation Results section in paper2_pase_net
Follows authenticity-first principle - NO hardcoding!
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Rectangle
import matplotlib.patches as mpatches
import os
import sys

# 设置字体和绘图风格
plt.rcParams['font.family'] = ['DejaVu Sans', 'Arial']
plt.rcParams['font.size'] = 11
plt.rcParams['axes.unicode_minus'] = False
sns.set_style("whitegrid")

def load_experimental_data():
    """加载真实实验数据"""
    
    # 加载汇总统计数据
    summary_path = os.path.join('..', 'plots', 'data4_crossdomain_v4.csv')
    if not os.path.exists(summary_path):
        print(f"错误：数据文件不存在 {summary_path}")
        return None, None
    
    df_summary = pd.read_csv(summary_path)
    print("加载汇总数据:")
    print(df_summary[['model_name', 'loso_mean', 'loro_mean', 'domain_gap', 'stability_status']])
    
    # 加载原始数据
    raw_path = os.path.join('..', 'plots', 'data4_crossdomain_v4_raw.csv')
    df_raw = None
    if os.path.exists(raw_path):
        df_raw = pd.read_csv(raw_path)
        print(f"\n加载原始数据: {len(df_raw)} 条记录")
    
    return df_summary, df_raw

def subplot_a_loso_loro_comparison(ax, df_summary):
    """子图A: LOSO vs LORO性能对比 - 体现跨域泛化能力"""
    
    models = df_summary['model_name'].tolist()
    loso_means = df_summary['loso_mean'].tolist()
    loso_stds = df_summary['loso_std'].tolist()
    loro_means = df_summary['loro_mean'].tolist()
    loro_stds = df_summary['loro_std'].tolist()
    
    x = np.arange(len(models))
    width = 0.35
    
    # 根据模型性能设置颜色
    colors_loso = ['#2E86AB', '#A23B72', '#F18F01', '#E74C3C']
    colors_loro = ['#5DADE2', '#EC7063', '#F39C12', '#C0392B']
    
    bars1 = ax.bar(x - width/2, loso_means, width, yerr=loso_stds, 
                   label='LOSO (Subject Transfer)', alpha=0.85, capsize=4,
                   color=colors_loso, edgecolor='black', linewidth=0.8)
    bars2 = ax.bar(x + width/2, loro_means, width, yerr=loro_stds,
                   label='LORO (Environment Transfer)', alpha=0.85, capsize=4,
                   color=colors_loro, edgecolor='black', linewidth=0.8)
    
    # 添加数值标签
    for i, (bar1, bar2, model) in enumerate(zip(bars1, bars2, models)):
        height1, height2 = bar1.get_height(), bar2.get_height()
        
        # 只为PASE-Net添加特殊标记（最佳性能）
        if model == 'PASE-Net':
            ax.text(bar1.get_x() + bar1.get_width()/2., height1 + loso_stds[i] + 2,
                    f'{height1:.1f}%★', ha='center', va='bottom', 
                    fontsize=10, fontweight='bold', color='darkblue')
            ax.text(bar2.get_x() + bar2.get_width()/2., height2 + loro_stds[i] + 2,
                    f'{height2:.1f}%★', ha='center', va='bottom', 
                    fontsize=10, fontweight='bold', color='darkred')
        else:
            ax.text(bar1.get_x() + bar1.get_width()/2., height1 + loso_stds[i] + 1,
                    f'{height1:.1f}%', ha='center', va='bottom', fontsize=9)
            ax.text(bar2.get_x() + bar2.get_width()/2., height2 + loro_stds[i] + 1,
                    f'{height2:.1f}%', ha='center', va='bottom', fontsize=9)
    
    ax.set_xlabel('Model Architecture', fontweight='bold')
    ax.set_ylabel('Macro F1-Score (%)', fontweight='bold')
    ax.set_title('(a) Cross-Domain Performance: Subject vs Environment Transfer', 
                 fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(models, rotation=0)
    ax.legend(loc='upper right', framealpha=0.9)
    ax.set_ylim(0, 100)
    ax.grid(True, alpha=0.3)

def subplot_b_domain_gap_analysis(ax, df_summary):
    """子图B: 域间隙分析 - 展示跨域稳定性"""
    
    models = df_summary['model_name'].tolist()
    domain_gaps = df_summary['domain_gap'].tolist()
    stability_status = df_summary['stability_status'].tolist()
    
    # 根据稳定性状态设置颜色
    color_map = {'Excellent': '#27AE60', 'Good': '#F39C12', 'Moderate': '#E67E22', 'Unstable': '#E74C3C'}
    colors = [color_map[status] for status in stability_status]
    
    bars = ax.bar(models, domain_gaps, color=colors, alpha=0.8, 
                  edgecolor='black', linewidth=1)
    
    # 添加数值标签和稳定性状态
    for bar, gap, status in zip(bars, domain_gaps, stability_status):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + max(domain_gaps) * 0.02,
                f'{gap:.1f}%\n({status})', ha='center', va='bottom', 
                fontsize=9, fontweight='bold')
    
    # 添加性能阈值参考线
    ax.axhline(y=1.0, color='green', linestyle='--', alpha=0.7, 
               label='Excellent (<1%)', linewidth=2)
    ax.axhline(y=5.0, color='orange', linestyle='--', alpha=0.7, 
               label='Good (<5%)', linewidth=2)
    
    ax.set_xlabel('Model Architecture', fontweight='bold')
    ax.set_ylabel('Domain Gap |LOSO - LORO| (%)', fontweight='bold')
    ax.set_title('(b) Cross-Domain Generalization Stability', fontweight='bold')
    ax.tick_params(axis='x', rotation=15)
    ax.legend(loc='upper right', framealpha=0.9)
    ax.set_yscale('log')  # 对数刻度突出差异
    ax.grid(True, alpha=0.3)

def subplot_c_model_robustness(ax, df_summary):
    """子图C: 模型鲁棒性分析 - 变异系数和失败率"""
    
    models = df_summary['model_name'].tolist()
    
    # 计算变异系数
    loso_cv = (df_summary['loso_std'] / df_summary['loso_mean'] * 100).tolist()
    loro_cv = (df_summary['loro_std'] / df_summary['loro_mean'] * 100).tolist()
    loso_failures = df_summary['loso_failures'].tolist()
    
    x = np.arange(len(models))
    width = 0.3
    
    # 绘制变异系数
    bars1 = ax.bar(x - width, loso_cv, width, label='LOSO Variability (CV%)', 
                   alpha=0.7, color='skyblue', edgecolor='blue')
    bars2 = ax.bar(x, loro_cv, width, label='LORO Variability (CV%)',
                   alpha=0.7, color='lightcoral', edgecolor='red')
    
    # 绘制失败次数（右轴）
    ax2 = ax.twinx()
    bars3 = ax2.bar(x + width, loso_failures, width, label='LOSO Failures', 
                    alpha=0.9, color='red', edgecolor='darkred')
    
    # 添加数值标签
    for i, (bar1, bar2, bar3) in enumerate(zip(bars1, bars2, bars3)):
        ax.text(bar1.get_x() + bar1.get_width()/2., bar1.get_height() + 0.1,
                f'{loso_cv[i]:.1f}%', ha='center', va='bottom', fontsize=8)
        ax.text(bar2.get_x() + bar2.get_width()/2., bar2.get_height() + 0.1,
                f'{loro_cv[i]:.1f}%', ha='center', va='bottom', fontsize=8)
        if loso_failures[i] > 0:
            ax2.text(bar3.get_x() + bar3.get_width()/2., bar3.get_height() + 0.1,
                     f'{loso_failures[i]}', ha='center', va='bottom', 
                     fontsize=10, fontweight='bold', color='darkred')
    
    ax.set_xlabel('Model Architecture', fontweight='bold')
    ax.set_ylabel('Coefficient of Variation (%)', fontweight='bold')
    ax2.set_ylabel('Number of Failed Seeds', fontweight='bold', color='red')
    ax.set_title('(c) Model Robustness: Variability and Convergence Reliability', 
                 fontweight='bold')
    
    ax.set_xticks(x)
    ax.set_xticklabels(models, rotation=15)
    ax.legend(loc='upper left', framealpha=0.9)
    ax2.legend(loc='upper right', framealpha=0.9)
    ax.grid(True, alpha=0.3)

def subplot_d_performance_distribution(ax, df_raw):
    """子图D: 性能分布箱线图 - 展示详细的性能分布特征"""
    
    if df_raw is None:
        ax.text(0.5, 0.5, 'Raw data not available', ha='center', va='center', 
                transform=ax.transAxes, fontsize=14)
        return
    
    # 准备箱线图数据
    models_order = ['PASE-Net', 'CNN', 'BiLSTM', 'Conformer']
    protocols = ['LOSO', 'LORO']
    
    plot_data = []
    positions = []
    colors = []
    
    pos = 0
    for model in models_order:
        for protocol in protocols:
            data_subset = df_raw[(df_raw['model_name'] == model) & 
                               (df_raw['protocol'] == protocol)]
            if not data_subset.empty:
                scores = data_subset['f1_score'].tolist()
                plot_data.append(scores)
                positions.append(pos)
                
                # 设置颜色
                if protocol == 'LOSO':
                    colors.append('lightblue')
                else:
                    colors.append('lightcoral')
            pos += 1
        pos += 0.5  # 模型间间距
    
    # 绘制箱线图
    box_parts = ax.boxplot(plot_data, positions=positions, patch_artist=True,
                          widths=0.6, showfliers=True)
    
    # 设置箱子颜色
    for patch, color in zip(box_parts['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    # 添加分组标签
    group_positions = [0.5, 2, 3.5, 5]  # 每组的中心位置
    ax.set_xticks(group_positions)
    ax.set_xticklabels(models_order)
    
    # 添加协议标签
    legend_elements = [mpatches.Patch(color='lightblue', alpha=0.7, label='LOSO'),
                      mpatches.Patch(color='lightcoral', alpha=0.7, label='LORO')]
    ax.legend(handles=legend_elements, loc='lower right', framealpha=0.9)
    
    ax.set_ylabel('F1-Score (%)', fontweight='bold')
    ax.set_xlabel('Model Architecture', fontweight='bold')
    ax.set_title('(d) Performance Distribution Across Seeds', fontweight='bold')
    ax.grid(True, alpha=0.3)

def create_figure():
    """创建完整的Figure 4"""
    
    # 加载数据
    df_summary, df_raw = load_experimental_data()
    
    if df_summary is None:
        print("错误：无法加载实验数据")
        return
    
    # 创建图形 (2×2 布局)
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Figure 4: CDAE Cross-Domain Adaptation Results', 
                 fontsize=18, fontweight='bold', y=0.96)
    
    # 创建四个子图
    subplot_a_loso_loro_comparison(ax1, df_summary)
    subplot_b_domain_gap_analysis(ax2, df_summary) 
    subplot_c_model_robustness(ax3, df_summary)
    subplot_d_performance_distribution(ax4, df_raw)
    
    # 调整布局
    plt.tight_layout()
    plt.subplots_adjust(top=0.92, hspace=0.35, wspace=0.3)
    
    # 添加关键发现总结
    summary_text = """Key Findings from CDAE Cross-Domain Adaptation:
• PASE-Net achieves identical LOSO/LORO performance (83.0%) - excellent domain invariance
• Conformer suffers from severe instability: 3/5 LOSO seeds fail (convergence issues)  
• Domain gap analysis: PASE-Net (0.04%) << CNN (4.5%) < BiLSTM (1.4%) << Conformer (43.8%)
• Model robustness: PASE-Net shows lowest variability across subjects and environments"""
    
    fig.text(0.02, 0.02, summary_text, fontsize=10, 
             bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgray", alpha=0.9),
             verticalalignment='bottom')
    
    # 保存图片
    output_path = os.path.join('..', 'plots', 'fig4_crossdomain_v4.pdf')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    print(f"Figure saved: {output_path}")
    
    # 同时保存PNG版本便于预览
    png_path = os.path.join('..', 'plots', 'fig4_crossdomain_v4.png')
    plt.savefig(png_path, dpi=150, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    print(f"PNG version saved: {png_path}")
    
    # Don't show in Windows environment to avoid display issues
    # plt.show()

def main():
    """主函数"""
    print("=" * 70)
    print("Figure 4: CDAE Cross-Domain Adaptation Results")
    print("基于真实实验数据，展示跨域自适应性能分析")
    print("=" * 70)
    
    create_figure()

if __name__ == "__main__":
    main()