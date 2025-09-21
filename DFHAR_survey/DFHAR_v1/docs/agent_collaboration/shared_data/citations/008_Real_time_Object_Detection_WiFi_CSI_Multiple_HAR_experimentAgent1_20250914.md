# Real-time Object Detection for WiFi CSI-based Multiple Human Activity Recognition - Experimental Analysis

## Basic Information
- **Paper ID**: 117
- **Title**: A Real-time Object Detection for WiFi CSI-based Multiple Human Activity Recognition
- **Authors**: Israel Elujide, Jian Li, Aref Shiran, Siwang Zhou, Yonghe Liu
- **Publication**: 2023 IEEE 20th Consumer Communications & Networking Conference (CCNC)
- **DOI**: 10.1109/CCNC51644.2023.10059647
- **Analysis Date**: 2025-09-14
- **Analyzed by**: experimentAgent1

## Experimental Framework Analysis

### Dataset Analysis (Score: 7/10)

#### Dataset Collection Methodology
The experimental evaluation employs a limited but focused dataset collection approach:

**Single Activity Datasets**:
- **Run Activity**: 115 training instances, 16 validation instances, 12 test instances
- **Walk Activity**: 312 training instances, 81 validation instances, 62 test instances
- **Total Participants**: Multiple subjects (exact number not specified)
- **Sampling Rate**: 80 packets/second
- **Data Split**: 70% training, 15% validation, 15% testing

**Multiple Activity Dataset**:
- **Combined Activities**: Hand movement, running, walking
- **Training Instances**: 108 instances of multiple activities + no-activity periods
- **Validation/Test**: 22 instances each
- **Activity Types**: 3 distinct activities plus no-activity state

#### Hardware Setup
**Experimental Environment**:
- **Transmitter**: TP-Link AC1750 dual-band access point (2.4 GHz)
- **Receiver**: Laptop with Intel NIC5300 for CSI collection
- **Operating System**: Ubuntu Linux 12.04 LTS with modified kernel
- **CSI Collection Tool**: Intel 5300 CSI tool [10]

#### Data Quality Assessment
**Strengths**:
- Real-time data collection approach
- Sliding window technique for continuous stream processing
- Multiple activity scenarios tested
- Adequate sampling rate for WiFi CSI

**Limitations**:
- Very small dataset sizes (especially for deep learning)
- Limited number of activity types (3 activities)
- No demographic information about participants
- Single hardware platform validation
- Limited environmental diversity testing

### Model Architecture Evaluation (Score: 8/10)

#### Core System Components

**1. System Pipeline**:
```
Real-time CSI Stream → Sliding Window Capture → CWT Transformation →
CSI-to-Image Conversion → Mask R-CNN Object Detection →
Activity Classification + Localization + Instance Segmentation
```

**2. Signal Processing Framework**:
- **CSI Collection**: Real-time stream processing with sliding windows
- **Time-Frequency Analysis**: Continuous Wavelet Transform (CWT)
- **Image Transformation**: CSI signals converted to spectrograms
- **Power Profile Exploitation**: Energy band tracking for activity boundaries

**3. Deep Learning Architecture - Mask R-CNN**:
- **Backbone**: ResNet-50 with Feature Pyramid Network (FPN)
- **Region Proposal Network (RPN)**: Sliding window-based anchor generation
- **RoIAlign**: Fixed-size feature map generation with misalignment elimination
- **Multi-task Learning**: Classification + Bounding Box Regression + Instance Segmentation
- **Loss Function**: Combined softmax loss + regression loss + mask loss

#### Technical Innovation Assessment
**Key Innovations**:
- First WiFi CSI-based real-time object detection approach for HAR
- Novel application of CWT for CSI-to-image transformation
- Instance segmentation for multiple concurrent activities
- Power profile-based activity boundary detection

**Mathematical Formulation**:
- **CWT Definition**: CWT(t,ω) = (ω/ω₀)^(1/2) ∫ s(t')Ψ*[(ω/ω₀)(t'-t)]dt'
- **Bounding Box Regression**: Minimizes sum of squares loss with L2 regularization
- **Loss Function**: L = L_cls + L_bbox + L_mask

### Results Assessment (Score: 6/10)

#### Performance Metrics Analysis

**Single Activity Performance**:
- **Run Activity**:
  - Validation: AP₅₀ = 99.55%, AP₇₅ = 87.45%, AP = 73.65%
  - Test: AP₅₀ = 100%, AP₇₅ = 72.95%, AP = 66.55%
  - mAP: 63.97% (test)

- **Walk Activity**:
  - Validation: AP₅₀ = 100%, AP₇₅ = 60.30%, AP = 60.34%
  - Test: AP₅₀ = 99.96%, AP₇₅ = 81.48%, AP = 63.00%
  - mAP: 55.37% (test)

**Multiple Activity Performance**:
- **Combined (Walk-Wave-Run)**:
  - Validation: AP₅₀ = 96.94%, AP₇₅ = 62.99%, AP = 58.05%
  - Test: AP₅₀ = 93.81%, AP₇₅ = 83.00%, AP = 64.67%
  - **Average Classification Accuracy**: 93.80%
  - **Instance Segmentation Accuracy**: 90.73%

