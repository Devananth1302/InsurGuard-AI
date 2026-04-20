# InsurGuard AI - Web Application
## Enterprise Insurance Risk Assessment System with Deep Learning & Reinforcement Learning

### 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the Flask application
python app.py

# Access the web app
# Homepage: http://localhost:5000
# Dashboard: http://localhost:5000/dashboard
# Risk Assessment: http://localhost:5000/risk-assessment
# Security Vault: http://localhost:5000/security-vault
```

---

## 📋 Project Structure

```
web_app/
├── app.py                          # Flask backend with all routes
├── requirements.txt                # Python dependencies
├── README.md                       # This file
│
├── templates/                      # HTML Templates
│   ├── index.html                 # Homepage (Cinematic Hero Section)
│   ├── dashboard.html             # Analytics Dashboard with Chart.js
│   ├── risk_assessment.html       # Risk Assessment Form & Results
│   └── security_vault.html        # Security, Encryption & Audit Logs
│
└── static/                        # Static Assets
    ├── css/
    │   └── theme.css              # Dark-mode Bootstrap 5 theme
    └── js/
        └── (chart.js included via CDN)
```

---

## 🎨 Frontend Features

### **1. Homepage (index.html)**
- **Cinematic Hero Section**: Animated gradient text with "INTRODUCING DEVANANTH: INSURGUARD AI"
- **Particle Animation**: 50+ floating particles with smooth animations
- **Feature Cards**: 6 enterprise feature cards with hover effects
- **Responsive Design**: Mobile-optimized layout
- **Glowing Effects**: Custom gradient text and shadow effects

### **2. Dashboard (dashboard.html)**
- **Real-time Statistics**: 4 key metrics (Total Policies, Avg Premium, Avg Age, Satisfaction)
- **Trend Chart**: Dual-axis line chart showing Risk Score & Premium Trends (30 days)
- **Risk Distribution**: Pie/Doughnut chart with legend
- **Performance Chart**: Bar chart comparing before/after RL optimization
- **Chart.js Integration**: Glowing lines and smooth animations
- **Responsive Grid**: Auto-adjusts for mobile/tablet/desktop

### **3. Risk Assessment (risk_assessment.html)**
- **Interactive Form**: 6 input fields (age, sex, bmi, smoker, children, region)
- **Security Matrix Animation**: Live matrix effect during data submission
- **Encryption Overlay**: Shows encryption process with spinner
- **Results Display**:
  - Predicted insurance cost
  - Risk level classification (LOW/MEDIUM/HIGH/CRITICAL)
  - RL-optimized premium with savings badge
  - Top risk factors (XAI breakdown)
  - Security status & hash verification
- **Color-coded Risk Levels**: Green (LOW) → Orange (MEDIUM) → Red (HIGH) → Dark Red (CRITICAL)

### **4. Security Vault (security_vault.html)**
- **Encryption Demo Tab**:
  - RSA-2048 encryption demonstration
  - SHA-512 hashing demonstration
  - Live hash output display
- **Integrity Verification Tab**:
  - Data integrity check with SHA-512
  - Tamper detection indication
  - Security metrics display
- **Audit Log Tab**:
  - Real-time audit log with 50+ entries
  - Timestamp, Action, Status, User Hash, Result Hash
  - Auto-refreshes every 10 seconds
  - Compliance indicators (RSA-2048, SHA-512, HIPAA, SOC 2)

### **CSS Theme (static/css/theme.css)**
- **Dark Mode**: Primary color #64c8ff, Accent #00ff88
- **Bootstrap 5 Integration**: Custom styling
- **Glowing Effects**: Box shadows and text effects
- **Smooth Transitions**: 0.3s ease on all interactive elements
- **Responsive Utilities**: Mobile-first design
- **Accessibility**: Focus-visible styles, high-contrast mode, reduced motion support
- **Scrollbar Styling**: Custom colors matching theme

---

## 🔧 Backend API Routes

### **Core Pages**
- `GET /` → Homepage
- `GET /dashboard` → Analytics Dashboard
- `GET /risk-assessment` → Risk Assessment Page
- `GET /security-vault` → Security & Audit Page

### **Assessment API**
- **POST `/api/assessment`** → Real-time risk assessment
  - Input: age, sex, bmi, smoker, children, region
  - Output: predicted_charge, risk_level, rl_optimization, risk_factors, security_info
  - Features:
    - Deep Learning MLP inference (TensorFlow/Keras)
    - Q-Learning RL agent optimization
    - RSA-2048 encryption & SHA-512 hashing
    - Explainable AI (feature importance)
    - Audit log entry

### **Dashboard APIs**
- **GET `/api/dashboard/trends`** → 30-day trend data
- **GET `/api/dashboard/distribution`** → Risk distribution stats
- **GET `/api/dashboard/statistics`** → Overall metrics

### **Security APIs**
- **POST `/api/security/encrypt`** → Encrypt data (RSA-2048)
- **POST `/api/security/verify-integrity`** → Verify SHA-512 hash
- **GET `/api/security/audit-log`** → Get audit log entries (last 50)

### **System Status**
- **GET `/api/status`** → System health check

---

## 🧠 Machine Learning Integration

### **Deep Learning (TensorFlow/Keras)**
```python
# MLP Neural Network
- Input Layer: 39 features (one-hot encoded)
- Hidden Layer 1: 128 neurons + Batch Norm + Dropout(0.3)
- Hidden Layer 2: 64 neurons + Batch Norm + Dropout(0.3)
- Hidden Layer 3: 32 neurons + Dropout(0.2)
- Output Layer: 1 neuron (insurance charge prediction)
- Activation: ReLU (hidden), Linear (output)
- Loss: Mean Squared Error (MSE)
- Optimizer: Adam
```

### **Reinforcement Learning (Q-Learning)**
```python
# Policy Adjustment Agent
- States: BMI bins (10) × Age bins (10) × Smoking (2) = 200 states
- Actions: Adjust premium by -10%, -5%, 0%, +5%, +10%
- Reward: Profit margin (×100) + Customer satisfaction (×50)
- Learning Rate: 0.1
- Discount Factor: 0.99
- Epsilon (exploration): 0.1
```

### **Security (RSA + SHA-512)**
```python
# Encryption
- Algorithm: RSA-2048
- Padding: OAEP with SHA-256
- Hash: SHA-512 (512-bit)

