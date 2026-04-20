# InsurGuard AI - Technical Architecture Document

## System Overview

InsurGuard AI is a comprehensive health insurance risk assessment and policy management system that integrates four complementary AI/ML technologies:

```
┌─────────────────────────────────────────────────────────────────┐
│                     INSURGUARD AI SYSTEM                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐            │
│  │ DATA ENGINE  │  │ DEEP LEARNING│  │ RL AGENT     │            │
│  │ (Pandas)     │  │ (TensorFlow) │  │ (Q-Learning) │            │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘            │
│         │                 │                  │                    │
│         └─────────────────┼──────────────────┘                    │
│                           │                                       │
│         ┌─────────────────▼─────────────────┐                    │
│         │  ORCHESTRATION (main.py)          │                    │
│         │  - Pipeline Coordination          │                    │
│         │  - Result Aggregation             │                    │
│         │  - Output Generation              │                    │
│         └─────────────────┬─────────────────┘                    │
│                           │                                       │
│  ┌────────────────────────┼─────────────────────────┐            │
│  │                        │                         │             │
│  ▼                        ▼                         ▼             │
│ SECURITY          ANALYTICS              EXPLAINABLE AI          │
│ (RSA + SHA-512)   (Seaborn)             (XAI Breakdown)          │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Module Architecture

### 1. Data Engineering Pipeline (`data_loader.py`)

**Responsibility**: Load, explore, and preprocess insurance data

**Key Classes**:
- `InsuranceDataLoader`: Main data processing class

**Data Flow**:
```
CSV File
  │
  ├─► load_data() ──────────► DataFrame (1,338 rows × 7 cols)
  │
  ├─► explore_data() ───────► Statistical summaries
  │
  └─► preprocess() ─────────► [X_train, X_test, y_train, y_test]
                │
                ├─► One-hot encoding (categorical)
                ├─► Standard scaling (numerical)
                └─► Train-test split (80-20)
```

**Preprocessing Steps**:

| Step | Input | Output | Method |
|------|-------|--------|--------|
| 1 | 7 features | Separated X/y | DataFrame operations |
| 2 | Categorical cols | One-hot encoded | `pd.get_dummies()` |
| 3 | Age, BMI | Scaled [0,1] | StandardScaler |
| 4 | Encoded data | Train/test | train_test_split(0.2) |
| Result | - | 39 features | - |

---

### 2. Deep Learning Model (`model.py`)

**Responsibility**: Build and train MLP for risk prediction

**Architecture**:
```
Input Layer (39 neurons)
    │
    ├─► Dense(128, ReLU)
    ├─► BatchNormalization
    ├─► Dropout(0.3)
    │
    ├─► Dense(64, ReLU)
    ├─► BatchNormalization
    ├─► Dropout(0.3)
    │
    ├─► Dense(32, ReLU)
    ├─► BatchNormalization
    ├─► Dropout(0.2)
    │
    └─► Dense(1, Linear) → Predicted Charge
```

**Training Loop**:
```python
for epoch in range(100):
    # Forward pass
    logits = model(X_batch)
    loss = MSE(logits, y_batch)
    
    # Backward pass
    gradients = compute_gradients(loss)
    optimizer.update_weights(gradients)
    
    # Early stopping check
    if val_loss > best_loss:
        patience -= 1
        if patience == 0:
            break
    else:
        best_loss = val_loss
