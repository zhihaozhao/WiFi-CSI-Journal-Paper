# Paper 116: Deep Learning Based Lightweight Human Activity Recognition System Using Reconstructed WiFi CSI - Experimental Analysis

**ExperimentAgent1 Analysis Report**
**Date:** September 14, 2025
**Paper ID:** 116
**Journal:** IEEE Transactions on Human-Machine Systems
**Year:** 2024

## Paper Overview
- **Title:** A Deep Learning Based Lightweight Human Activity Recognition System Using Reconstructed WiFi CSI
- **Authors:** Xingcan Chen, Yi Zou, Chenglin Li, Wendong Xiao
- **Methodology:** Wisor-DL system with reconstructed CSI tensor and deep learning
- **Target:** Lightweight HAR with cross-domain generalization

## Experimental Section Analysis

### 1. Dataset Analysis (Quality: 8.5/10)

**Dataset 1 (Public Dataset):**
- Source: https://github.com/ermongroup/Wifi_Activity_Recognition
- Hardware: Intel 5300 NIC, 1 kHz sampling frequency
- Activities: 6 classes (Lie down, Fall, Walk, Run, Sit down, Stand up)
- Participants: 6 volunteers
- Data Collection: 20 samples per activity per volunteer, 2-second windows
- Total Samples: 720 samples

**Dataset 2 (Office Room):**
- Environment: 4400mm × 2650mm office room
- Hardware: Commercial WiFi router (Tx), Intel 5300 NIC (Rx)
- Sampling: 500 Hz, 3.5m Tx-Rx distance, line-of-sight
- Participants: 8 volunteers
- Activities: 6 classes (Jump, Stoop, Wave hand, Fall, Sit down, Stand up)
- Data Collection: 100 samples per activity per volunteer, 15s collection with 4s sliding window
- Total Samples: 4800 samples

**Dataset 3 (Laboratory Room):**
- Environment: 4400mm × 3600mm laboratory room
- Hardware: Same as Dataset 2
- Sampling: 500 Hz, 2.5m Tx-Rx distance, line-of-sight
- Participants: 8 volunteers
- Activities: Same as Dataset 2
- Data Collection: Same protocol as Dataset 2
- Total Samples: 4800 samples

### 2. Experimental Design Analysis (Quality: 9.0/10)

**Signal Processing Pipeline:**
1. **Preprocessing:** PCA and low-pass filtering for noise reduction
2. **Sparse Signal Representation:** Subcarrier selection (10 from 30 subcarriers)
3. **CSI Tensor Construction:** Hankel matrix construction with CP decomposition
4. **Phase Difference Calculation:** Between adjacent receiving antennas
5. **Feature Fusion:** GTCN-RC for temporal feature learning
6. **Classification:** Dendrite Network (DD) for final decision

**Model Architecture:**
- Input: Reconstructed CSI phase differences and tensor peaks
- Network: Gated Temporal Convolutional Network with Residual Connections (GTCN-RC)
- Output: Dendrite Network replacing traditional dense layer
- Innovation: Lightweight design with cross-domain generalization

### 3. Performance Metrics and Results (Quality: 9.2/10)

**Recognition Accuracy Results:**
- Dataset 1: 98.44% (Wisor-DL) vs competitors (CNN: 89.32%, LSTM: 95.47%, ABLSTM: 97.55%)
- Dataset 2: 98.00% average accuracy across 6 activities
- Dataset 3: 97.57% average accuracy across 6 activities

**Computational Efficiency:**
- Training Time: 1857.44 seconds (Dataset 2)
- Testing Time: 2.81 ms per sample (real-time capable)
- Model Complexity: 16.43M parameters (lightweight compared to competitors)
- Computational Cost: 0.83 GMac operations

**Cross-Domain Generalization:**
- Dataset 2→3: 97.76% accuracy (only 0.24% degradation)
- Dataset 3→2: 97.57% accuracy (only 0.43% degradation)
- Superior to competitors: CNN (-15%), LSTM (-15%), ABLSTM (-8%), THAT (-3%)

### 4. Statistical Methodology Analysis (Quality: 8.8/10)

