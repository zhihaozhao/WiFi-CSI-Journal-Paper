# Paper 118: Taxonomy of WiFi Sensing: CSI vs Passive WiFi Radar - Experimental Analysis

**ExperimentAgent1 Analysis Report**
**Date:** September 14, 2025
**Paper ID:** 118
**Journal:** IEEE Globecom Workshops (GC Wkshps)
**Year:** 2020

## Paper Overview
- **Title:** A Taxonomy of WiFi Sensing: CSI vs Passive WiFi Radar
- **Authors:** W. Li, M. J. Bocus, C. Tang, S. Vishwakarma, R. J. Piechocki, K. Woodbridge, K. Chetty
- **Methodology:** Comparative study between CSI and Passive WiFi Radar (PWR) systems
- **Innovation:** First comprehensive comparison of CSI vs PWR for activity recognition

## Experimental Section Analysis

### 1. Dataset Analysis (Quality: 8.0/10)

**Dataset Characteristics:**
- **Total Samples:** 1,122 data samples
- **Participants:** 5 volunteers of different age groups
- **Activities:** 6 classes (walking, sitting, standing from chair, laying down, standing from floor, picking up items)
- **Window Size:** 4-second sliding window
- **Environments:** 3m × 3m monitoring area with computers and furniture
- **Positions:** 9 test positions with 1.5m separation

**Activity Collection Protocol:**
- Activities performed in random fashion
- No specific orientation requirement relative to receiver
- Each activity captured simultaneously by both systems
- Real environment with realistic furniture and obstacles

**Hardware Setup:**
- **CSI System:** Intel 5300 Network Interface Card (NIC)
- **PWR System:** USRP-2921 Software-Defined-Radio (SDR)
- **Frequency Band:** 2.4 GHz (different channels to avoid interference)
- **CSI Packet Rate:** 1 kHz
- **Data Split:** 80% training, 20% testing

### 2. Experimental Design Analysis (Quality: 9.5/10)

**Novel Comparative Framework:**
Three distinct geometric layouts tested:
- **Layout 1 (LoS):** Forward scatter, transmitter-object-receiver alignment ≈ 180°
- **Layout 2 (Bistatic):** Transmitter-object-receiver ≈ 90°
- **Layout 3 (Monostatic):** Transmitter-object-receiver < 45°

**CSI Signal Processing Pipeline:**
1. **Denoising:** Discrete Wavelet Transform (DWT) + median filtering
2. **Dimension Reduction:** Principal Component Analysis (PCA) - 6 components (discard 1st)
3. **Spectrogram Generation:** Short-Time Fourier Transform (STFT)

**PWR Signal Processing Pipeline:**
1. **Cross Ambiguity Function (CAF):** Generate range-Doppler surface
2. **CLEAN Algorithm:** Direct signal interference cancellation
3. **CFAR:** Constant False Alarm Rate for noise reduction

**Simultaneous Data Collection:**
- Both systems operated concurrently with synchronized measurements
- Same signal source but different processing mechanisms
- Different channels used to avoid interference

### 3. Performance Metrics and Results (Quality: 8.5/10)

**Overall Classification Results:**
- **CSI System Accuracy:** 67.3% (combined layouts)
- **PWR System Accuracy:** 66.7% (combined layouts)
- **Classifier:** Simple 2D CNN (1 conv layer + 1 max-pooling + 2 FC layers)

**Layout-Specific Performance:**
- **Layout 1 (LoS):**
  - CSI: 90% accuracy
  - PWR: 60% accuracy
  - **CSI superior in forward scatter**

- **Layout 2 (Bistatic):**
  - CSI: ~70% accuracy
  - PWR: ~70% accuracy
  - **Similar performance**

- **Layout 3 (Monostatic):**
  - CSI: 62% accuracy
  - PWR: 91.3% accuracy
  - **PWR superior in monostatic configuration**

**Activity-Specific Results:**
- **Best Performance:** Walking activity (>90% both systems)
- **Second Best:** Picking up activity (>70% both systems)
- **CSI Weakest:** Standing activities (activities 3,5)
- **PWR Weakest:** Sitting and laying activities (activities 2,4)

### 4. Statistical Methodology Analysis (Quality: 7.5/10)

**Experimental Design:**
- **Validation:** Fixed 80/20 train-test split
- **Evaluation Metrics:** Classification accuracy, confusion matrices
- **Comparison Framework:** Direct performance comparison on identical dataset

**Signal Processing Validation:**
- **CSI:** Principal component selection (5 components capturing 70-80% variance)
- **PWR:** CAF with CLEAN algorithm validation
- **Spectrogram Generation:** STFT with appropriate windowing

