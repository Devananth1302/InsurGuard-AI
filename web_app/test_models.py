import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model import RiskPredictionMLP
from rl_agent import PolicyAdjustmentAgent
from security import DataProtectionManager
from data_loader import InsuranceDataLoader

print("Testing model initialization...")

try:
    print("1. Loading data...")
    data_loader = InsuranceDataLoader(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'medical_insurance.csv'))
    data_loader.load_data()
    data_loader.preprocess()
    print(f"   Data loaded: {data_loader.df.shape}")

    print("2. Initializing MLP...")
    ml_model = RiskPredictionMLP(input_dim=39)
    ml_model.build_model()
    print("   MLP initialized")

    print("3. Initializing RL Agent...")
    rl_agent = PolicyAdjustmentAgent(learning_rate=0.1, discount_factor=0.99, epsilon=0.1)
    print("   RL Agent initialized")

    print("4. Initializing Security Manager...")
    security_mgr = DataProtectionManager()
    print("   Security Manager initialized")

    print("✓ All models initialized successfully")
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