**Comparative Performance**:
- **vs Non-real-time models**: 0.061 accuracy reduction on average
- **Real-time vs Offline**: Trade-off between real-time capability and accuracy

#### Statistical Analysis Quality
**Evaluation Protocol**:
- **Training Configuration**: 1500 epochs with evaluation every 500 steps
- **Transfer Learning**: Pre-trained ResNet-50 weights
- **Performance Metrics**: IoU-based AP, mAP, recall
- **Validation Approach**: Separate validation and test sets

**Statistical Rigor Issues**:
- No confidence intervals or statistical significance testing
- Very small test sets (12-62 instances)
- No cross-validation methodology
- Limited baseline comparisons

### Experimental Design Quality (Score: 6/10)

#### Methodological Strengths
1. **Real-time Focus**: First work addressing real-time CSI-based activity recognition
2. **Novel Problem Formulation**: Object detection approach for activity localization
3. **Multi-task Learning**: Simultaneous classification, localization, and segmentation
4. **Practical Implementation**: Real hardware setup with streaming data

#### Experimental Limitations
1. **Limited Scale**: Very small datasets inadequate for deep learning validation
2. **Single Environment**: No cross-domain evaluation
3. **Limited Baselines**: Minimal comparison with existing methods
4. **Incomplete Analysis**: Missing ablation studies and component analysis
5. **Hardware Dependency**: Single platform validation only

#### Missing Critical Evaluations
- No latency analysis for real-time performance claims
- No computational complexity evaluation
- No robustness testing across different environments
- No analysis of sliding window parameters impact
- No comparison with traditional CSI-based HAR methods

### Reproducibility Evaluation (Score: 4/10)

#### Implementation Details
**Provided Information**:
- **Hardware Setup**: Specific device models and configurations
- **Software Environment**: OS, kernel modifications, CSI collection tools
- **Training Details**: Architecture, epochs, evaluation frequency
- **Framework**: PyTorch implementation with Google Colab

**Missing Critical Elements**:
- **Code Availability**: No public repository or implementation details
- **Hyperparameters**: Learning rates, batch sizes, optimization details missing
- **Preprocessing Steps**: Exact CWT parameters and image conversion details
- **Network Architecture**: Specific layer configurations and modifications
- **Data Collection Protocol**: Detailed subject instructions and environment setup

#### Reproducibility Score: 4/10
**Strengths**: Basic hardware and framework information provided
**Critical Gaps**: No code availability, incomplete methodology details, missing hyperparameters

### Discussion Analysis (Score: 7/10)

#### Technical Insights
The authors provide good discussion of the motivation for real-time processing and the challenges of streaming CSI data analysis. The explanation of why traditional offline approaches fail in real-time scenarios is well articulated.

#### Limitation Acknowledgment
**Explicitly Acknowledged**:
- Small dataset sizes
- Limited activity types
- Single environment testing
- Accuracy trade-offs vs non-real-time approaches

**Not Addressed**:
- Computational requirements for real-time deployment
- Scalability to more participants or activities
- Cross-domain generalization challenges
- Practical deployment considerations

#### Future Work Direction
The authors identify specific areas for improvement including sliding window parameter optimization and backbone network alternatives.

### Experimental Quality Rating

#### Overall Experimental Score: 6.3/10

**Component Scores**:
- **Dataset Quality**: 7/10
- **Model Architecture**: 8/10
- **Results Analysis**: 6/10
- **Experimental Design**: 6/10
- **Reproducibility**: 4/10
- **Discussion Quality**: 7/10

#### Strengths Summary
1. **Novel Problem Approach**: First real-time object detection for CSI-based HAR
2. **Technical Innovation**: CWT-based CSI-to-image transformation
3. **Practical Relevance**: Addresses real-world deployment challenges
4. **Multi-task Learning**: Comprehensive activity analysis (classification + localization + segmentation)

#### Critical Weaknesses
1. **Insufficient Dataset Scale**: Deep learning validation with inadequate data
2. **Limited Experimental Scope**: Single environment, few activities, small test sets
3. **Missing Reproducibility Elements**: No code, incomplete methodology details
4. **Inadequate Baseline Comparisons**: Limited comparative evaluation
5. **No Computational Analysis**: Missing real-time performance characterization

### Impact and Significance

This work represents an important first step toward real-time CSI-based activity recognition using object detection frameworks. However, the experimental validation is insufficient to support the strong claims about real-time performance and practical applicability.

### Recommendations for Future Work

1. **Dataset Expansion**: Collect larger-scale datasets with more participants and activities
2. **Cross-Domain Evaluation**: Test across different environments and hardware setups
3. **Computational Analysis**: Provide detailed latency and throughput measurements
4. **Comparative Evaluation**: Compare with established CSI-based HAR methods
5. **Code Release**: Provide open-source implementation for reproducibility
6. **Ablation Studies**: Analyze component contributions and parameter sensitivity

---

**Analysis Completed**: September 14, 2025
**Quality Assessment**: Moderate experimental validation with significant limitations in scale and scope
**Reproducibility Status**: Poor - insufficient implementation details and no code availability
**Overall Contribution**: Important problem formulation with limited experimental validation