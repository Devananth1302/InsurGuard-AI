import sys
import os
import json
import logging
from datetime import datetime
import hashlib
import traceback

import numpy as np
import pandas as pd
import joblib

from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Fix import path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model import RiskPredictionMLP
from rl_agent import PolicyAdjustmentAgent
from security import DataProtectionManager

# ================= CONFIG =================

app = Flask(__name__)
app.secret_key = 'insurguard-ai-secure-key-2026'

CORS(app)

limiter = Limiter(key_func=get_remote_address)
limiter.init_app(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("insurguard")


# ================= MODEL MANAGER =================

class ModelManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "_initialized"):
            return

        logger.info("🚀 Initializing Models...")

        BASE_DIR = os.path.dirname(os.path.dirname(__file__))

        model_path = os.path.join(BASE_DIR, "saved_models", "mlp_model.keras")
        columns_path = os.path.join(BASE_DIR, "saved_models", "columns.pkl")

        if not os.path.exists(model_path):
            raise Exception("❌ Model not found. Run: python model.py")

        self.feature_columns = joblib.load(columns_path)

        self.ml_model = RiskPredictionMLP(input_dim=len(self.feature_columns))
        self.ml_model.load_model(model_path)

        logger.info(f"✅ ML Model loaded ({len(self.feature_columns)} features)")

        self.rl_agent = PolicyAdjustmentAgent()

        self.security_mgr = DataProtectionManager()
        self.audit_log = []
        self._initialized = True


_model_mgr = ModelManager()


def get_model_manager():
    return _model_mgr


# ================= HELPERS =================

def normalize_form_data(data):
    return {
        'age': float(data['age']),
        'sex': data['sex'],
        'bmi': float(data['bmi']),
        'children': int(data['children']),
        'smoker': data['smoker'],
        'region': data['region']
    }


def create_feature_vector(features):
    df = pd.DataFrame([features])

    df = pd.get_dummies(df, columns=['sex', 'smoker', 'region'], drop_first=False)

    expected_cols = get_model_manager().feature_columns

    for col in expected_cols:
        if col not in df.columns:
            df[col] = 0

    df = df[expected_cols]

    return df.values.astype('float32')


# ================= ROUTES =================

@app.route('/')
def index():
    return redirect(url_for('risk_assessment'))


@app.route('/risk-assessment')
def risk_assessment():
    return render_template('risk_assessment.html')


@app.route('/api/assessment', methods=['POST'])
def assess_risk():
    try:
        mgr = get_model_manager()
        data = request.json

        features = normalize_form_data(data)
        X = create_feature_vector(features)

        # ML prediction
        prediction = mgr.ml_model.predict(X)
        predicted_charge = float(prediction[0])

        predicted_charge = max(predicted_charge, 1000)

        # Risk
        if predicted_charge < 10000:
            risk = "LOW"
        elif predicted_charge < 25000:
            risk = "MEDIUM"
        elif predicted_charge < 40000:
            risk = "HIGH"
        else:
            risk = "CRITICAL"

        # RL adjustment
        adjusted_charge, factor, action = mgr.rl_agent.adjust_premium(
            float(data['bmi']),
            int(data['age']),
            data['smoker'] == 'yes',
            predicted_charge
        )

        charge_hash = hashlib.sha512(str(predicted_charge).encode()).hexdigest()

        return jsonify({
            "predicted_charge": round(predicted_charge, 2),
            "adjusted_charge": round(adjusted_charge, 2),
            "risk": risk,
            "adjustment": action,
            "factor": round(factor, 3),
            "hash": charge_hash[:16]
        })

    except Exception as e:
        logger.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 500


# ================= RUN =================

if __name__ == '__main__':
    logger.info("🚀 Starting InsurGuard App")
    app.run(host='0.0.0.0', port=5000)