# InsurGuard AI - Implementation & Integration Guide

## Table of Contents
1. [Quick Start Examples](#quick-start-examples)
2. [Component Integration](#component-integration)
3. [Advanced Usage](#advanced-usage)
4. [Integration Patterns](#integration-patterns)
5. [Best Practices](#best-practices)

---

## Quick Start Examples

### Example 1: Complete Pipeline in 10 Lines

```python
from main import InsurGuardAISystem

# Run complete analysis
system = InsurGuardAISystem('./data/medical_insurance.csv', use_gpu=False)
results = system.run_full_pipeline()

# Save results
system.save_results('./results')

print(f"R² Score: {results['ml_metrics']['r2_score']:.4f}")
print(f"RL Episodes: {results['rl_summary']['episodes_trained']}")
```

**Output**:
```
========================================================
InsurGuard AI System Initializing
========================================================

[STAGE 1] DATA ENGINEERING
[STAGE 2] DEEP LEARNING - RISK PREDICTION MLP
[STAGE 3] REINFORCEMENT LEARNING - POLICY ADJUSTMENT
[STAGE 4] CYBERSECURITY - DATA PROTECTION
[STAGE 5] ANALYTICS - VISUALIZATION & INSIGHTS
[STAGE 6] EXPLAINABLE AI - RISK FACTOR BREAKDOWN
[STAGE 7] DIGITAL PULSE - SYSTEM SUMMARY

InsurGuard Pipeline Completed in 45.32 seconds
```

---

### Example 2: Individual Risk Assessment

```python
from main import InsurGuardAISystem

system = InsurGuardAISystem('./data/medical_insurance.csv')
system.run_full_pipeline()

# Assess new customer
assessment = system.get_individual_risk_assessment(
    age=40,
    bmi=32.5,
    smoker=True,
    children=2,
    region='southeast'
)

print(f"Risk Level: {assessment['risk_level']}")
print(f"Base Charge: ${assessment['predicted_charge']:.2f}")
print(f"Adjusted Charge: ${assessment['policy_adjustment']['adjusted_charge']:.2f}")
print(f"Adjustment: {assessment['policy_adjustment']['policy_change']}")
```

**Output**:
```
Risk Level: HIGH
Base Charge: $28500.50
Adjusted Charge: $29932.53
Adjustment: +5.0%
```

---

### Example 3: Data Analysis Only

```python
from data_loader import InsuranceDataLoader

loader = InsuranceDataLoader('./data/medical_insurance.csv')
loader.load_data()

# Explore data
info = loader.explore_data()
print(f"Records: {info['shape'][0]}")
print(f"Features: {info['shape'][1]}")
print(f"Missing values: {info['missing']}")

# Preprocess
X_train, X_test, y_train, y_test, features = loader.preprocess()
print(f"\nTrain shape: {X_train.shape}")
print(f"Test shape: {X_test.shape}")
print(f"Features: {len(features)}")

# Statistics
stats = loader.get_feature_statistics()
print(f"\nAvg charge: ${stats['target_mean']:.2f}")
print(f"Std charge: ${stats['target_std']:.2f}")
```

---

### Example 4: Train Custom ML Model

```python
from data_loader import InsuranceDataLoader
from model import RiskPredictionMLP

# Load and preprocess
loader = InsuranceDataLoader('./data/medical_insurance.csv')
loader.load_data()
X_train, X_test, y_train, y_test, features = loader.preprocess()

# Create model
model = RiskPredictionMLP(
    input_dim=X_train.shape[1],
    use_gpu=False
)

# Custom architecture
model.build_model(layers_config=[256, 128, 64, 32])

# Train with custom parameters
history = model.train(
    X_train, y_train,
    X_val=X_test, y_val=y_test,
    epochs=200,
    batch_size=16
)

# Evaluate
metrics = model.evaluate(X_test, y_test)
print(f"RMSE: ${metrics['rmse']:.2f}")
print(f"R² Score: {metrics['r2_score']:.4f}")

# Save model
model.save_model('./my_model.h5')
```

---

### Example 5: Encryption & Security

```python
from security import DataProtectionManager, InsurGuardSecurity

# Initialize security
manager = DataProtectionManager()

# Encrypt user information
user_id = "USER_POLICY_2024001"
encrypted_id = manager.protect_user_id(user_id)
print(f"Original: {user_id}")
print(f"Encrypted: {encrypted_id[:50]}...")

# Encrypt health data
health_data = {
    'age': 45,
    'bmi': 28.5,
    'pre_existing_conditions': ['diabetes', 'hypertension'],
    'medication_list': ['metformin', 'lisinopril']
}
encrypted_health = manager.protect_health_info(health_data)

# Protect claim records with integrity hash
claim = "Claim_2024_03_15_Emergency_Surgery_$15000_Approved"
encrypted_claim, claim_hash = manager.protect_claim_records(claim)

# Verify integrity later
is_valid = manager.verify_claim_integrity(claim)
print(f"Claim integrity valid: {is_valid}")

# Export keys for storage
security = manager.security
public_key = security.get_public_key_pem()
print(f"Public key (first 100 chars): {public_key[:100]}...")
```

---

### Example 6: RL Agent for Policy Management

```python
from rl_agent import PolicyAdjustmentAgent
import numpy as np

# Initialize agent
agent = PolicyAdjustmentAgent(
    learning_rate=0.15,
    discount_factor=0.90,
    epsilon=1.0
)

# Create training data
customers = [
    {'age': 25, 'bmi': 22.0, 'smoker': 0},
    {'age': 45, 'bmi': 28.5, 'smoker': 1},
    {'age': 65, 'bmi': 31.0, 'smoker': 0},
    {'age': 35, 'bmi': 26.5, 'smoker': 1},
]

baseline_charges = np.array([5000, 25000, 30000, 20000])

# Train agent
print("Training RL Agent...")
for episode in range(50):
    reward = agent.train_episode(customers, baseline_charges)
    
    if episode % 10 == 0:
        summary = agent.get_training_summary()
        print(f"Episode {episode}: Reward={reward:.2f}, "
              f"Avg={summary['average_reward']:.2f}")

# Use trained agent
print("\nPolicy Adjustments:")
for idx, customer in enumerate(customers):
    adjustment = agent.adjust_premium(
        customer['bmi'],
        customer['age'],
        customer['smoker'],
        baseline_charges[idx]
    )
    
    print(f"\nCustomer {idx+1} (Age={customer['age']}, BMI={customer['bmi']}):")
    print(f"  Base: ${adjustment['original_charge']:.2f}")
    print(f"  Adjusted: ${adjustment['adjusted_charge']:.2f}")
    print(f"  Action: {adjustment['action']}")
```

---

### Example 7: Generate Visualizations

```python
from analytics import InsuranceAnalyticsDashboard
from data_loader import InsuranceDataLoader
from model import RiskPredictionMLP

# Load and preprocess data
loader = InsuranceDataLoader('./data/medical_insurance.csv')
loader.load_data()
X_train, X_test, y_train, y_test, features = loader.preprocess()

# Get predictions
model = RiskPredictionMLP(X_train.shape[1])
model.build_model()
model.train(X_train, y_train, epochs=50)
predictions = model.predict(X_test)

# Create dashboard
df_processed = loader.get_preprocessed_df()
dashboard = InsuranceAnalyticsDashboard(df_processed, predictions)

# Generate all visualizations
print("Generating visualizations...")
dashboard.plot_risk_distribution()
dashboard.plot_age_bmi_correlation()
dashboard.plot_demographic_breakdown()
dashboard.plot_region_analysis()
dashboard.plot_prediction_performance(y_test.values, predictions)

# Save to files
dashboard.save_dashboard('./visualizations')
print("Saved to ./visualizations/")

# Get summary statistics
summary = dashboard.generate_summary_report()
print(f"\nDataset Summary:")
print(f"  Records: {summary['total_records']}")
print(f"  Avg Charge: ${summary['average_charge']:.2f}")
print(f"  Charge Range: ${summary['min_charge']:.2f} - ${summary['max_charge']:.2f}")
```

---

### Example 8: Explainable AI - Risk Breakdown

```python
from data_loader import InsuranceDataLoader
from model import RiskPredictionMLP

# Prepare data
loader = InsuranceDataLoader('./data/medical_insurance.csv')
loader.load_data()
X_train, X_test, y_train, y_test, features = loader.preprocess()

# Train model
model = RiskPredictionMLP(X_train.shape[1])
model.build_model()
model.train(X_train, y_train, epochs=50)

# Get detailed breakdown for a customer
sample_idx = 0
breakdown = model.get_risk_factors_breakdown(
    X_test.iloc[sample_idx].values,
    features,
    y_test.iloc[sample_idx]
)

print("=" * 60)
print("RISK ASSESSMENT REPORT")
print("=" * 60)

print(f"\nPredicted Charge: ${breakdown['predicted_charge']:.2f}")
print(f"Actual Charge: ${breakdown['actual_charge']:.2f}")
print(f"Risk Classification: {breakdown['risk_level']}")

print("\nTOP RISK FACTORS:")
for idx, factor in enumerate(breakdown['top_risk_factors'], 1):
    print(f"  {idx}. {factor['factor']}")
    print(f"     Influence Score: {factor['influence_score']:.4f}")

print("\n" + "=" * 60)
```

---

## Component Integration

### Scenario 1: ML + RL Integration

```python
from data_loader import InsuranceDataLoader
from model import RiskPredictionMLP
from rl_agent import PolicyAdjustmentAgent

# Step 1: Load data
loader = InsuranceDataLoader('./data/medical_insurance.csv')
loader.load_data()
X_train, X_test, y_train, y_test, features = loader.preprocess()

# Step 2: Train ML model
ml_model = RiskPredictionMLP(X_train.shape[1])
ml_model.build_model()
ml_model.train(X_train, y_train, epochs=100)

# Step 3: Generate baseline predictions
baseline_predictions = ml_model.predict(X_test)

# Step 4: Train RL agent with ML predictions
agent = PolicyAdjustmentAgent()

# Convert test data to customer profiles
health_profiles = []
for idx in range(min(100, len(X_test))):
    health_profiles.append({
        'age': X_test.iloc[idx]['age'] if 'age' in X_test.columns else 30,
        'bmi': X_test.iloc[idx]['bmi'] if 'bmi' in X_test.columns else 25,
        'smoker': int(X_test.iloc[idx].get('smoker_yes', 0))
    })

# Train RL on ML predictions
for episode in range(20):
    reward = agent.train_episode(health_profiles, baseline_predictions[:len(health_profiles)])

# Step 5: Generate hybrid predictions
print("Hybrid Risk Assessment (ML + RL):")
for idx in range(3):
    ml_pred = baseline_predictions[idx]
    profile = health_profiles[idx]
    
    rl_adjustment = agent.adjust_premium(
        profile['bmi'],
        profile['age'],
        profile['smoker'],
        ml_pred
    )
    
    print(f"\nCustomer {idx+1}:")
    print(f"  ML Baseline: ${ml_pred:.2f}")
    print(f"  RL Adjustment: {rl_adjustment['policy_change']}")
    print(f"  Final Premium: ${rl_adjustment['adjusted_charge']:.2f}")
```

---

### Scenario 2: Security Wrapper for Predictions

```python
from main import InsurGuardAISystem
from security import DataProtectionManager
import json

# Run system
system = InsurGuardAISystem('./data/medical_insurance.csv')
system.run_full_pipeline()

# Get assessment
assessment = system.get_individual_risk_assessment(
    age=35,
    bmi=28.5,
    smoker=True,
    children=2,
    region='northeast'
)

# Encrypt sensitive fields
security_mgr = DataProtectionManager()

# Create secure assessment record
secure_assessment = {
    'timestamp': '2024-03-15T10:30:00Z',
    'customer_id_encrypted': security_mgr.protect_user_id('CUST_12345'),
    'assessment_encrypted': security_mgr.protect_health_info(assessment),
    'risk_level': assessment['risk_level'],  # Not sensitive
}

# Hash for integrity
assessment_json = json.dumps(assessment)
_, assessment_hash = security_mgr.protect_claim_records(assessment_json)
secure_assessment['integrity_hash'] = assessment_hash

print("Secure Assessment Created")
print(f"Customer ID (encrypted): {secure_assessment['customer_id_encrypted'][:50]}...")
print(f"Risk Level: {secure_assessment['risk_level']}")
print(f"Integrity Hash: {secure_assessment['integrity_hash'][:32]}...")

# Save securely
with open('secure_assessment.json', 'w') as f:
    json.dump(secure_assessment, f)
```

---

### Scenario 3: Batch Processing Pipeline

```python
from data_loader import InsuranceDataLoader
from model import RiskPredictionMLP
from security import DataProtectionManager
import csv

# Setup
loader = InsuranceDataLoader('./data/medical_insurance.csv')
loader.load_data()
X_train, X_test, y_train, y_test, features = loader.preprocess()

model = RiskPredictionMLP(X_train.shape[1])
model.build_model()
model.train(X_train, y_train, epochs=50)

security_mgr = DataProtectionManager()

# Process batch
print("Processing batch of customers...")
results = []

for idx in range(min(50, len(X_test))):
    # Get prediction
    sample = X_test.iloc[idx].values.reshape(1, -1)
    prediction = model.predict(sample)[0]
    
    # Encrypt customer ID (would come from database)
    customer_id = f"CUST_{1000+idx}"
    encrypted_id = security_mgr.protect_user_id(customer_id)
    
    # Get risk breakdown
    breakdown = model.get_risk_factors_breakdown(
        X_test.iloc[idx].values,
        features
    )
    
    # Store result
    result = {
        'customer_id_encrypted': encrypted_id,
        'predicted_charge': prediction,
        'risk_level': breakdown['risk_level'],
        'top_factor': breakdown['top_risk_factors'][0]['factor']
    }
    results.append(result)

# Export to CSV (with encryption)
with open('batch_results.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

print(f"Processed {len(results)} customers")
print(f"Results saved to batch_results.csv")
```

---

## Advanced Usage

### Custom Model Architecture

```python
from model import RiskPredictionMLP
from data_loader import InsuranceDataLoader
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# Create subclass for custom architecture
class ResidualMLP(RiskPredictionMLP):
    def build_model(self):
        """Build MLP with residual connections"""
        with tf.device(self.device):
            inputs = layers.Input(shape=(self.input_dim,))
            
            # First block
            x = layers.Dense(128, activation='relu')(inputs)
            x = layers.BatchNormalization()(x)
            
            # Second block with residual connection
            residual = layers.Dense(128)(x)
            x = layers.Dense(128, activation='relu')(x)
            x = layers.BatchNormalization()(x)
            x = layers.Add()([x, residual])
            x = layers.ReLU()(x)
            
            # Output
            outputs = layers.Dense(1, activation='linear')(x)
            
            model = keras.Model(inputs=inputs, outputs=outputs)
            model.compile(optimizer='adam', loss='mse', metrics=['mae'])
            
            self.model = model
            return model

# Use custom architecture
loader = InsuranceDataLoader('./data/medical_insurance.csv')
loader.load_data()
X_train, X_test, y_train, y_test, features = loader.preprocess()

model = ResidualMLP(X_train.shape[1])
model.build_model()
history = model.train(X_train, y_train, epochs=50)
```

---

### RL Agent with Custom Rewards

```python
from rl_agent import PolicyAdjustmentAgent

class CustomRewardAgent(PolicyAdjustmentAgent):
    def _calculate_reward(self, predicted_charge, optimal_charge,
                         customer_satisfaction):
        """Custom reward function emphasizing profit"""
        
        # Aggressive profit maximization
        profit_margin = (optimal_charge - predicted_charge) / predicted_charge
        profit_reward = profit_margin * 200  # Weight profit more
        
        # Mild customer satisfaction penalty
        satisfaction_reward = customer_satisfaction * 10  # Lower weight
        
        # Add bonus for high premiums
        premium_bonus = (optimal_charge / 20000) * 50
        
        return profit_reward + satisfaction_reward + premium_bonus

# Use custom reward agent
agent = CustomRewardAgent()
# ... rest of training ...
```

---

### Distributed RL Training

```python
from rl_agent import PolicyAdjustmentAgent
import numpy as np

class DistributedAgent:
    """Train multiple agents and combine results"""
    
    def __init__(self, num_agents=5):
        self.agents = [PolicyAdjustmentAgent() for _ in range(num_agents)]
    
    def parallel_train(self, health_profiles, predictions, episodes=20):
        """Train agents on different data segments"""
        
        segment_size = len(health_profiles) // len(self.agents)
        
        for agent_id, agent in enumerate(self.agents):
            # Split data
            start = agent_id * segment_size
            end = start + segment_size if agent_id < len(self.agents) - 1 else len(health_profiles)
            
            segment_profiles = health_profiles[start:end]
            segment_predictions = predictions[start:end]
            
            # Train on segment
            for episode in range(episodes):
                agent.train_episode(segment_profiles, segment_predictions)
    
    def ensemble_adjust_premium(self, bmi, age, smoker, charge):
        """Get ensemble prediction"""
        adjustments = []
        for agent in self.agents:
            adj = agent.adjust_premium(bmi, age, smoker, charge)
            adjustments.append(adj['adjusted_charge'])
        
        # Average ensemble
        final_charge = np.mean(adjustments)
        return {
            'adjusted_charge': final_charge,
            'ensemble_std': np.std(adjustments)
        }
```

---

## Integration Patterns

### Pattern 1: API Service

```python
from flask import Flask, request, jsonify
from main import InsurGuardAISystem

app = Flask(__name__)
system = InsurGuardAISystem('./data/medical_insurance.csv')
system.run_full_pipeline()

@app.route('/assess', methods=['POST'])
def assess_risk():
    data = request.json
    assessment = system.get_individual_risk_assessment(
        age=data['age'],
        bmi=data['bmi'],
        smoker=data['smoker'],
        children=data.get('children', 0),
        region=data.get('region', 'northeast')
    )
    return jsonify(assessment)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
```

**Usage**:
```bash
curl -X POST http://localhost:5000/assess \
  -H "Content-Type: application/json" \
  -d '{"age": 35, "bmi": 28.5, "smoker": true, "children": 2}'
```

---

### Pattern 2: Configuration-Driven System

```python
import configparser
from main import InsurGuardAISystem

# Load config
config = configparser.ConfigParser()
config.read('config.ini')

# Create system from config
system = InsurGuardAISystem(
    config['System']['data_path'],
    use_gpu=config.getboolean('System', 'use_gpu')
)

# Run with config parameters
results = system.run_full_pipeline()

# Save to config output directory
output_dir = config['System']['output_directory']
system.save_results(output_dir)
```

---

## Best Practices

### 1. Data Validation

```python
def validate_customer_data(age, bmi, smoker, children, region):
    """Validate input before processing"""
    
    errors = []
    
    if not 18 <= age <= 100:
        errors.append("Age must be 18-100")
    
    if not 10 <= bmi <= 60:
        errors.append("BMI must be 10-60")
    
    if smoker not in [0, 1]:
        errors.append("Smoker must be 0 or 1")
    
    if not 0 <= children <= 10:
        errors.append("Children must be 0-10")
    
    valid_regions = ['northeast', 'northwest', 'southeast', 'southwest']
    if region not in valid_regions:
        errors.append(f"Region must be {valid_regions}")
    
    return len(errors) == 0, errors

# Usage
is_valid, errors = validate_customer_data(35, 28.5, 1, 2, 'northeast')
if not is_valid:
    print("Validation errors:", errors)
```

### 2. Error Handling

```python
try:
    system = InsurGuardAISystem('./data/medical_insurance.csv')
    results = system.run_full_pipeline()
except FileNotFoundError as e:
    logger.error(f"Data file not found: {e}")
except ValueError as e:
    logger.error(f"Invalid data: {e}")
except Exception as e:
    logger.error(f"Unexpected error: {e}", exc_info=True)
```

### 3. Resource Management

```python
import tensorflow as tf

# Limit GPU memory growth
gpus = tf.config.list_physical_devices('GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)

# Or use CPU only
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
```

### 4. Logging & Monitoring

```python
import logging

# Configure detailed logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('insurguard.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
logger.info("System started")
```

---

**Integration Guide Complete** ✓  
For questions, refer to README.md and ARCHITECTURE.md