```

**Key Features**:
- **Batch Normalization**: Stabilizes training by normalizing activations
- **Dropout**: Reduces overfitting (p=0.2-0.3)
- **Early Stopping**: Prevents overfitting (patience=15)
- **GPU Support**: TensorFlow automatically uses available GPU

**Loss Function**: Mean Squared Error (MSE)
$$\text{MSE} = \frac{1}{n}\sum_{i=1}^{n}(y_i - \hat{y}_i)^2$$

**Optimizer**: Adam (Adaptive Moment Estimation)
$$m_t = \beta_1 m_{t-1} + (1-\beta_1)g_t$$
$$v_t = \beta_2 v_{t-1} + (1-\beta_2)g_t^2$$
$$\theta_t = \theta_{t-1} - \frac{\alpha \cdot m_t}{\sqrt{v_t} + \epsilon}$$

---

### 3. Reinforcement Learning Agent (`rl_agent.py`)

**Responsibility**: Dynamic policy adjustment using Q-Learning

**Algorithm**: Q-Learning with Epsilon-Greedy Exploration

**State Space**:
- BMI: Discretized into 10 bins (15-55)
- Age: Discretized into 10 bins (18-65)
- Smoking: Binary (0=non-smoker, 1=smoker)
- **Total States**: 10 × 10 × 2 = 200 possible states

**Action Space**:
- Action 0: Reduce premium by 5%
- Action 1: Maintain premium
- Action 2: Increase premium by 5%

**Q-Learning Update Rule**:
$$Q(s,a) \leftarrow Q(s,a) + \alpha \left[r + \gamma \max_{a'} Q(s',a') - Q(s,a)\right]$$

Where:
- α (alpha) = learning rate = 0.1
- γ (gamma) = discount factor = 0.95
- r = reward (combination of profit and satisfaction)
- s = current state
- a = action taken

**Reward Function**:
$$\text{Reward} = \text{ProfitReward} + \text{SatisfactionReward}$$
$$= \text{ProfitMargin} \times 100 + \text{Satisfaction} \times 50$$

**Exploration Strategy**: Epsilon-Greedy
```python
if random() < epsilon:
    action = random_action()  # Explore
else:
    action = argmax(Q[state])  # Exploit
    
epsilon = max(epsilon_min, epsilon * decay)  # Decay over time
```

**Training Flow**:
```
Episode Loop (20 episodes)
  │
  ├─► For each customer:
  │   ├─► Get state (discretize BMI, age, smoking)
  │   ├─► Select action (ε-greedy)
  │   ├─► Observe reward (based on premium adjustment)
  │   ├─► Update Q-value
  │   └─► Transition to next state
  │
  └─► Decay epsilon
```

---

### 4. Security Module (`security.py`)

**Responsibility**: Protect sensitive data using encryption and hashing

#### RSA Encryption
**Purpose**: Confidentiality of User_ID and Personal_Health_Info

**Process**:
```
Plaintext
   │
   ├─► Padding: OAEP (Optimal Asymmetric Encryption Padding)
   │   └─► Adds randomness to prevent patterns
   │
   ├─► Encryption: RSA-2048
   │   └─► Ciphertext = (plaintext ^ e) mod n
   │
   └─► Encoding: Base64
       └─► Transport-safe representation
```

**Mathematical Basis**:
$$C = M^e \bmod n$$

Where:
- M = plaintext message
- e = public exponent (65537)
- n = modulus (product of two large primes)
- C = ciphertext

**Key Size**: 2048 bits ≈ 617 decimal digits
**Security**: Equivalent to 112-bit symmetric key strength

#### SHA-512 Hashing
**Purpose**: Data integrity of Claim_Records

**Process**:
```
Input Data
   │
   └─► SHA-512 Hash Function
       └─► 512-bit output (128 hex characters)
```

**Properties**:
- **Deterministic**: Same input always produces same hash
- **Avalanche Effect**: Small change → completely different hash
- **One-way**: Cannot reverse hash to get original data
- **Collision-resistant**: No two different inputs produce same hash

**Example**:
```
Input: "Claim_2024_03_15_$5000"
Hash:  "a3f1d2e5c8b9...4a7f2e1d" (128 chars)
```

---

### 5. Analytics Module (`analytics.py`)

**Responsibility**: Data visualization and business intelligence

**Visualizations**:

#### 1. Risk Distribution
- **Plot Type**: Box plot + Histogram
- **Data**: Charges by smoking status
- **Insight**: Identify high-risk segments

#### 2. Age-BMI Correlation
- **Plot Type**: Scatter plot with color gradient
- **Data**: Age vs BMI, colored by charges
- **Insight**: Non-linear risk relationships

#### 3. Demographic Breakdown
- **Plot Type**: Multiple histograms
- **Data**: Age, BMI, dependents distributions
- **Insight**: Customer segmentation

#### 4. Regional Analysis
- **Plot Type**: Box plot + Bar chart
- **Data**: Claims by geographic region
- **Insight**: Regional risk variations

#### 5. Model Performance
- **Plot Type**: Scatter + Residual plot
- **Data**: Actual vs predicted charges
- **Insight**: Model accuracy assessment

---

### 6. Main Orchestration (`main.py`)

**Responsibility**: Coordinate all components into unified pipeline

**Execution Flow**:

```
Stage 1: DATA ENGINEERING
  │
  ├─► Load medical_insurance.csv
  ├─► Explore statistics
  └─► Preprocess (encode, scale, split)
           │
           ▼
