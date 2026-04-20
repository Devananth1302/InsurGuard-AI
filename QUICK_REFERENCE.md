# InsurGuard AI - Quick Reference Card

## Module Overview

### 🔧 data_loader.py
**Purpose**: Data loading and preprocessing  
**Main Class**: `InsuranceDataLoader`

| Method | Purpose | Returns |
|--------|---------|---------|
| `load_data()` | Load CSV file | DataFrame |
| `explore_data()` | Get statistics | dict with shape, dtypes, missing |
| `preprocess(test_size=0.2)` | Scale & encode | (X_train, X_test, y_train, y_test, features) |
| `get_feature_statistics()` | Feature info | dict with stats |
| `get_preprocessed_df()` | Full dataset | DataFrame |

**Example**:
```python
loader = InsuranceDataLoader('./data/medical_insurance.csv')
loader.load_data()
X_train, X_test, y_train, y_test, features = loader.preprocess()
```

---

### 🧠 model.py
**Purpose**: Deep Learning (Multi-Layer Perceptron)  
**Main Class**: `RiskPredictionMLP`

| Method | Purpose | Returns |
|--------|---------|---------|
| `build_model(layers_config=[128,64,32])` | Build MLP | keras.Model |
| `train(X_train, y_train, epochs=100)` | Train model | history dict |
| `predict(X)` | Get predictions | np.ndarray |
| `evaluate(X_test, y_test)` | Get metrics | dict {rmse, mae, r2} |
| `get_risk_factors_breakdown(X_sample, features)` | XAI | dict with top factors |
| `save_model(path)` | Save weights | None |

**Example**:
```python
model = RiskPredictionMLP(input_dim=39, use_gpu=False)
model.build_model()
history = model.train(X_train, y_train, epochs=100)
metrics = model.evaluate(X_test, y_test)
breakdown = model.get_risk_factors_breakdown(X_test[0], features)
```

**Key Functions**:
- `_classify_risk(charge)` → "LOW" | "MEDIUM" | "HIGH" | "CRITICAL"

---

### 🎮 rl_agent.py
**Purpose**: Q-Learning for policy adjustment  
**Main Class**: `PolicyAdjustmentAgent`

| Method | Purpose | Returns |
|--------|---------|---------|
| `select_action(state)` | Choose action | int (0, 1, 2) |
| `train_episode(health_metrics, predictions)` | Train one episode | float (reward) |
| `adjust_premium(bmi, age, smoker, charge)` | Get adjustment | dict with new charge |
| `get_training_summary()` | Training stats | dict with metrics |

**Example**:
```python
agent = PolicyAdjustmentAgent(learning_rate=0.1)
# Train
for episode in range(20):
    reward = agent.train_episode(customers, predictions)
# Use
adjustment = agent.adjust_premium(bmi=28.5, age=35, smoker=1, charge=25000)
print(f"Adjusted: ${adjustment['adjusted_charge']:.2f}")
```

**Key Functions**:
- `_discretize_state(bmi, age, smoker)` → tuple
- `_calculate_reward(pred, optimal, satisfaction)` → float

---

### 🔐 security.py
**Purpose**: Data encryption and integrity  
**Main Classes**: `InsurGuardSecurity`, `DataProtectionManager`

| Class | Method | Purpose | Returns |
|-------|--------|---------|---------|
| **InsurGuardSecurity** | `rsa_encrypt(plaintext)` | Encrypt data | str (Base64) |
| | `rsa_decrypt(ciphertext)` | Decrypt data | str (plaintext) |
| | `sha512_hash(data)` | Hash data | str (hex) |
| | `verify_integrity(data, hash)` | Verify hash | bool |
| **DataProtectionManager** | `protect_user_id(user_id)` | Encrypt ID | str |
| | `protect_health_info(dict)` | Encrypt health | str |
| | `protect_claim_records(claim)` | Encrypt & hash | (str, str) |

**Example**:
```python
security = InsurGuardSecurity(key_size=2048)
encrypted = security.rsa_encrypt("USER_12345")
decrypted = security.rsa_decrypt(encrypted)

manager = DataProtectionManager()
encrypted_id = manager.protect_user_id("USER_ABC")
encrypted_claim, hash_val = manager.protect_claim_records("Claim_2024_$5000")
is_valid = manager.verify_claim_integrity("Claim_2024_$5000")
```

---

### 📊 analytics.py
**Purpose**: Visualization and reporting  
**Main Class**: `InsuranceAnalyticsDashboard`

