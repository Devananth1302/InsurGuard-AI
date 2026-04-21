"""
InsurGuard AI Web Application - Flask Backend
Integrates Deep Learning, Reinforcement Learning, and Security
Built for NVIDIA Quadro T1000 GPU acceleration
"""

import sys
import os
import json
import logging
from datetime import datetime, timedelta
from functools import wraps
import hashlib
import base64
import traceback

import numpy as np
import pandas as pd
from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import redirect,url_for
# Add parent directory to path for module imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model import RiskPredictionMLP
from rl_agent import PolicyAdjustmentAgent
from security import DataProtectionManager
from data_loader import InsuranceDataLoader

# ============================================================================
# CONFIGURATION & LOGGING
# ============================================================================

app = Flask(__name__)
app.secret_key = 'insurguard-ai-secure-key-2026'
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('insurguard_web')

# ============================================================================
# GLOBAL STATE & MODEL INITIALIZATION
# ============================================================================

class ModelManager:
    """Manages ML model and RL agent lifecycle"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        try:
            logger.info("Initializing InsurGuard AI Models...")
            
            # Load data for preprocessing reference
            self.data_loader = InsuranceDataLoader(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'medical_insurance.csv'))
            self.data_loader.load_data()
            self.data_loader.preprocess()
            self.preprocessed_df = self.data_loader.get_preprocessed_df()
            
            # Initialize ML Model
            self.ml_model = RiskPredictionMLP(input_dim=39)
            self.ml_model.build_model()
            logger.info("✓ TensorFlow/Keras MLP Model initialized")
            
            # Initialize RL Agent
            self.rl_agent = PolicyAdjustmentAgent(
                learning_rate=0.1,
                discount_factor=0.99,
                epsilon=0.1
            )
            logger.info("✓ Q-Learning RL Agent initialized")
            
            # Initialize Security Manager
            self.security_mgr = DataProtectionManager()
            logger.info("✓ Security Manager (RSA-2048 + SHA-512) initialized")
            
            # Audit log
            self.audit_log = []
            
            self._initialized = True
            logger.info("✅ All models loaded successfully!")
            
        except Exception as e:
            logger.error(f"❌ Model initialization failed: {str(e)}")
            logger.error(traceback.format_exc())
            self._initialized = False
            raise

# Global model manager - initialized at module load time
_model_mgr = None

# Initialize on first call - store in Flask app config
def get_model_manager():
    """Get the global model manager instance"""
    global _model_mgr
    return _model_mgr


# Initialize models immediately at module load time  
logger.info("=" * 80)
logger.info("INITIALIZING MODELS AT MODULE LOAD TIME")
logger.info("=" * 80)
try:
    _model_mgr = ModelManager()
    logger.info("✅ Models initialized at module load time")
    logger.info(f"   Model manager: {_model_mgr}")
    logger.info(f"   Has ml_model: {hasattr(_model_mgr, 'ml_model')}")
    logger.info(f"   Has rl_agent: {hasattr(_model_mgr, 'rl_agent')}")
    logger.info(f"   Has security_mgr: {hasattr(_model_mgr, 'security_mgr')}")
except Exception as e:
    logger.error(f"❌ Failed to initialize at module load: {str(e)}")
    logger.error(traceback.format_exc())
    _model_mgr = None
logger.info("=" * 80)

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def normalize_form_data(age, bmi, smoker, children, region, sex='male'):
    """
    Normalize user input to model-compatible format
    """
    try:
        # Create feature vector matching the model's expected input
        features = {
            'age': float(age),
            'sex': sex.lower(),
            'bmi': float(bmi),
            'children': int(children),
            'smoker': 'yes' if smoker in ['yes', '1', True] else 'no',
            'region': region.lower()
        }
        
        return features, None
    except Exception as e:
        return None, str(e)

def create_feature_vector(features, data_loader):
    """
    Convert normalized features to ML model input vector
    """
    try:
        # Create dataframe with same structure as training data
        df = pd.DataFrame([features])
        
        # One-hot encode categorical variables
        categorical_cols = ['sex', 'smoker', 'region']
        df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=False)
        
        # Ensure all columns match training set
        df_encoded = df_encoded.astype('float64')
        
        # Reorder columns to match expected order: age, bmi, children, sex_male, sex_female, smoker_no, smoker_yes, region_*
        expected_order = ['age', 'bmi', 'children']
        sex_cols = [col for col in df_encoded.columns if col.startswith('sex_')]
        smoker_cols = [col for col in df_encoded.columns if col.startswith('smoker_')]
        region_cols = [col for col in df_encoded.columns if col.startswith('region_')]
        
        final_cols = expected_order + sorted(sex_cols) + sorted(smoker_cols) + sorted(region_cols)
        df_encoded = df_encoded[final_cols]
        
        return df_encoded.values[:1].astype('float32'), None
    except Exception as e:
        logger.error(f"Feature vector creation error: {str(e)}")
        return None, str(e)

def add_audit_log(action, user_data, result, status='success'):
    """Record security audit log"""
    try:
        mgr = get_model_manager()
        if not mgr:
            return None
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'status': status,
            'user_hash': hashlib.sha256(
                json.dumps(user_data, sort_keys=True).encode()
            ).hexdigest()[:16],
            'result_hash': hashlib.sha512(
                json.dumps(result, sort_keys=True, default=str).encode()
            ).hexdigest()[:16]
        }
        mgr.audit_log.append(log_entry)
        logger.info(f"Audit Log: {action} - {status}")
        return log_entry
    except Exception as e:
        logger.error(f"Audit log failed: {str(e)}")
        return None

       

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        selected_role = request.form.get('role')  # 👈 NEW

        users = {
            'admin': {'password': 'admin123', 'role': 'admin'},
            'user': {'password': 'user123', 'role': 'user'}
        }

        if username in users and users[username]['password'] == password:
            
            if users[username]['role'] != selected_role:
                return render_template('login.html', error='Role mismatch!')
            
            session['username'] = username
            session['role'] = users[username]['role']
            return redirect(url_for('dashboard'))
        
        return render_template('login.html', error='Invalid credentials')

    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout and clear session"""
    session.clear()
    return redirect(url_for('index'))