**Statistical Rigor:**
- Multiple subjects and activities tested
- Different geometric configurations evaluated
- Confusion matrices provided for detailed analysis

### 5. Reproducibility Assessment (Quality: 8.0/10)

**Available Information:**
- ✓ Complete signal processing pipeline descriptions
- ✓ Hardware specifications clearly stated
- ✓ Experimental layout diagrams provided
- ✓ Dataset collection protocol described
- ✓ Performance results comprehensively reported
- ✓ Signal processing parameters specified

**Missing Information:**
- ✗ Dataset not publicly available
- ✗ Source code not provided
- ✗ Specific CNN architecture parameters
- ✗ Random seed information
- ✗ Exact DWT and PCA parameter settings

**Reproducibility Factors:**
- Well-documented hardware platforms (Intel 5300, USRP-2921)
- Clear signal processing descriptions
- Standard algorithms used (DWT, PCA, STFT, CAF)
- Detailed experimental setup diagrams

### 6. Experimental Strengths

1. **Novel Comparative Study:** First comprehensive comparison of CSI vs PWR
2. **Simultaneous Data Collection:** Synchronized measurements from both systems
3. **Multiple Geometric Configurations:** Three distinct transmitter-receiver geometries
4. **Real Environment Testing:** Realistic indoor environment with furniture
5. **Comprehensive Analysis:** Doppler spectrograms and layout performance analysis
6. **Fair Comparison:** Same activities, subjects, and temporal windows
7. **Clear Insights:** Geometry-dependent performance characteristics identified

### 7. Experimental Limitations

1. **Limited Dataset Scale:** Only 1,122 samples across 5 subjects
2. **Simple Classifier:** Basic 2D CNN may not capture full potential
3. **Limited Activities:** Only 6 basic activities tested
4. **Single Environment:** Only one indoor setting tested
5. **No Cross-Domain Evaluation:** Single environment limits generalization
6. **Missing Statistical Tests:** No significance testing between systems

### 8. Technical Innovation Assessment

**Novel Contributions:**
- First systematic comparison of CSI and PWR approaches
- Identification of geometry-dependent performance characteristics
- Simultaneous data collection methodology
- Clear taxonomy of WiFi sensing approaches

**Key Insights:**
- CSI performs better in Line-of-Sight (forward scatter) configurations
- PWR performs better in monostatic/bistatic configurations
- Different Doppler signature characteristics between systems
- Complementary strengths suggest fusion potential

**Technical Soundness:**
- Appropriate signal processing for each system type
- Fair comparison methodology
- Clear performance characterization
- Well-motivated experimental design

### 9. Scientific Impact

**Research Contributions:**
- Establishes baseline comparison between major WiFi sensing approaches
- Provides guidance for system selection based on geometry
- Identifies complementary strengths for potential system fusion
- Validates both approaches in realistic conditions

**Practical Implications:**
- Layout-dependent performance guidance for system deployment
- Understanding of coverage limitations for each approach
- Foundation for hybrid system development

## Overall Experimental Quality Score: 8.4/10

### Scoring Breakdown:
- **Dataset Quality:** 8.0/10 (Good multi-subject, multi-layout design but limited scale)
- **Experimental Design:** 9.5/10 (Excellent comparative framework with novel insights)
- **Performance Metrics:** 8.5/10 (Comprehensive evaluation across multiple dimensions)
- **Statistical Methodology:** 7.5/10 (Adequate validation, missing significance tests)
- **Reproducibility:** 8.0/10 (Well-documented but missing code/data)
- **Technical Innovation:** 8.5/10 (First comprehensive comparison with valuable insights)

### Recommendations for Improvement:
1. Increase dataset scale with more participants and environments
2. Test more sophisticated classification algorithms
3. Include statistical significance testing between systems
4. Evaluate cross-domain generalization capability
5. Release dataset and source code for reproducibility
6. Test hybrid system combining both approaches
7. Include computational complexity analysis

### Verdict:
This paper presents an excellent comparative experimental study between CSI and PWR systems for WiFi sensing. The experimental design is particularly strong, providing the first systematic comparison with simultaneous data collection and multiple geometric configurations. The identification of geometry-dependent performance characteristics is a valuable contribution. The key insight that CSI excels in LoS configurations while PWR performs better in NLOS/bistatic setups provides important guidance for system selection and deployment. While the dataset scale is limited, the experimental methodology is sound and the results provide clear actionable insights for the WiFi sensing community. The work establishes an important baseline and opens possibilities for hybrid system development.