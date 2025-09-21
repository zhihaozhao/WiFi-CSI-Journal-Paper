# A Taxonomy of WiFi Sensing: CSI vs Passive WiFi Radar - Experimental Analysis

## Basic Information
- **Paper ID**: 118
- **Title**: A Taxonomy of WiFi Sensing: CSI vs Passive WiFi Radar
- **Authors**: W. Li, M. J. Bocus, C. Tang, S. Vishwakarma, R. J. Piechocki, K. Woodbridge, K. Chetty
- **Publication**: 2020 IEEE Globecom Workshops (GC Wkshps)
- **DOI**: 10.1109/GCWkshps50303.2020.9367546
- **Analysis Date**: 2025-09-14
- **Analyzed by**: experimentAgent1

## Experimental Framework Analysis

### Dataset Analysis (Score: 6/10)

#### Dataset Collection Methodology
The paper presents a comparative experimental study using simultaneous data collection from two different WiFi sensing systems:

**Data Collection Setup**:
- **Participants**: 5 volunteers of different age groups
- **Activities**: 6 different activity classes
  - Walking
  - Sitting
  - Standing from chair
  - Laying down
  - Standing from floor
  - Picking up small items from floor
- **Total Samples**: 1,122 data samples
- **Window Length**: 4-second sliding window applied to Doppler spectrograms
- **Monitoring Area**: 3m × 3m with computers and furniture in surroundings
- **Measurement Positions**: 9 positions tested with 1.5m separation

**System Configurations**:
- **Frequency Band**: 2.4 GHz (systems on different channels to avoid interference)
- **CSI System**: Intel 5300 NIC with 1 kHz packet rate, 1×3×30 antenna configuration
- **PWR System**: USRP-2921 Software-Defined Radio platform
- **Geometric Layouts**: 3 different transmitter-receiver configurations
  - Layout 1: Forward scatter (Line-of-Sight, ~180°)
  - Layout 2: Bistatic configuration (~90°)
  - Layout 3: Monostatic configuration (<45°)

#### Data Quality Assessment
**Strengths**:
- Simultaneous synchronized measurements from both systems
- Multiple geometric configurations tested
- Reasonable number of participants and activities
- Real-world environment with realistic interference

**Limitations**:
- Relatively small dataset (1,122 samples total)
- Limited number of participants (5 subjects)
- No demographic details provided
- Single environment testing
- No cross-domain validation

### Model Architecture Evaluation (Score: 7/10)

#### System Architectures

**CSI System Processing Pipeline**:
1. **Raw CSI Data Collection**: Intel 5300 NIC captures CSI from WiFi preambles
2. **Denoising**: Discrete Wavelet Transform (DWT) + median filtering
3. **Dimension Reduction**: Principal Component Analysis (PCA)
   - Reduces 90k complex values/second to 5 principal components
   - Discards first component (contains static reflection noise)
4. **Spectrogram Generation**: Short-Time Fourier Transform (STFT)

**PWR System Processing Pipeline**:
1. **Raw Signal Capture**: USRP-2921 captures entire WiFi signal
2. **Cross Ambiguity Function (CAF)**: Generates range-Doppler surface
3. **CLEAN Algorithm**: Suppresses direct signal interference
4. **Constant False Alarm Rate (CFAR)**: Noise reduction and detection

#### Technical Innovation Assessment
**Novel Aspects**:
- First comprehensive comparison between CSI and PWR systems
- Simultaneous synchronized data collection methodology
- Analysis of geometric configuration impact on performance
- Comparative Doppler signature analysis

**Architecture Strengths**:
- Well-designed dual-system comparison framework
- Appropriate signal processing techniques for each system
- Comprehensive coverage of different geometric scenarios

### Results Assessment (Score: 5/10)

#### Performance Metrics Analysis

**Classification Performance**:
- **Overall CSI System Accuracy**: 67.3%
- **Overall PWR System Accuracy**: 66.7%
- **Classifier**: Simple 2D CNN (1 conv layer + 1 max-pooling + 2 FC layers)

**Per-Activity Performance**:
- **Walking (Activity 1)**: >90% accuracy for both systems
- **Picking up (Activity 6)**: >70% accuracy for both systems
- **Other activities**: Relatively low accuracy (varies by system and layout)

**Layout-Specific Performance**:
- **CSI System**:
  - Best: Layout 1 (LoS) - 90% accuracy
  - Worst: Layout 3 (Monostatic) - 62% accuracy
- **PWR System**:
  - Best: Layout 3 (Monostatic) - 91.3% accuracy
  - Worst: Layout 1 (LoS) - 60% accuracy

#### Statistical Analysis Quality
**Evaluation Protocol**:
- **Data Split**: 80% training, 20% testing (randomly selected)
- **Performance Metrics**: Confusion matrices, accuracy per layout
- **Cross-validation**: Not explicitly mentioned

**Statistical Rigor Issues**:
- No confidence intervals reported
- No statistical significance testing
- Small dataset size limits reliability
- Single train-test split evaluation