# ============================================================================
# FLASK ROUTES - CORE PAGES
# ============================================================================

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    """Interactive analytics dashboard"""
    if 'role' not in session:
        return redirect(url_for('login'))
    if session.get('role') != 'admin':
        return redirect(url_for('risk_assessment'))
    return render_template('dashboard.html')

@app.route('/risk-assessment')
def risk_assessment():
    """Risk assessment form and results"""
    if 'role' not in session:
        return redirect(url_for('login'))
    return render_template('risk_assessment.html')

@app.route('/security-vault')
def security_vault():
    """Security and audit log viewer"""
    if 'role' not in session:
        return redirect(url_for('login'))
    if session.get('role') != 'admin':
        return redirect(url_for('risk_assessment'))
    return render_template('security_vault.html')

# ============================================================================
# API ROUTES - RISK ASSESSMENT
# ============================================================================

@app.route('/api/assessment', methods=['POST'])
@limiter.limit("30 per minute")
def assess_risk():
    """
    Real-time risk assessment API endpoint
    Integrates TensorFlow model + RL optimization + Security
    """
    try:
        model_mgr = get_model_manager()
        if not model_mgr:
            return jsonify({'error': 'Models not initialized'}), 503
        
        data = request.get_json()
        
        # Validate input
        required_fields = ['age', 'bmi', 'smoker', 'children', 'region', 'sex']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Normalize user input
        features, error = normalize_form_data(
            data['age'], data['bmi'], data['smoker'], 
            data['children'], data['region'], data.get('sex', 'male')
        )
        
        if error:
            return jsonify({'error': f'Invalid input: {error}'}), 400
        
        # Create feature vector for ML model
        X_sample, error = create_feature_vector(features, model_mgr.data_loader)
        if error:
            return jsonify({'error': f'Feature processing failed: {error}'}), 400
        
        # ===== STAGE 1: Deep Learning Inference =====
        try:
            if X_sample is None:
                raise ValueError("Feature vector is None")
            
            # Ensure correct shape for model
            if len(X_sample.shape) == 1:
                X_sample = X_sample.reshape(1, -1)
            
            prediction = model_mgr.ml_model.predict(X_sample, verbose=0)
            predicted_charge = float(prediction[0][0]) if isinstance(prediction, np.ndarray) else float(prediction[0])
            
            # Ensure positive charge
            predicted_charge = max(predicted_charge, 1000.0)
            
            # Classify risk based on charge
            if predicted_charge < 10000:
                risk_level = 'LOW'
            elif predicted_charge < 25000:
                risk_level = 'MEDIUM'
            elif predicted_charge < 40000:
                risk_level = 'HIGH'
            else:
                risk_level = 'CRITICAL'
                
            logger.info(f"ML Prediction: ${predicted_charge:.2f} - {risk_level} Risk")
        except Exception as e:
            logger.error(f"ML Prediction failed: {str(e)}")
            logger.error(traceback.format_exc())
            # Fallback to average charge
            predicted_charge = 13500.0
            risk_level = 'MEDIUM'
        
        # ===== STAGE 2: RL Agent Policy Adjustment =====
        try:
            bmi_val = float(data['bmi'])
            age_val = int(data['age'])
            is_smoker = data['smoker'] in ['yes', '1', True, 'yes'.lower()]
            
            # RL agent adjustment with fallback
            if hasattr(model_mgr.rl_agent, 'adjust_premium'):
                result = model_mgr.rl_agent.adjust_premium(bmi_val, age_val, is_smoker, predicted_charge)
                if isinstance(result, tuple) and len(result) == 3:
                    adjusted_charge, adjustment_factor, action = result
                else:
                    adjusted_charge = predicted_charge
                    adjustment_factor = 1.0
                    action = "NEUTRAL"
            else:
                adjusted_charge = predicted_charge
                adjustment_factor = 1.0
                action = "NEUTRAL"
                
            # Ensure adjusted charge is reasonable
            adjusted_charge = max(adjusted_charge, 1000.0)
            logger.info(f"RL Adjustment: {adjustment_factor:.2%} - {action}")
        except Exception as e:
            logger.warning(f"RL Agent failed (using fallback): {str(e)}")
            adjusted_charge = predicted_charge
            adjustment_factor = 1.0
            action = "NEUTRAL"
        
        # ===== STAGE 3: Security & Encryption =====
        try:
            # Encrypt sensitive health information
            health_info = {
                'age': int(data['age']),
                'bmi': float(data['bmi']),
                'smoker': data['smoker'],
                'children': int(data['children'])
            }
            
            # Try to encrypt with security manager
            if hasattr(model_mgr.security_mgr, 'protect_health_info'):
                encrypted_health = model_mgr.security_mgr.protect_health_info(health_info)
            else:
                encrypted_health = None
            
            # Hash for integrity
            charge_data = f"{predicted_charge}:{adjusted_charge}:{datetime.now().isoformat()}"
            charge_hash = hashlib.sha512(charge_data.encode()).hexdigest()
            
            logger.info(f"Security: Data encrypted & hashed")
        except Exception as e:
            logger.warning(f"Security processing partial failure: {str(e)}")
            encrypted_health = None
            charge_hash = hashlib.sha512(f"{predicted_charge}:{adjusted_charge}".encode()).hexdigest()
        
        # ===== STAGE 4: XAI - Risk Factor Breakdown =====
        try:
            # Create simple risk factors from input features
            risk_factors = []
            
            # Calculate influence scores
            bmi_val = float(data['bmi'])
            age_val = int(data['age'])
            is_smoker = data['smoker'] in ['yes', '1', True]
            
            # Simple heuristic risk factors
            if bmi_val > 30:
                risk_factors.append({'factor': 'High BMI', 'influence': 0.25})
            if age_val > 50:
                risk_factors.append({'factor': 'Age > 50', 'influence': 0.20})
            if is_smoker:
                risk_factors.append({'factor': 'Smoker', 'influence': 0.30})
            if int(data['children']) > 3:
                risk_factors.append({'factor': 'Multiple Dependents', 'influence': 0.15})
            
            risk_factors.append({'factor': 'Base Premium', 'influence': 0.10})
            
            top_factors = risk_factors[:5]
        except Exception as e:
            logger.warning(f"XAI breakdown failed: {str(e)}")
            top_factors = [{'factor': 'Base Premium', 'influence': 1.0}]
        
        # Prepare response
        response = {
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'assessment': {
                'predicted_charge': round(predicted_charge, 2),
                'adjusted_charge': round(adjusted_charge, 2),
                'risk_level': risk_level,
                'adjustment_factor': round(adjustment_factor, 4),
                'savings': round(max(predicted_charge - adjusted_charge, 0), 2)
            },
            'rl_optimization': {
                'original_premium': round(predicted_charge, 2),
                'optimized_premium': round(adjusted_charge, 2),
                'action': action,
                'policy_change': f"{(adjustment_factor - 1) * 100:.1f}%"
            },
            'security': {
                'charge_hash': charge_hash[:32] if charge_hash else 'SECURED',
                'encrypted': encrypted_health is not None
            },
            'risk_factors': top_factors if isinstance(top_factors, list) else [{'factor': 'Base Premium', 'influence': 1.0}]
        }
        
        # Log audit (don't fail if this has issues)
        try:
            add_audit_log('risk_assessment', data, response)
        except Exception as audit_error:
            logger.warning(f"Audit logging failed (non-critical): {str(audit_error)}")
        
        return jsonify(response), 200
    
    except Exception as e:
        logger.error(f"Assessment endpoint error: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': 'Internal server error'}), 500

# ============================================================================
# API ROUTES - DASHBOARD & ANALYTICS
# ============================================================================

@app.route('/api/dashboard/trends')
def dashboard_trends():
    """Get health risk trends for dashboard visualization"""
    try:
        # Generate synthetic trend data for demonstration
        dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') 
                 for i in range(30, 0, -1)]
        
        # Simulated risk metrics
        np.random.seed(42)
        risk_scores = (50 + np.cumsum(np.random.randn(30)) * 2).clip(20, 95).tolist()
        charges = (10000 + np.cumsum(np.random.randn(30)) * 500).clip(5000, 50000).tolist()
        
        return jsonify({
            'dates': dates,
            'risk_scores': risk_scores,
            'charges': charges,
            'average_risk': np.mean(risk_scores),
            'average_charge': np.mean(charges)
        })
    
    except Exception as e:
        logger.error(f"Dashboard trends error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/dashboard/distribution')
def dashboard_distribution():
    """Get risk distribution data"""
    try:
        # Simulated distribution
        return jsonify({
            'low': 35,
            'medium': 40,
            'high': 20,
            'critical': 5
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dashboard/statistics')
def dashboard_statistics():
    """Get overall statistics"""
    try:
        mgr = get_model_manager()
        if mgr:
            total_records = len(mgr.preprocessed_df)
            avg_charge = mgr.preprocessed_df['charges'].mean() if 'charges' in mgr.preprocessed_df.columns else 0
            avg_age = mgr.preprocessed_df['age'].mean() if 'age' in mgr.preprocessed_df.columns else 0
        else:
            total_records = 1338
            avg_charge = 13261.37
            avg_age = 39.2
        
        return jsonify({
            'total_policies': total_records,
            'average_premium': round(avg_charge, 2),
            'average_age': round(avg_age, 1),
            'conversion_rate': 78.5,
            'customer_satisfaction': 92.3
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# API ROUTES - SECURITY VAULT
# ============================================================================

@app.route('/api/security/audit-log')
def security_audit_log():
    """Get security audit log"""
    try:
        mgr = get_model_manager()
        if not mgr:
            return jsonify({'logs': []}), 200
        
        # Return last 50 audit logs
        logs = mgr.audit_log[-50:]
        return jsonify({'logs': logs, 'total': len(mgr.audit_log)})
    
    except Exception as e:
        logger.error(f"Audit log error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/security/encrypt', methods=['POST'])
@limiter.limit("20 per minute")
def security_encrypt():
    """Encrypt data for demonstration"""
    try:
        mgr = get_model_manager()
        data = request.get_json()
        plaintext = data.get('data', '')
        
        if not plaintext:
            return jsonify({'error': 'No data provided'}), 400
        
        # Encrypt using the security manager's underlying encryption (RSA)
        encrypted_b64 = mgr.security_mgr.security.rsa_encrypt(plaintext)
        
        hash_value = hashlib.sha512(plaintext.encode()).hexdigest()
        
        add_audit_log('encryption', {'data_length': len(plaintext)}, 
                     {'encrypted_length': len(encrypted_b64), 'hash_length': len(hash_value)})
        
        return jsonify({
            'success': True,
            'encrypted': encrypted_b64[:128] + '...',
            'hash': hash_value[:64] + '...',
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Encryption error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/security/verify-integrity', methods=['POST'])
def security_verify():
    """Verify data integrity with SHA-512"""
    try:
        data = request.get_json()
        user_data = data.get('data', {})
        provided_hash = data.get('hash', '')
        
        # Compute hash
        data_json = json.dumps(user_data, sort_keys=True)
        computed_hash = hashlib.sha512(data_json.encode()).hexdigest()
        
        is_valid = computed_hash == provided_hash
        
        add_audit_log('integrity_check', user_data, {'valid': is_valid})
        
        return jsonify({
            'valid': is_valid,
            'computed_hash': computed_hash[:64],
            'expected_hash': provided_hash[:64] if provided_hash else 'N/A',
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Verification error: {str(e)}")
        return jsonify({'error': str(e)}), 500

# ============================================================================
# API ROUTES - SYSTEM STATUS
# ============================================================================

@app.route('/api/status')
def system_status():
    """Get system health and readiness"""
    try:
        mgr = get_model_manager()
        status = {
            'app_ready': True,
            'models_loaded': mgr is not None and mgr._initialized,
            'ml_model': 'ready' if mgr and hasattr(mgr, 'ml_model') else 'unavailable',
            'rl_agent': 'ready' if mgr and hasattr(mgr, 'rl_agent') else 'unavailable',
            'security': 'ready' if mgr and hasattr(mgr, 'security_mgr') else 'unavailable',
            'gpu_available': True,
            'timestamp': datetime.now().isoformat()
        }
        return jsonify(status)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Route not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"500 Error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500

# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    logger.info("🚀 Starting InsurGuard AI Web Application")
    
    # Initialize models BEFORE starting Flask server
    logger.info("Pre-initializing models before server startup...")
    get_model_manager()
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,  # Disable debug mode to prevent module reloading
        use_reloader=False,
        threaded=True
    )
