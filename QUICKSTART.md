# InsurGuard AI - Quick Start Guide

## 🚀 Getting Started (5 Minutes)

### Step 1: Environment Setup

#### Option A: Using Virtual Environment (Recommended)
```bash
# Navigate to project directory
cd InsurGuard-AI

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

#### Option B: Using Conda
```bash
conda create -n insurguard python=3.9
conda activate insurguard
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

**Expected output**: All packages installed successfully ✓

### Step 3: Verify GPU Support (Optional)
```python
import tensorflow as tf
print(tf.config.list_physical_devices('GPU'))
# If GPU available: [PhysicalDevice(name='/physical_device:GPU:0', ...)]
# If no GPU: []
```

### Step 4: Run the System
```bash
python main.py
```

**Expected output**:
```
========================================================
InsurGuard AI System Initializing
========================================================

[STAGE 1] DATA ENGINEERING
Loading data from ./data/medical_insurance.csv
...
Model saved to ./results/system_metrics.json
InsurGuard Pipeline Completed in 42.50 seconds
```

---

## 📊 Understanding the Output

### 1. **System Metrics** (`results/system_metrics.json`)
```json
{
  "ml_model": {
    "rmse": 4523.45,
    "mae": 3201.32,
    "r2_score": 0.7856,
    "mse": 20461589.23
  },
  "rl_agent": {
    "episodes_trained": 20,
    "average_reward": 167.89,
    "q_table_size": 1250
  },
  "xai_samples": [
    {
      "predicted_charge": 28500.50,
      "risk_level": "HIGH",
      "top_risk_factors": [...]
    }
  ]
}
```

### 2. **Visualizations** (`results/visualizations/`)
- `risk_distribution.png` - Risk by smoking status + charge distribution
- `age_bmi.png` - Age-BMI correlation heatmap
- `demographics.png` - Age, BMI, children distributions
- `region.png` - Regional claims analysis
- `performance.png` - Actual vs predicted charges

### 3. **Policy Adjustments** (`results/rl_policy_adjustments.json`)
```json
{
  "original_charge": 28500.50,
  "adjusted_charge": 29932.53,
  "adjustment_factor": 1.05,
  "action": "INCREASE (5%)",
  "policy_change": "+5.0%"
}
```

---

## 🔐 Security Demonstration

The system automatically demonstrates:

### ✅ RSA Encryption
```
[STAGE 4] CYBERSECURITY - DATA PROTECTION

RSA Encryption - User ID encrypted (sample): MIIBIjANBgkqhkiG...
RSA Encryption - Health info encrypted: AQB/qGZqw3Z...
```

### ✅ SHA-512 Integrity
```
SHA-512 Hash - Claim integrity verified: True
```

---

## 💡 Using Individual Components

### 1. Load and Explore Data
```python
from data_loader import InsuranceDataLoader

loader = InsuranceDataLoader('./data/medical_insurance.csv')
loader.load_data()
info = loader.explore_data()

# Get feature statistics
stats = loader.get_feature_statistics()
print(f"Total features: {stats['total_features_after_encoding']}")
print(f"Training samples: {stats['training_samples']}")
```

### 2. Train a Custom ML Model
```python
from data_loader import InsuranceDataLoader
from model import RiskPredictionMLP

loader = InsuranceDataLoader('./data/medical_insurance.csv')
loader.load_data()
X_train, X_test, y_train, y_test, feature_names = loader.preprocess()

# Build and train
model = RiskPredictionMLP(input_dim=X_train.shape[1], use_gpu=False)
model.build_model(layers_config=[256, 128, 64])
history = model.train(X_train, y_train, X_val=X_test, y_val=y_test, epochs=50)

# Evaluate
metrics = model.evaluate(X_test, y_test)
print(f"R² Score: {metrics['r2_score']:.4f}")

# Get predictions
predictions = model.predict(X_test)
```

### 3. Train RL Agent
```python
from rl_agent import PolicyAdjustmentAgent

agent = PolicyAdjustmentAgent(learning_rate=0.15)

# Train on your data
health_metrics = [
    {'age': 35, 'bmi': 28.5, 'smoker': 1},
    {'age': 45, 'bmi': 26.0, 'smoker': 0},
    # ... more data
]

for episode in range(50):
    reward = agent.train_episode(health_metrics, predictions)
    print(f"Episode {episode}: Reward = {reward:.2f}")

# Get policy adjustment
adjustment = agent.adjust_premium(bmi=28.5, age=35, smoker=1, predicted_charge=25000)
print(adjustment)
```

