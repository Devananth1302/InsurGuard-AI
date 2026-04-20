# InsurGuard AI: Adaptive Risk Profiling & RSA-Secured Policy Analytics

## Project Overview

**InsurGuard AI** is a comprehensive Python solution for intelligent health insurance risk assessment and dynamic policy management. This system integrates four core AI/ML technologies:

1. **Deep Learning (MLP)** - Risk prediction using TensorFlow/Keras
2. **Reinforcement Learning (Q-Learning)** - Dynamic policy adjustment
3. **Cybersecurity (RSA + SHA-512)** - Data protection and fraud prevention
4. **Advanced Analytics** - Healthcare risk visualization and insights

---

## Architecture & Components

### 1. Data Engineering (`data_loader.py`)

**Purpose**: Load and preprocess insurance dataset with advanced feature engineering

**Key Features**:
- **Feature Scaling**: StandardScaler applied to BMI and Age (continuous features)
- **Categorical Encoding**: One-hot encoding for lifestyle factors (smoking, region, sex)
- **Train-Test Split**: 80-20 stratified split for model validation
- **Data Exploration**: Comprehensive statistical summaries

**Usage**:
```python
loader = InsuranceDataLoader('./data/medical_insurance.csv')
loader.load_data()
X_train, X_test, y_train, y_test, feature_names = loader.preprocess(test_size=0.2)
```

---

### 2. Deep Learning Model (`model.py`)

**Architecture**: Multi-Layer Perceptron with Batch Normalization and Dropout

```
Input (39 features)
    ↓
Dense(128, ReLU) + BatchNorm + Dropout(0.3)
    ↓
Dense(64, ReLU) + BatchNorm + Dropout(0.3)
    ↓
Dense(32, ReLU) + BatchNorm + Dropout(0.2)
    ↓
Dense(1, Linear) → Risk Score/Insurance Charge
```

**Key Technologies**:
- **Optimizer**: Adam (learning_rate=0.001)
- **Loss Function**: Mean Squared Error (MSE)
- **GPU Support**: Leverages NVIDIA GPU via `tf.device('/GPU:0')`
- **Early Stopping**: Prevents overfitting with patience=15 epochs

**Performance Metrics**:
- RMSE (Root Mean Squared Error)
- MAE (Mean Absolute Error)
- R² Score (Coefficient of Determination)

**Explainable AI (XAI)**:
```python
breakdown = model.get_risk_factors_breakdown(X_sample, feature_names)
# Returns:
# {
#   'predicted_charge': 28500.50,
#   'risk_level': 'HIGH',
#   'top_risk_factors': [
#     {'factor': 'smoker_yes', 'influence_score': 2.145},
#     {'factor': 'bmi', 'influence_score': 1.832},
#     {'factor': 'age', 'influence_score': 0.956}
#   ]
# }
```

---

### 3. Reinforcement Learning Agent (`rl_agent.py`)

**Algorithm**: Q-Learning with Epsilon-Greedy Exploration

**State Space**: Discretized features
- Age bins: 10 (18-65 years)
- BMI bins: 10 (15-55)
- Smoking status: 2 (smoker/non-smoker)

**Action Space**: Premium adjustment
- Action 0: Reduce premium by 5% (reward: cost reduction)
- Action 1: Maintain premium (neutral)
- Action 2: Increase premium by 5% (reward: profit maximization)

**Q-Learning Update**:
```
Q(s,a) ← Q(s,a) + α[r + γ·max(Q(s',a')) - Q(s,a)]
where:
  α = learning rate (0.1)
  γ = discount factor (0.95)
  r = reward (profit + satisfaction)
```

**Training Process**:
- Episodes: 20-50 per dataset
- Reward Function: Balances profit margin and customer satisfaction
- Exploration Decay: ε-greedy with ε_decay = 0.995

---

### 4. Cybersecurity Module (`security.py`)

#### RSA Asymmetric Encryption
**Protection**: User_ID and Personal_Health_Info columns