Stage 2: DEEP LEARNING
  │
  ├─► Build MLP model (39→128→64→32→1)
  ├─► Train 100 epochs with validation
  └─► Evaluate RMSE, MAE, R²
           │
           ▼
Stage 3: REINFORCEMENT LEARNING
  │
  ├─► Initialize Q-Learning agent
  ├─► Train 20 episodes
  └─► Generate policy adjustments
           │
           ▼
Stage 4: CYBERSECURITY
  │
  ├─► Demonstrate RSA encryption
  ├─► Generate SHA-512 hashes
  └─► Verify integrity checks
           │
           ▼
Stage 5: ANALYTICS
  │
  ├─► Generate 5 visualizations
  ├─► Create summary statistics
  └─► Save PNG outputs
           │
           ▼
Stage 6: EXPLAINABLE AI
  │
  ├─► Feature importance analysis
  ├─► Risk factor breakdown
  └─► Human-readable explanations
           │
           ▼
Stage 7: RESULTS
  │
  ├─► Save system_metrics.json
  ├─► Save rl_adjustments.json
  └─► Save visualizations
```

**Result Structure**:
```json
{
  "data_stats": {
    "total_features": 39,
    "training_samples": 1063,
    "testing_samples": 267
  },
  "ml_metrics": {
    "rmse": 4523.45,
    "mae": 3201.32,
    "r2_score": 0.7856
  },
  "rl_summary": {
    "episodes_trained": 20,
    "average_reward": 167.89,
    "q_table_size": 1250
  },
  "analytics_summary": {
    "average_charge": 13270.42,
    "average_age": 39.21,
    "average_bmi": 30.66
  }
}
```

---

## Data Flow Diagrams

### End-to-End Processing
```
Input Data (CSV)
  │
  ├─────────────────────────────────────────────┐
  │                                             │
  ▼                                             ▼
Preprocessing                           Raw Data Analysis
  │                                             │
  ├─► One-hot encoding                ├─► Descriptive stats
  ├─► Feature scaling                 ├─► Correlation matrix
  ├─► Train-test split                └─► Missing values
  │
  ▼
Processed Data (X_train, y_train, X_test, y_test)
  │
  ├──────────────────────────────────────────────┬──────────────────┐
  │                                              │                  │
  ▼                                              ▼                  ▼
ML Model Training                       RL Agent Training      Dashboard Data
  │                                              │                  │
  ├─► Forward pass                      ├─► State discretization   ├─► Risk plots
  ├─► Backpropagation                   ├─► Q-value updates       ├─► Demographics
  ├─► Weight updates                    └─► Policy learning       └─► Performance
  │
  ▼
Predictions (Risk Scores)
  │
  ├────────────────────────────────────────────────┐
  │                                                │
  ▼                                                ▼
RL Policy Adjustment              Explainable AI
  │                                    │
  ├─► Premium adjustment        ├─► Feature importance
  ├─► Customer satisfaction      ├─► Risk breakdown
  └─► Profit optimization         └─► Interpretability
```

---

## Security Architecture

```
User Data
  │
  ├─► User_ID
  │   │
  │   └─► RSA Encryption (Public Key)
  │       │
  │       └─► Encrypted_ID (Base64)
  │
  ├─► Health_Info
  │   │
  │   └─► RSA Encryption (Public Key)
  │       │
  │       └─► Encrypted_Health (Base64)
  │
  └─► Claim_Records
      │
      ├─► RSA Encryption
      │   └─► Encrypted_Claims
      │
      └─► SHA-512 Hash
          └─► Integrity_Hash