### 4. Encrypt Sensitive Data
```python
from security import DataProtectionManager

security_mgr = DataProtectionManager()

# Encrypt user ID
user_id = "USER_ABC_123"
encrypted = security_mgr.protect_user_id(user_id)

# Encrypt health information
health_info = {'age': 35, 'bmi': 28.5, 'smoker': True}
encrypted_health = security_mgr.protect_health_info(health_info)

# Protect claim with hash
claim_data = "Claim_2024_03_15_$5000_Approved"
encrypted_claim, hash_value = security_mgr.protect_claim_records(claim_data)

# Verify integrity
is_valid = security_mgr.verify_claim_integrity(claim_data)
```

### 5. Generate Visualizations
```python
from analytics import InsuranceAnalyticsDashboard
from data_loader import InsuranceDataLoader

loader = InsuranceDataLoader('./data/medical_insurance.csv')
loader.load_data()
df = loader.get_preprocessed_df()

dashboard = InsuranceAnalyticsDashboard(df, predictions=None)

# Generate individual plots
dashboard.plot_risk_distribution()
dashboard.plot_age_bmi_correlation()
dashboard.plot_demographic_breakdown()

# Save all visualizations
dashboard.save_dashboard('./my_results')
```

---

## 📈 Performance Tuning

### For Better Model Accuracy
1. **Increase training epochs**:
   ```python
   model.train(X_train, y_train, epochs=200, batch_size=16)
   ```

2. **Use larger hidden layers**:
   ```python
   model.build_model(layers_config=[256, 128, 64, 32])
   ```

3. **Enable GPU acceleration**:
   ```python
   system = InsurGuardAISystem('./data/medical_insurance.csv', use_gpu=True)
   ```

### For Faster Training
1. **Reduce batch size** (trade-off: more noise)
2. **Use fewer hidden layers**
3. **Disable GPU** if memory is limited

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'tensorflow'"
**Solution**: Install TensorFlow
```bash
pip install tensorflow>=2.10.0
```

### Issue: "GPU not detected"
**Solution**: Check CUDA compatibility
```python
import tensorflow as tf
tf.sysconfig.get_build_info()['cuda_version']
```

### Issue: "Memory error during training"
**Solution**: Reduce batch size or disable GPU
```python
system = InsurGuardAISystem('./data/medical_insurance.csv', use_gpu=False)
```

### Issue: "Data file not found"
**Ensure**: `./data/medical_insurance.csv` exists in the correct location

---

## 📚 Detailed Tutorials

### Tutorial 1: Building a Custom MLP
See [Advanced Model Training](./docs/advanced_model_training.md)

### Tutorial 2: RL Agent Customization
See [RL Agent Guide](./docs/rl_agent_guide.md)

### Tutorial 3: Security Implementation
See [Security Best Practices](./docs/security_guide.md)

---

## ✅ Verification Checklist

After running the system, verify:

- [ ] `results/system_metrics.json` exists
- [ ] 5 PNG files in `results/visualizations/`
- [ ] Model training completed (epochs finished)
- [ ] R² score between 0.70-0.85
- [ ] RL agent trained 20+ episodes
- [ ] Security encryption/hashing demonstrated
- [ ] No errors in console output

**Success Criteria**: All checkboxes marked ✓

---

## 🎯 Next Steps

1. **Explore Results**: Open PNG visualizations in image viewer
2. **Analyze Metrics**: Review `system_metrics.json` in text editor
3. **Modify Configuration**: Edit `config.ini` for custom parameters
4. **Integrate Custom Data**: Replace `medical_insurance.csv` with your own
5. **Deploy Model**: Use `model.save_model()` for production deployment

---

## 📞 Support

For issues:
1. Check README.md for comprehensive documentation
2. Review code comments and docstrings
3. Enable debug logging:
   ```python
   logging.basicConfig(level=logging.DEBUG)
   ```

---

**Happy insuring with InsurGuard AI! 🛡️**