```python
security = InsurGuardSecurity(key_size=2048)

# Encrypt
encrypted_user_id = security.rsa_encrypt("USER_12345")

# Decrypt
decrypted = security.rsa_decrypt(encrypted_user_id)
```

**Specifications**:
- Algorithm: RSA-2048
- Padding: OAEP (Optimal Asymmetric Encryption Padding)
- Hash Function: SHA-256
- Encoding: Base64 for transport

#### SHA-512 Hashing
**Purpose**: Claim record integrity and fraud prevention

```python
# Generate hash
claim_hash = security.sha512_hash("Claim_2024_03_15_$5000")

# Verify integrity
is_valid = security.verify_integrity(claim_data, expected_hash)
```

**Usage**:
- Immutable claim records
- Tamper detection
- Financial audit trail

---

### 5. Analytics Dashboard (`analytics.py`)

**Visualizations**:

1. **Risk Distribution Analysis**
   - Box plots: Risk by smoking status
   - Histograms: Overall charge distribution
   - Actual vs predicted overlay

2. **Demographic Correlation**
   - Age-BMI scatter plot with charge color mapping
   - Reveals non-linear relationships

3. **Demographic Breakdown**
   - Age distribution histogram
   - BMI distribution histogram
   - Dependents (children) bar chart

4. **Regional Analysis**
   - Claims by geographic region
   - Regional sample distribution

5. **Model Performance**
   - Actual vs predicted charges
   - Residual analysis for error patterns

---

## Installation & Setup

### Prerequisites
```bash
Python 3.8+
NVIDIA CUDA Toolkit (optional, for GPU support)
```

### Install Dependencies
```bash
pip install pandas numpy scikit-learn
pip install tensorflow>=2.10.0
pip install cryptography
pip install matplotlib seaborn
```

### Project Structure
```
InsurGuard-AI/
├── data/
│   ├── medical_insurance.csv
│   └── sample_submission.csv
├── main.py                 # Orchestration
├── data_loader.py          # Data engineering
├── model.py                # Deep learning MLP
├── rl_agent.py             # Q-Learning agent
├── security.py             # RSA + SHA-512
├── analytics.py            # Visualizations
├── results/
│   ├── system_metrics.json
│   ├── rl_policy_adjustments.json
│   └── visualizations/     # PNG outputs
└── README.md               # This file
```

---

## Execution Guide

### 1. Run Full Pipeline
```bash
python main.py
```

**Output**:
- Trained DL model
- RL agent training history
- JSON results with metrics
- 5 analytical visualizations (PNG)
- Encrypted sample health data

### 2. Custom Execution (Step-by-Step)
```python
from main import InsurGuardAISystem

system = InsurGuardAISystem('./data/medical_insurance.csv', use_gpu=True)
results = system.run_full_pipeline()
system.save_results('./results')
```

### 3. Individual Risk Assessment
```python
assessment = system.get_individual_risk_assessment(
    age=35,
    bmi=28.5,
    smoker=True,
    children=2,
    region='northeast'
)
print(assessment)
```

---

## Technical Specifications

### Data Processing
| Metric | Value |
|--------|-------|
| Original Features | 7 |
| Features After Encoding | 39 |
| Training Samples | 1,063 |
| Testing Samples | 267 |
| Target Variable | Insurance Charges ($) |

### Model Hyperparameters
| Parameter | Value |
|-----------|-------|
| Input Neurons | 39 |
| Hidden Layer 1 | 128 neurons, ReLU |
| Hidden Layer 2 | 64 neurons, ReLU |
| Hidden Layer 3 | 32 neurons, ReLU |
| Optimizer | Adam (lr=0.001) |
| Loss Function | MSE |
| Batch Size | 32 |
| Epochs | 100 (with early stopping) |