# Protected Data
- User IDs
- Health information (age, BMI, smoking status)
- Claim records
```

---

## 🎯 Key Features

### **1. Real-time Inference**
- GPU acceleration on NVIDIA Quadro T1000
- Sub-second prediction latency
- Batch processing support
- Model caching for performance

### **2. Dynamic Premium Adjustment**
- RL agent optimizes pricing based on health metrics
- Before/After comparison display
- Savings calculation and visualization
- Policy change indicators

### **3. Explainable AI (XAI)**
- Permutation-based feature importance
- Top 5 risk factors per prediction
- Factor influence scores
- Human-interpretable explanations

### **4. Security & Compliance**
- RSA-2048 encryption for sensitive data
- SHA-512 hashing for integrity
- Complete audit trail with timestamps
- HIPAA-compliant data handling
- Tamper detection

### **5. Interactive Analytics**
- Real-time trend visualization
- Risk distribution charts
- Premium optimization metrics
- Dynamic Chart.js visualizations
- Glowing, responsive design

---

## 🔐 Security Implementation

### **Data Protection**
```python
# In app.py - SecurityManager
security_mgr = DataProtectionManager()

# Encrypt health info
encrypted = security_mgr.protect_health_info({
    'age': 35,
    'bmi': 24.5,
    'smoker': 'no',
    'children': 2
})

# Hash for integrity
hash_value = hashlib.sha512(data.encode()).hexdigest()
```

### **Audit Logging**
```python
# Every operation logged
add_audit_log(
    action='risk_assessment',
    user_data=form_data,
    result=assessment_result
)
```

---

## 📊 API Response Examples

### **Risk Assessment Response**
```json
{
  "success": true,
  "timestamp": "2026-04-20T10:30:45.123456",
  "assessment": {
    "predicted_charge": 12543.50,
    "adjusted_charge": 11915.32,
    "risk_level": "MEDIUM",
    "adjustment_factor": 0.9499,
    "savings": 628.18
  },
  "rl_optimization": {
    "original_premium": 12543.50,
    "optimized_premium": 11915.32,
    "action": "REDUCE",
    "policy_change": "-5.0%"
  },
  "security": {
    "charge_hash": "a3f9d2e1c5b8...",
    "encrypted": true
  },
  "risk_factors": [
    "age",
    "smoker_yes",
    "children",
    "region_northeast",
    "sex_male"
  ]
}
```

---

## 🚀 Deployment

### **Local Development**
```bash
python app.py
# Server runs on http://0.0.0.0:5000
```

### **Production (Gunicorn)**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### **Docker**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

---

## 🔧 Configuration

### **Environment Variables**
```bash
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=insurguard-ai-secure-key-2026
```

### **Flask Settings**
```python
# app.py
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
```

---

## 📈 Performance Metrics

- **Model Inference**: ~50-100ms per prediction
- **Page Load**: <2 seconds
- **API Response**: <500ms average
- **Concurrent Users**: 100+ (with gunicorn workers)
- **Memory Usage**: ~500MB base + model weight
- **GPU Memory**: ~1GB (NVIDIA Quadro T1000)

---

## 🎓 Usage Examples

### **Basic Assessment Flow**
1. User navigates to `/risk-assessment`
2. Fills in health information (age, BMI, etc.)
3. Clicks "Analyze Risk Profile"
4. Security matrix animation plays
5. System encrypts & hashes data
6. TensorFlow model predicts insurance cost
7. RL agent optimizes premium
8. Results displayed with XAI breakdown
9. Audit log updated

### **Programmatic API Usage**
```python
import requests
import json

