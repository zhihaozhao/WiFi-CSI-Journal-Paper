# Paper 117: Real-time Object Detection for WiFi CSI-based Multiple Human Activity Recognition - Experimental Analysis

**ExperimentAgent1 Analysis Report**
**Date:** September 14, 2025
**Paper ID:** 117
**Journal:** IEEE Consumer Communications & Networking Conference (CCNC)
**Year:** 2023

## Paper Overview
- **Title:** A Real-time Object Detection for WiFi CSI-based Multiple Human Activity Recognition
- **Authors:** Israel Elujide, Jian Li, Aref Shiran, Siwang Zhou, Yonghe Liu
- **Methodology:** Real-time object detection framework using Mask R-CNN for CSI-based HAR
- **Innovation:** First WiFi CSI-based real-time multiple activity recognition system

## Experimental Section Analysis

### 1. Dataset Analysis (Quality: 7.0/10)

**Single Activity Datasets:**
- **Run Activity Dataset:**
  - Training: 115 instances
  - Validation: 16 instances
  - Testing: 12 instances
  - Total: 143 instances

- **Walk Activity Dataset:**
  - Training: 312 instances
  - Validation: 81 instances
  - Testing: 62 instances
  - Total: 455 instances

**Multiple Activity Dataset:**
- **Combined Activities (Walk-Wave-Run):**
  - Training: 108 instances
  - Validation: 22 instances
  - Testing: 22 instances
  - Total: 152 instances
  - Activities: Hand movement, running, walking

**Hardware Setup:**
- Transmitter: Dual-band TP-Link AC1750 (2.4 GHz)
- Receiver: Laptop with Intel NIC5300
- Operating System: Ubuntu Linux 12.04 LTS with modified kernel
- Sampling Rate: 80 packets/second
- Data Split: 70% training, 15% validation, 15% testing

### 2. Experimental Design Analysis (Quality: 8.2/10)

**System Architecture:**
1. **CSI Collection Phase:** Real-time CSI data capture using sliding window
2. **CSI-to-Image Transformation:** Continuous Wavelet Transform (CWT) for time-frequency conversion
3. **Object Detection Network:** Mask R-CNN for classification and localization

**Signal Processing Pipeline:**
- **Sliding Window Capture:** Real-time stream processing
- **CWT Transformation:** Convert CSI to time-frequency domain images
- **Power Profile Exploitation:** Extract features from transformed images
- **Deep Learning Framework:** Mask R-CNN for detection and segmentation

**Network Architecture:**
- **Backbone:** ResNet-50 with Feature Pyramid Network (FPN)
- **Detection Framework:** Region Proposal Network (RPN)
- **Segmentation:** RoIAlign + Fully Convolutional Network (FCN)
- **Loss Function:** Combined classification, bounding box regression, and mask losses

### 3. Performance Metrics and Results (Quality: 8.0/10)

**Single Activity Results:**
- **Run Activity:**
  - Validation: AP@0.5=99.55%, AP@0.75=87.45%, AP=73.65%
  - Testing: AP@0.5=100%, AP@0.75=72.95%, AP=66.55%
  - mAP: 67.07% (validation), 63.97% (testing)

- **Walk Activity:**
  - Validation: AP@0.5=100%, AP@0.75=60.30%, AP=60.34%
  - Testing: AP@0.5=99.96%, AP@0.75=81.48%, AP=63.00%
  - mAP: 48.31% (validation), 55.37% (testing)

**Multiple Activity Results:**
- **Walk-Wave-Run Combined:**
  - Validation: AP@0.5=96.94%, AP@0.75=62.99%, AP=58.05%
  - Testing: AP@0.5=93.81%, AP@0.75=83.00%, AP=64.67%
  - Individual mAP: Run=53.27%, Walk=62.77%, Wave=73.37%

**Real-time Performance:**
- Average Classification Accuracy: 93.80%
- Instance Segmentation Accuracy: 90.73%
- Real-time processing capability demonstrated

### 4. Statistical Methodology Analysis (Quality: 7.5/10)

