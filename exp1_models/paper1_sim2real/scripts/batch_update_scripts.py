#!/usr/bin/env python3
"""
Batch update remaining figure scripts with v1 naming convention
Fixes Unicode characters and path issues
"""

import os
import re
from pathlib import Path

def update_script_file(script_path, fig_number):
    """Update a single script file with v1 naming and fixed paths"""
    
    print(f"Updating {script_path}...")
    
    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove Unicode emoji characters
    content = re.sub(r'[^\x00-\x7F]+', '', content)
    
    # Fix output paths - replace complex path resolution with simple ../plots
    patterns_to_replace = [
        (r'REPO = Path\(__file__\)\.resolve\(\)\.parents\[\d+\]', 'plots_dir = Path("../plots")'),
        (r'PLOTS = REPO / [^\n]+', 'plots_dir.mkdir(exist_ok=True)'),  
        (r'FIGS = REPO / [^\n]+', 'plots_dir.mkdir(exist_ok=True)'),
        (r'FIGS\.mkdir\([^)]+\)', ''),
        (r'PLOTS\.mkdir\([^)]+\)', ''),
    ]
    
    for pattern, replacement in patterns_to_replace:
        content = re.sub(pattern, replacement, content)
    
    # Update figure names to v1
    fig_patterns = [
        (f'fig{fig_number}_([^v\.\s]+)\.pdf', f'fig{fig_number}_\\1_v1.pdf'),
        (f'fig{fig_number}_([^v\.\s]+)\.png', f'fig{fig_number}_\\1_v1.png'),
    ]
    
    for pattern, replacement in fig_patterns:
        content = re.sub(pattern, replacement, content)
    
    # Fix savefig calls to use string paths
    content = re.sub(r'savefig\((plots_dir / [^,]+)', r'savefig(str(\1)', content)
    content = re.sub(r'savefig\((FIGS / [^,]+)', r'savefig(str(plots_dir / \1.split("/")[-1])', content)
    content = re.sub(r'savefig\((PLOTS / [^,]+)', r'savefig(str(plots_dir / \1.split("/")[-1])', content)
    
    # Write back the updated content
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated {script_path}")

def main():
    """Update all remaining figure scripts"""
    
    scripts_dir = Path(".")
    
    # Scripts to update with their figure numbers
    scripts_to_update = [
        ("scr5_cross_domain.py", 5),
        ("scr6_pca_analysis.py", 6),
        ("generate_fig7_comprehensive_deployment_optimized.py", 7)
    ]
    
    for script_name, fig_num in scripts_to_update:
        script_path = scripts_dir / script_name
        if script_path.exists():
            try:
                update_script_file(script_path, fig_num)
            except Exception as e:
                print(f"Error updating {script_name}: {e}")
        else:
            print(f"Script not found: {script_name}")

if __name__ == "__main__":
    main()