### RL Agent Parameters
| Parameter | Value |
|-----------|-------|
| Algorithm | Q-Learning |
| Learning Rate (α) | 0.1 |
| Discount Factor (γ) | 0.95 |
| Initial Epsilon (ε) | 1.0 |
| Epsilon Decay | 0.995 |
| Minimum Epsilon | 0.01 |

---

## Key Innovations

### 1. **Explainable AI (XAI) - Risk Factor Breakdown**
Each prediction includes interpretable factors:
- Identifies which features contribute most to risk score
- Provides actionable insights for customer communication
- Example: "Your risk score is HIGH due to smoking status (influence: 2.145) and BMI (influence: 1.832)"

### 2. **Dual-Model Architecture**
- **Deep Learning**: Predicts baseline insurance charges with high accuracy
- **Reinforcement Learning**: Dynamically adjusts premiums based on policy objectives
- Allows profit optimization while maintaining customer satisfaction

### 3. **Enterprise-Grade Security**
- RSA-2048 encryption for PII (Personally Identifiable Information)
- SHA-512 hashing for immutable claim records
- Defense against data tampering and fraud

### 4. **Digital Pulse Analytics Engine**
- Real-time visualization of risk distributions
- Demographic correlation analysis
- Regional performance benchmarking

---

## Performance Metrics

### Expected Model Performance
- **RMSE**: $4,500-5,500 (varies by seed)
- **R² Score**: 0.75-0.80
- **MAE**: $3,000-4,000

### RL Agent Performance
- **Episodes to Convergence**: 20-30
- **Average Reward**: 150-200 per episode
- **Policy Adjustment Range**: ±5% of ML prediction

---

## Security Compliance

✅ **Data Protection**
- RSA-2048 encryption for sensitive columns
- SHA-512 integrity hashing
- No plaintext storage of health information

✅ **Audit Trail**
- Claim record hashing prevents unauthorized modifications
- Immutable transaction logs

✅ **Best Practices**
- Follows OWASP cryptographic standards
- GDPR-compliant data handling (encryption at rest)

---

## Future Enhancements

1. **Model Ensemble**
   - Combine multiple DL architectures
   - Stacking for improved R² scores

2. **Advanced RL**
   - Deep Q-Network (DQN) for policy learning
   - Multi-agent coordination for claims processing

3. **Federated Learning**
   - Privacy-preserving model training across multiple insurers
   - Secure aggregation protocols

4. **Real-time Scoring**
   - REST API for instant risk predictions
   - Batch processing pipeline for bulk assessments

---

## References

### Papers & Algorithms
- Bellman Equation: https://en.wikipedia.org/wiki/Dynamic_programming
- Q-Learning: Watkins & Dayan (1992)
- OAEP Padding: Bellare & Rogaway (1994)
- Keras Documentation: https://keras.io/

### Libraries
- **TensorFlow 2.x**: Deep learning framework
- **scikit-learn**: Preprocessing and model evaluation
- **cryptography**: Cryptographic operations
- **Seaborn**: Statistical data visualization

---

## Assignment Submission Summary

**Project**: InsurGuard AI - Adaptive Risk Profiling & RSA-Secured Policy Analytics  
**Student Role**: Senior AI Engineer & Cybersecurity Specialist  
**Submission Date**: April 2024

### Deliverables Checklist
- ✅ Modular Python code (main.py, security.py, model.py, rl_agent.py, data_loader.py, analytics.py)
- ✅ Deep Learning MLP with GPU optimization
- ✅ Reinforcement Learning Q-Learning agent
- ✅ RSA-2048 encryption for sensitive data
- ✅ SHA-512 hashing for claim integrity
- ✅ Seaborn-based analytics dashboard
- ✅ Explainable AI (Risk Factor Breakdown)
- ✅ Digital Pulse analytics summary
- ✅ Comprehensive README with technical documentation

---

## Support & Contact

For implementation questions or technical issues, refer to:
- Code comments and docstrings
- Module-level documentation
- Example usages in main.py

---

**InsurGuard AI © 2024** - Advanced Health Insurance Risk Management System