```

**Decryption** (requires private key):
```
Encrypted Data + Private Key ──► RSA Decryption ──► Plaintext
```

---

## Performance Characteristics

### Time Complexity
| Operation | Time | Notes |
|-----------|------|-------|
| Data loading | O(n) | Linear scan of CSV |
| Preprocessing | O(n·m) | n samples, m features |
| ML training | O(n·epochs) | Batched gradient descent |
| RL training | O(episodes·samples) | Q-table updates |
| Predictions | O(1) | Single forward pass |
| Encryption | O(log n) | RSA key size n |
| Hashing | O(n) | Message length n |

### Space Complexity
| Component | Space | Notes |
|-----------|-------|-------|
| Dataset | O(n·m) | n=1338 samples, m=39 features |
| ML model | O(m²) | Weights ≈ 10,000 parameters |
| RL Q-table | O(200·3) | States × Actions |
| Visualizations | O(1) | In-memory plots |

---

## Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Data** | Pandas, NumPy | Data manipulation, numerical computing |
| **ML** | TensorFlow/Keras | Deep learning framework |
| **RL** | NumPy | Q-table management |
| **Security** | cryptography | RSA, SHA-512 implementation |
| **Viz** | Matplotlib, Seaborn | Statistical visualization |
| **Language** | Python 3.8+ | Core implementation |

---

## Extensibility Points

### 1. Add New ML Models
```python
# Example: Replace MLP with LSTM
class RiskPredictionLSTM(RiskPredictionMLP):
    def build_model(self):
        model = keras.Sequential([
            layers.LSTM(64, input_shape=(timesteps, features)),
            layers.Dense(32, activation='relu'),
            layers.Dense(1, activation='linear')
        ])
```

### 2. Enhanced RL Algorithms
```python
# Example: Replace Q-Learning with DQN
class PolicyAdjustmentDQN(PolicyAdjustmentAgent):
    def __init__(self):
        self.dnn = DeepQNetwork()  # Neural network Q-approximator
```

### 3. Custom Visualizations
```python
# Example: Add survival analysis plot
def plot_claim_survival(self):
    # Kaplan-Meier curves by risk group
```

### 4. Alternative Encryption
```python
# Example: Use Fernet (symmetric) for faster operations
from cryptography.fernet import Fernet
cipher = Fernet(key)
encrypted = cipher.encrypt(data)
```

---

## Monitoring & Diagnostics

### Logging
- All modules use Python `logging`
- Set level to DEBUG for troubleshooting
- Includes timestamps and function names

### Metrics Collection
- ML model: RMSE, MAE, R²
- RL agent: Episode reward, Q-table size
- System: Training time, memory usage

### Validation
- Run `python test_validation.py` to verify all components
- Checks dependencies, data loading, model training
- Reports pass/fail for each module

---

## Deployment Considerations

### Production Deployment
1. **Model Serialization**: Save trained model using `model.save()`
2. **Configuration Management**: Use `config.ini` for hyperparameters
3. **API Wrapper**: Implement Flask/FastAPI for REST endpoints
4. **Monitoring**: Log predictions and decision reasons
5. **Security**: Store private keys in secure key vault

### Scalability
- **Data**: Implement distributed data loading (Spark)
- **Model**: Use model parallelism for larger architectures
- **Inference**: Deploy with TensorFlow Serving
- **RL**: Distribute episode collection across workers

---

## References

**Machine Learning**:
- Goodfellow et al. "Deep Learning" (2016)
- Kingma & Ba "Adam: A Method for Stochastic Optimization" (2014)

**Reinforcement Learning**:
- Sutton & Barto "Reinforcement Learning: An Introduction" (2018)
- Watkins & Dayan "Q-learning" (1992)

**Cryptography**:
- NIST FIPS 197: AES specification
- PKCS #1: RSA Cryptography Standard
- FIPS 180-4: SHA Hash Functions

---

**Document Version**: 1.0  
**Last Updated**: April 2024  
**Architecture**: Modular, extensible, production-ready