**Validation Protocol:**
- 10-fold cross-validation for all experiments
- Average results across all 10 runs reported
- Maximum 50 epochs training limit
- Statistical significance through confusion matrices

**Hyperparameters:**
- Xavier initialization with gain = 1
- ADAM optimizer
- Learning rate: 0.0001
- Weight decay: 0.001
- Tensor order: 3rd-order CSI tensors
- Hankel matrix: 300×300 dimensions

**Comparison Framework:**
- Baseline models: CNN, LSTM, ABLSTM, THAT, Siamese, HAR-SAnet
- Fair comparison: Same datasets, same validation protocol
- Multiple metrics: Accuracy, efficiency, cross-domain performance

### 5. Reproducibility Assessment (Quality: 7.5/10)

**Available Information:**
- ✓ Detailed model architecture descriptions
- ✓ Complete hyperparameter specifications
- ✓ Dataset collection protocols clearly described
- ✓ Hardware specifications provided
- ✓ Performance comparison with baselines

**Missing Information:**
- ✗ Source code not publicly available
- ✗ Trained model weights not shared
- ✗ Specific random seeds not mentioned
- ✗ Detailed implementation of CP decomposition
- ✗ Exact preprocessing parameters

**Reproducibility Challenges:**
- Complex tensor decomposition implementation
- Multiple signal processing stages requiring careful tuning
- Hardware-dependent CSI measurements
- Environmental sensitivity of WiFi signals

### 6. Experimental Strengths

1. **Comprehensive Evaluation:** Three different datasets with varying environments
2. **Fair Comparison:** Multiple state-of-the-art baselines using identical protocols
3. **Multiple Metrics:** Accuracy, efficiency, and cross-domain generalization
4. **Real-world Scenarios:** Office and laboratory environments with multiple participants
5. **Statistical Rigor:** 10-fold cross-validation with confusion matrix analysis
6. **Innovation Validation:** Novel components (tensor decomposition, GTCN-RC, DD) properly ablated

### 7. Experimental Limitations

1. **Limited Scale:** Only 6-8 participants per dataset
2. **Controlled Environments:** Line-of-sight conditions only
3. **Activity Scope:** Limited to 6 basic activities
4. **Hardware Dependency:** Specific to Intel 5300 NIC
5. **Missing Statistical Tests:** No significance tests between methods
6. **Reproducibility Gap:** Implementation details insufficient for full reproduction

### 8. Technical Innovation Assessment

**Novel Contributions:**
- CSI tensor construction with canonical polyadic decomposition
- Gated temporal convolutional network with residual connections
- Dendrite network for lightweight classification
- Dual-path signal reconstruction (sparse representation + tensor decomposition)

**Technical Soundness:**
- Mathematical foundations well-established
- Signal processing pipeline logically designed
- Deep learning architecture appropriately chosen
- Cross-domain generalization mechanism clearly explained

## Overall Experimental Quality Score: 8.7/10

### Scoring Breakdown:
- **Dataset Quality:** 8.5/10 (Multiple datasets, adequate size, but limited diversity)
- **Experimental Design:** 9.0/10 (Well-structured, comprehensive pipeline)
- **Performance Metrics:** 9.2/10 (Multiple relevant metrics, thorough evaluation)
- **Statistical Methodology:** 8.8/10 (Proper validation, good baselines)
- **Reproducibility:** 7.5/10 (Good documentation, but missing implementation details)
- **Technical Innovation:** 9.0/10 (Novel architecture with clear contributions)

### Recommendations for Improvement:
1. Release source code and trained models
2. Include statistical significance tests
3. Evaluate on larger-scale datasets with more participants
4. Test robustness to non-line-of-sight conditions
5. Provide more detailed implementation specifications
6. Include computational complexity analysis with theoretical bounds

### Verdict:
This paper presents a technically sound experimental evaluation of a novel WiFi CSI-based HAR system. The experimental design is comprehensive with proper baselines and multiple evaluation metrics. The cross-domain generalization results are particularly strong. However, reproducibility could be improved with better implementation details and code availability.