| Method | Purpose | Returns |
|--------|---------|---------|
| `plot_risk_distribution()` | Risk by smoking | plt.Figure |
| `plot_age_bmi_correlation()` | Age-BMI scatter | plt.Figure |
| `plot_demographic_breakdown()` | Age/BMI/children | plt.Figure |
| `plot_region_analysis()` | Regional claims | plt.Figure |
| `plot_prediction_performance(y_true, y_pred)` | Model performance | plt.Figure |
| `save_dashboard(output_dir)` | Save PNG files | None |
| `generate_summary_report()` | Statistics | dict |

**Example**:
```python
dashboard = InsuranceAnalyticsDashboard(df, predictions=None)
dashboard.plot_risk_distribution()
dashboard.plot_age_bmi_correlation()
dashboard.save_dashboard('./results')
summary = dashboard.generate_summary_report()
```

---

### 🚀 main.py
**Purpose**: System orchestration  
**Main Class**: `InsurGuardAISystem`

| Method | Purpose | Returns |
|--------|---------|---------|
| `run_full_pipeline()` | Execute all 7 stages | dict with results |
| `get_individual_risk_assessment(age, bmi, smoker, children, region)` | Single assessment | dict |
| `save_results(output_dir)` | Save outputs | None |

**Example**:
```python
system = InsurGuardAISystem('./data/medical_insurance.csv', use_gpu=False)
results = system.run_full_pipeline()

assessment = system.get_individual_risk_assessment(
    age=35, bmi=28.5, smoker=True, children=2, region='northeast'
)

system.save_results('./results')
```

---

## Configuration Parameters

### config.ini - Key Settings

**Data Processing**:
```ini
[DataProcessing]
test_size = 0.2
scaling_method = StandardScaler
categorical_features = sex,smoker,region
```

**Deep Learning**:
```ini
[DeepLearning]
hidden_layers = [128, 64, 32]
learning_rate = 0.001
epochs = 100
early_stopping_patience = 15
```

**RL Agent**:
```ini
[ReinforcementLearning]
learning_rate = 0.1
discount_factor = 0.95
initial_epsilon = 1.0
training_episodes = 20
```

**Security**:
```ini
[Security]
rsa_key_size = 2048
hash_function = SHA512
```

---

## Common Workflows

### Workflow 1: Full Analysis
```python
from main import InsurGuardAISystem

system = InsurGuardAISystem('./data/medical_insurance.csv', use_gpu=False)
results = system.run_full_pipeline()
system.save_results()
```

### Workflow 2: Custom ML Model
```python
from data_loader import InsuranceDataLoader
from model import RiskPredictionMLP

loader = InsuranceDataLoader('./data/medical_insurance.csv')
loader.load_data()
X_train, X_test, y_train, y_test, features = loader.preprocess()

model = RiskPredictionMLP(X_train.shape[1], use_gpu=True)
model.build_model(layers_config=[256, 128, 64])
model.train(X_train, y_train, epochs=200)
metrics = model.evaluate(X_test, y_test)
```

### Workflow 3: RL Policy Training
```python
from rl_agent import PolicyAdjustmentAgent
import numpy as np

agent = PolicyAdjustmentAgent()

# Training
for episode in range(50):
    reward = agent.train_episode(health_profiles, predictions)

# Using
adjustment = agent.adjust_premium(bmi=28.5, age=35, smoker=1, charge=25000)
```

### Workflow 4: Secure Data Protection
```python
from security import DataProtectionManager

manager = DataProtectionManager()

# Protect
encrypted_id = manager.protect_user_id("USER_12345")
encrypted_health = manager.protect_health_info({'age': 35, 'bmi': 28.5})
encrypted_claim, claim_hash = manager.protect_claim_records("Claim_$5000")

# Verify
is_valid = manager.verify_claim_integrity("Claim_$5000")
```

### Workflow 5: Generate Visualizations
```python
from analytics import InsuranceAnalyticsDashboard

dashboard = InsuranceAnalyticsDashboard(df, predictions)
dashboard.plot_risk_distribution()
dashboard.plot_age_bmi_correlation()
dashboard.plot_demographic_breakdown()
dashboard.plot_region_analysis()
dashboard.plot_prediction_performance(y_true, y_pred)
dashboard.save_dashboard('./visualizations')
```

---

## Key Parameters & Values

### Model Architecture
```
Input: 39 features (after one-hot encoding)
Layer 1: Dense(128) + ReLU + BatchNorm + Dropout(0.3)
Layer 2: Dense(64) + ReLU + BatchNorm + Dropout(0.3)
Layer 3: Dense(32) + ReLU + BatchNorm + Dropout(0.2)
Output: Dense(1) + Linear
```