**Training Protocol:**
- Training Duration: 1500 epochs per model
- Evaluation Frequency: Every 500 steps on validation data
- Transfer Learning: Pre-trained ResNet-50 weights used
- Detection Threshold: 85% for RoI classification
- Loss Function: Multi-task loss combining classification, regression, and segmentation

**Evaluation Metrics:**
- **Intersection over Union (IoU):** Area overlap ratio
- **mean Average Precision (mAP):** Average IoU across all classes
- **Average Precision (AP):** At different IoU thresholds (0.5, 0.75, 0.5-0.95)

**Validation Strategy:**
- Fixed train/validation/test split (70/15/15)
- Performance evaluation on both validation and test sets
- Comparison with non-real-time baselines

### 5. Reproducibility Assessment (Quality: 6.5/10)

**Available Information:**
- ✓ Hardware specifications clearly described
- ✓ Network architecture details provided
- ✓ Training parameters specified
- ✓ Data collection protocol described
- ✓ Performance metrics comprehensively reported

**Missing Information:**
- ✗ Source code not publicly available
- ✗ Dataset not publicly released
- ✗ Specific CWT parameters not detailed
- ✗ Exact sliding window parameters unclear
- ✗ Environmental setup details insufficient
- ✗ Random seed information not provided

**Reproducibility Challenges:**
- Custom dataset with limited description
- Real-time system implementation complexity
- Hardware-dependent CSI measurements
- Missing implementation details for CWT transformation

### 6. Experimental Strengths

1. **Real-time Focus:** First WiFi CSI-based real-time multiple activity recognition system
2. **Novel Approach:** Object detection framework applied to CSI activity recognition
3. **Comprehensive Evaluation:** Both single and multiple activity scenarios tested
4. **Practical System:** Addresses real-world streaming data challenges
5. **Multiple Metrics:** IoU, mAP, and segmentation accuracy evaluated
6. **Baseline Comparison:** Comparison with non-real-time methods provided

### 7. Experimental Limitations

1. **Limited Dataset Scale:** Small number of participants and activities
2. **Simple Activities:** Only basic activities tested (walk, run, hand wave)
3. **Controlled Environment:** Single indoor setup with fixed hardware
4. **Small Sample Size:** Very limited test instances (12-62 per activity)
5. **No Cross-domain Evaluation:** Single environment testing only
6. **Missing Statistical Analysis:** No significance tests or confidence intervals

### 8. Technical Innovation Assessment

**Novel Contributions:**
- Real-time CSI activity recognition using object detection
- CWT-based CSI-to-image transformation for streaming data
- Mask R-CNN application to WiFi CSI activity segmentation
- Multi-activity detection and localization in continuous streams

**Technical Soundness:**
- Well-motivated approach to real-time challenges
- Appropriate use of object detection framework
- Comprehensive loss function for multi-task learning
- Reasonable performance evaluation methodology

## Overall Experimental Quality Score: 7.4/10

### Scoring Breakdown:
- **Dataset Quality:** 7.0/10 (Limited scale but appropriate for proof-of-concept)
- **Experimental Design:** 8.2/10 (Novel approach, well-structured pipeline)
- **Performance Metrics:** 8.0/10 (Comprehensive metrics, good evaluation)
- **Statistical Methodology:** 7.5/10 (Adequate validation, missing significance tests)
- **Reproducibility:** 6.5/10 (Good documentation, missing implementation details)
- **Technical Innovation:** 8.0/10 (First real-time system, novel application of object detection)

### Recommendations for Improvement:
1. Increase dataset scale with more participants and activities
2. Evaluate cross-domain generalization capability
3. Provide detailed CWT implementation parameters
4. Include statistical significance testing
5. Release source code and dataset for reproducibility
6. Test with more complex activities and environments
7. Compare with more baseline methods
8. Include computational complexity analysis

### Verdict:
This paper presents an innovative approach to real-time WiFi CSI-based activity recognition using object detection frameworks. The experimental design addresses an important gap in existing research by focusing on real-time streaming data. While the technical approach is sound and the results are promising, the experimental evaluation is limited by small dataset scale and lack of cross-domain validation. The work represents a valuable contribution as a proof-of-concept for real-time CSI-based activity recognition, but requires more comprehensive evaluation for practical deployment.