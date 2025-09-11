# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an academic journal paper repository focused on Device-Free Human Activity Recognition (DFHAR) using WiFi Channel State Information (CSI). The project consists of:

- **Main LaTeX Paper**: `dfhar_v1.tex` - A comprehensive survey paper using the Sage journal template
- **Bibliography Files**: `Ref.bib` and `nsa_entry_har.bib` - Reference databases for citations
- **Figures Directory**: `plots/` - Contains all figures, diagrams, and visualizations (PDF and PNG formats)
- **Scripts Directory**: `scripts/` - Jupyter notebooks for figure generation and data analysis

## Common Development Tasks

### LaTeX Compilation
```bash
# Compile the main paper
pdflatex dfhar_v1.tex
bibtex dfhar_v1
pdflatex dfhar_v1.tex
pdflatex dfhar_v1.tex
```

### Figure Generation
```bash
# Navigate to scripts directory
cd scripts/

# Run Jupyter notebooks to generate figures
jupyter notebook SAGE_v1.6_figures.ipynb
jupyter notebook hybridHAR0727.ipynb
jupyter notebook Fig4RSSIvsCSI.ipynb
```

## Architecture and Structure

### Paper Structure
- Uses Sage journal template (`sagej` document class)
- Multi-section survey format covering DFHAR taxonomy, methodologies, and analysis
- Extensive figure integration with generated plots and diagrams
- Dual bibliography system for comprehensive citation management

### Data Workflow
1. **Literature Analysis**: Bibliography management through BibTeX files
2. **Figure Creation**: Python-based visualization using matplotlib, seaborn, graphviz
3. **Paper Compilation**: LaTeX processing with figure integration
4. **Output Generation**: PDF compilation for journal submission

### Key Dependencies
- LaTeX distribution with `sagej` class support
- Python environment with:
  - matplotlib, seaborn (visualization)
  - pandas, numpy (data processing)
  - graphviz (diagram generation)
  - plotly (interactive visualizations)
- Jupyter notebook environment

## File Conventions

### Figure Management
- All figures stored in `plots/` directory
- Naming convention: `fig[number]_description.pdf/png`
- LaTeX references use relative paths: `plots/filename.pdf`

### Bibliography Management
- Main references: `Ref.bib` (comprehensive bibliography)
- Specialized references: `nsa_entry_har.bib` (NSA and HAR specific)
- Citation keys follow author-year format

### Script Organization
- Figure generation scripts in `scripts/` directory
- Jupyter notebooks for reproducible visualization
- Self-contained cells for individual figure creation

## Git Workflow
This repository is tracked with git. When making changes:
- Commit LaTeX source changes separately from generated figures
- Include figure regeneration in commit messages when updating visualizations
- Bibliography updates should be committed with related text changes