# Submit assessment
data = {
    'age': 35,
    'sex': 'male',
    'bmi': 24.5,
    'smoker': 'no',
    'children': 2,
    'region': 'northeast'
}

response = requests.post(
    'http://localhost:5000/api/assessment',
    json=data
)

result = response.json()
print(f"Predicted Cost: ${result['assessment']['predicted_charge']:.2f}")
print(f"After RL: ${result['rl_optimization']['optimized_premium']:.2f}")
print(f"Risk Factors: {result['risk_factors']}")
```

---

## 🐛 Troubleshooting

### **Models Not Initializing**
```
Solution: Ensure data/medical_insurance.csv exists
          Check file permissions and path
```

### **GPU Not Detected**
```
Solution: Install NVIDIA CUDA drivers
          Update TensorFlow-GPU
          Check NVIDIA Quadro T1000 compatibility
```

### **Port Already in Use**
```bash
# Kill process using port 5000
lsof -ti:5000 | xargs kill -9

# Or use different port
python app.py --port 5001
```

### **CSS Not Loading**
```
Solution: Check static/ directory structure
          Clear browser cache
          Verify Flask static_folder config
```

---

## 📝 Browser Support

- **Chrome/Edge**: ✅ Full support
- **Firefox**: ✅ Full support
- **Safari**: ✅ Full support
- **Mobile Browsers**: ✅ Responsive design
- **IE 11**: ❌ Not supported (modern features required)

---

## 🔗 API Rate Limiting

- **Assessment endpoint**: 30 requests/minute per IP
- **Encryption demo**: 20 requests/minute per IP
- **Dashboard**: 200 requests/day, 50 requests/hour
- **General**: 200 requests/day, 50 requests/hour

---

## 📞 Support & Documentation

- **Quick Start**: See above
- **API Docs**: Check route docstrings in app.py
- **Frontend**: See template HTML comments
- **ML Models**: See parent directory README.md

---

## ✨ Features at a Glance

| Feature | Status | Details |
|---------|--------|---------|
| Deep Learning | ✅ | TensorFlow/Keras MLP with 4 layers |
| Reinforcement Learning | ✅ | Q-Learning agent for price optimization |
| Real-time Inference | ✅ | GPU-accelerated on NVIDIA Quadro T1000 |
| RSA-2048 Encryption | ✅ | OAEP padding, SHA-256 |
| SHA-512 Hashing | ✅ | Integrity verification |
| Explainable AI | ✅ | Permutation importance, top 5 factors |
| Interactive Dashboard | ✅ | Chart.js with dual-axis trends |
| Audit Logging | ✅ | Real-time, auto-refresh every 10s |
| Security Matrix | ✅ | Live animation on data submission |
| Dark Mode Theme | ✅ | Bootstrap 5 custom glowing design |
| Responsive Design | ✅ | Mobile, tablet, desktop optimized |
| Rate Limiting | ✅ | Flask-Limiter protection |
| CORS Support | ✅ | Cross-origin requests enabled |
| Error Handling | ✅ | Comprehensive exception handling |

---

## 📄 License

InsurGuard AI - Enterprise Insurance Risk Assessment System
© 2026 DEVANANTH. All Rights Reserved.

---

**Last Updated**: April 20, 2026  
**Version**: 1.0.0  
**Status**: Production Ready ✅
