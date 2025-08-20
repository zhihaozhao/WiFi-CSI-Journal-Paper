# WiFi-CSI Journal Paper Repository

This repository contains the LaTeX source files and related materials for the WiFi-CSI sensing journal paper submission.

## Target Journals

Primary targets (Top-tier IoT/Mobile Computing journals):
- **IEEE Internet of Things Journal (IoTJ)** - IF: ~10.6
- **IEEE Transactions on Mobile Computing (TMC)** - IF: ~7.9  
- **Proceedings of the ACM on Interactive, Mobile, Wearable and Ubiquitous Technologies (IMWUT)** - IF: ~5.9

## Repository Structure

- `paper/` - Main LaTeX source files
  - `main.tex` - Main document
  - `refs.bib` - Bibliography  
  - `figures/` - Figure files and generation scripts
- `references/` - Reference papers (PDFs)
- `submission_materials/` - Journal-specific submission files
- `review_responses/` - Response letters to reviewers

## Paper Focus

**Title**: Trustworthy WiFi CSI Sensing with Enhanced Models and Cross-Domain Validation

**Key Contributions**:
1. Enhanced CNN+SE+Attention model for WiFi CSI sensing
2. Comprehensive calibration and reliability evaluation framework  
3. Cross-domain generalization (LOSO/LORO) validation
4. Sim2Real label efficiency analysis (10-20% labels achieving 90-95% performance)
5. Capacity-matched fair comparisons with state-of-the-art baselines

## Compilation

```bash
cd paper/
pdflatex main.tex
bibtex main
pdflatex main.tex  
pdflatex main.tex
```

## Submission Status

- [ ] First draft complete
- [ ] Internal review
- [ ] Submission to target journal
- [ ] Under review
- [ ] Revision needed
- [ ] Accepted

## Notes

This paper builds on the experimental results from the WiFi-CSI-Sensing-Results repository and implements algorithms from the WiFi-CSI-Sensing-Core repository.