### Experimental Design Quality (Score: 7/10)

#### Methodological Strengths
1. **Novel Comparative Framework**: First direct comparison between CSI and PWR systems
2. **Synchronized Data Collection**: Both systems operated simultaneously
3. **Multiple Geometric Configurations**: Comprehensive layout analysis
4. **Real-World Setting**: Realistic environment with furniture and obstacles

#### Experimental Design Features
**Geometric Analysis**:
- Systematic evaluation of transmitter-receiver geometries
- Clear demonstration of layout-dependent performance
- Doppler signature analysis across different configurations

**Signal Processing Comparison**:
- Detailed analysis of time-domain and frequency-domain differences
- Comprehensive signal processing pipeline documentation
- Clear explanation of each system's strengths and limitations

#### Design Limitations
1. **Limited Dataset Scale**: Small sample size for deep learning validation
2. **Simple Classifier**: Basic CNN architecture may not fully exploit system capabilities
3. **Single Environment**: No cross-domain or environmental robustness testing
4. **No Fusion Evaluation**: Despite mentioning fusion potential, no implementation provided

### Reproducibility Evaluation (Score: 6/10)

#### Implementation Details
**Provided Information**:
- **Hardware Specifications**: Clear description of Intel 5300 NIC and USRP-2921 setup
- **Signal Processing**: Detailed mathematical formulations for both systems
- **Experimental Setup**: Layout descriptions and measurement protocols
- **Parameters**: Window sizes, packet rates, frequency bands specified

**Missing Elements**:
- **Code Availability**: No mention of public implementation
- **Detailed CNN Architecture**: Insufficient classifier specification
- **Hyperparameters**: Learning rates, training details missing
- **Data Availability**: No indication of dataset release

#### Reproducibility Score: 6/10
**Strengths**: Good hardware and signal processing documentation
**Weaknesses**: Missing implementation details and data availability

### Discussion Analysis (Score: 8/10)

#### Technical Insights
The paper provides excellent analysis of the fundamental differences between CSI and PWR systems:

**CSI System Characteristics**:
- Uses only WiFi preamble signals
- Operates at subcarrier level with fine-grained features
- Better performance in Line-of-Sight configurations
- Cannot determine movement direction due to short integration time

**PWR System Characteristics**:
- Uses entire WiFi signal including time gaps
- Treats OFDM signal as single entity
- Better performance in monostatic configurations
- Can determine velocity and direction due to longer integration time

#### Limitation Acknowledgment
**Well Addressed**:
- Geometric dependency limitations clearly discussed
- Dataset size constraints acknowledged
- Performance comparison with prior work contextualized
- System coverage limitations explicitly stated

#### Future Work Direction
The authors provide clear directions for improvement including multi-channel systems and CSI-PWR fusion approaches.

### Experimental Quality Rating

#### Overall Experimental Score: 6.5/10

**Component Scores**:
- **Dataset Quality**: 6/10
- **Model Architecture**: 7/10
- **Results Analysis**: 5/10
- **Experimental Design**: 7/10
- **Reproducibility**: 6/10
- **Discussion Quality**: 8/10

#### Strengths Summary
1. **Novel Comparative Study**: First comprehensive CSI vs PWR comparison
2. **Synchronized Measurements**: Rigorous simultaneous data collection
3. **Geometric Analysis**: Thorough evaluation of layout dependencies
4. **Signal Processing Documentation**: Detailed mathematical formulations
5. **Practical Insights**: Clear identification of system strengths and limitations

#### Critical Weaknesses
1. **Limited Dataset Scale**: Insufficient data for robust deep learning validation
2. **Simple Classification**: Basic CNN doesn't fully exploit system capabilities
3. **No Cross-Domain Testing**: Single environment limits generalizability
4. **Missing Statistical Analysis**: No significance testing or confidence intervals
5. **Low Overall Accuracy**: Performance below typical HAR system standards

### Impact and Significance

This work provides important foundational insights for WiFi sensing system selection and design. The systematic comparison reveals complementary strengths that could guide future fusion approaches. However, the experimental validation is limited by small dataset scale and simplified classification methodology.

### Recommendations for Future Work

1. **Dataset Expansion**: Collect larger-scale datasets across multiple environments
2. **Advanced Classification**: Implement state-of-the-art deep learning architectures
3. **Fusion Implementation**: Develop and evaluate CSI-PWR fusion systems
4. **Cross-Domain Validation**: Test across different environments and hardware platforms
5. **Statistical Analysis**: Include proper significance testing and confidence intervals
6. **Multi-Channel Systems**: Implement spatially distributed receiver configurations

---

**Analysis Completed**: September 14, 2025
**Quality Assessment**: Moderate experimental validation with important comparative insights but limited by scale and methodology
**Reproducibility Status**: Moderate - good signal processing documentation but missing implementation details
**Overall Contribution**: Important comparative study providing foundation for WiFi sensing system understanding and future fusion approaches