### RL State Space
```
Age: 10 bins (18-65)
BMI: 10 bins (15-55)
Smoking: 2 states (yes/no)
Total: 200 states
```

### RL Action Space
```
Action 0: Reduce premium -5%
Action 1: Maintain premium (0%)
Action 2: Increase premium +5%
```

---

## Performance Benchmarks

| Metric | Value | Notes |
|--------|-------|-------|
| Data Loading | ~2 sec | 1,338 records |
| Preprocessing | ~3 sec | 7→39 features |
| ML Training | ~30 sec | 100 epochs, CPU |
| RL Training | ~5 sec | 20 episodes |
| Prediction | <1 ms | Per sample |
| Model R² | 0.75-0.80 | Test set |
| Model RMSE | $4,500-5,500 | Test set |

---

## Troubleshooting Quick Reference

| Issue | Solution |
|-------|----------|
| "No module named 'tensorflow'" | `pip install tensorflow>=2.10.0` |
| "Memory error during training" | Set `use_gpu=False` or reduce batch size |
| "Data file not found" | Check path: `./data/medical_insurance.csv` |
| "GPU not detected" | Verify CUDA/cuDNN or use CPU mode |
| "Import error: cryptography" | `pip install cryptography>=3.4.8` |
| "Seaborn plot not showing" | Add `plt.show()` or save with `savefig()` |

---

## File Locations & Outputs

```
Project Root: InsurGuard-AI/

Input:
  data/medical_insurance.csv       ← Kaggle dataset

Configuration:
  config.ini                       ← System parameters

Output (generated after run_full_pipeline):
  results/system_metrics.json      ← ML & RL metrics
  results/rl_adjustments.json      ← Policy adjustments
  results/visualizations/          ← 5 PNG plots
    ├── risk_distribution.png
    ├── age_bmi.png
    ├── demographics.png
    ├── region.png
    └── performance.png
```

---

## Quick Command Reference

```bash
# Setup
pip install -r requirements.txt

# Test
python test_validation.py

# Run
python main.py

# Custom
python -c "from main import InsurGuardAISystem; s = InsurGuardAISystem('./data/medical_insurance.csv'); s.run_full_pipeline()"
```

---

## Data Dictionary

### Input Features (medical_insurance.csv)
| Column | Type | Range | Description |
|--------|------|-------|-------------|
| age | int | 18-65 | Customer age |
| sex | str | M/F | Gender |
| bmi | float | 15-55 | Body Mass Index |
| children | int | 0-5 | Number of dependents |
| smoker | str | yes/no | Smoking status |
| region | str | 4 regions | Geographic region |
| charges | float | 1,122-63,770 | **Target**: Insurance charges |

### After Preprocessing
```
39 features created from 7 original:
- age (scaled)
- bmi (scaled)
- children (unchanged)
- sex_female (one-hot)
- sex_male (one-hot)
- smoker_no (one-hot)
- smoker_yes (one-hot)
- region_northeast (one-hot)
- region_northwest (one-hot)
- region_southeast (one-hot)
- region_southwest (one-hot)
- (+ other encoded features)
```

---

## Output Interpretation

### Model Metrics
```json
{
  "rmse": 4523.45,      // ± dollars (lower is better)
  "mae": 3201.32,       // Average error in dollars
  "r2_score": 0.7856,   // 78.56% variance explained (0-1)
  "mse": 20461589.23    // Mean squared error
}
```

### Risk Levels
- **LOW**: Charge < $10,000
- **MEDIUM**: $10,000-$20,000
- **HIGH**: $20,000-$35,000
- **CRITICAL**: > $35,000

### RL Adjustment
```json
{
  "original_charge": 25000,
  "adjusted_charge": 26250,
  "adjustment_factor": 1.05,
  "action": "INCREASE (5%)",
  "policy_change": "+5.0%"
}
```

---

## Dependencies Checklist

Essential packages:
- ✓ pandas (data)
- ✓ numpy (math)
- ✓ scikit-learn (preprocessing)
- ✓ tensorflow (ML)
- ✓ cryptography (security)
- ✓ matplotlib (plotting)
- ✓ seaborn (viz)

Check: `pip list | grep -E "pandas|numpy|tensorflow|cryptography|seaborn"`

---

**Quick Reference v1.0** | April 2024 | InsurGuard AI Project
