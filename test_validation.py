"""
InsurGuard Validation & Test Suite
Verifies all components are working correctly
"""

import os
import sys
import logging
import numpy as np
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)


def test_data_loading():
    """Test data loading module"""
    logger.info("\n[TEST 1] Data Loading Module")
    logger.info("-" * 50)
    
    try:
        from data_loader import InsuranceDataLoader
        
        data_path = './data/medical_insurance.csv'
        
        if not os.path.exists(data_path):
            logger.error(f"Data file not found: {data_path}")
            return False
        
        loader = InsuranceDataLoader(data_path)
        loader.load_data()
        
        if loader.df is None:
            logger.error("Failed to load data")
            return False
        
        logger.info(f"✓ Loaded {len(loader.df)} records")
        
        info = loader.explore_data()
        logger.info(f"✓ Columns: {info['shape'][1]}")
        
        X_train, X_test, y_train, y_test, features = loader.preprocess()
        logger.info(f"✓ Preprocessed - Train: {X_train.shape}, Test: {X_test.shape}")
        logger.info(f"✓ Features after encoding: {len(features)}")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Data loading failed: {str(e)}")
        return False


def test_deep_learning_model():
    """Test TensorFlow model"""
    logger.info("\n[TEST 2] Deep Learning Model (TensorFlow/Keras)")
    logger.info("-" * 50)
    
    try:
        from model import RiskPredictionMLP
        import numpy as np
        
        # Create dummy data
        X_dummy = np.random.randn(100, 20)
        y_dummy = np.random.uniform(5000, 50000, 100)
        
        # Build model
        model = RiskPredictionMLP(input_dim=20, use_gpu=False)
        model.build_model(layers_config=[64, 32])
        logger.info("✓ Model built successfully")
        
        # Train briefly
        history = model.train(X_dummy, y_dummy, epochs=5, batch_size=16)
        logger.info("✓ Model training completed")
        
        # Make prediction
        X_test = np.random.randn(10, 20)
        predictions = model.predict(X_test)
        
        if len(predictions) == 10:
            logger.info(f"✓ Predictions generated: {len(predictions)} samples")
        else:
            logger.error("Prediction shape mismatch")
            return False
        
        # Risk classification
        risk = model._classify_risk(25000)
        logger.info(f"✓ Risk classification: ${25000} = {risk}")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Deep learning test failed: {str(e)}")
        return False


def test_reinforcement_learning():
    """Test RL agent"""
    logger.info("\n[TEST 3] Reinforcement Learning Agent")
    logger.info("-" * 50)
    
    try:
        from rl_agent import PolicyAdjustmentAgent
        import numpy as np
        
        # Initialize agent
        agent = PolicyAdjustmentAgent(
            learning_rate=0.1,
            discount_factor=0.95
        )
        logger.info("✓ RL agent initialized")
        
        # Create dummy health metrics
        health_metrics = [
            {'age': 35, 'bmi': 28.5, 'smoker': 1},
            {'age': 45, 'bmi': 26.0, 'smoker': 0},
            {'age': 55, 'bmi': 30.5, 'smoker': 1},
        ]
        
        predictions = np.array([25000, 15000, 35000])
        
        # Train
        for episode in range(5):
            reward = agent.train_episode(health_metrics, predictions)
        logger.info("✓ RL training completed (5 episodes)")
        
        # Get adjustment
        adjustment = agent.adjust_premium(28.5, 35, 1, 25000)
        
        if 'adjusted_charge' in adjustment:
            logger.info(f"✓ Premium adjustment: ${adjustment['adjusted_charge']:.2f}")
        else:
            logger.error("Adjustment failed")
            return False
        
        # Get summary
        summary = agent.get_training_summary()
        logger.info(f"✓ Q-table size: {summary['q_table_size']}")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ RL agent test failed: {str(e)}")
        return False


def test_security_module():
    """Test encryption and hashing"""
    logger.info("\n[TEST 4] Cybersecurity Module (RSA + SHA-512)")
    logger.info("-" * 50)
    
    try:
        from security import InsurGuardSecurity, DataProtectionManager
        
        # Initialize security
        security = InsurGuardSecurity(key_size=2048)
        logger.info("✓ RSA key pair generated (2048-bit)")
        
        # Test RSA encryption
        plaintext = "USER_12345"
        encrypted = security.rsa_encrypt(plaintext)
        decrypted = security.rsa_decrypt(encrypted)
        
        if decrypted == plaintext:
            logger.info(f"✓ RSA encryption/decryption: SUCCESS")
        else:
            logger.error("Decryption mismatch")
            return False
        
        # Test SHA-512 hashing
        data = "Claim_2024_03_15_$5000"
        hash_value = security.sha512_hash(data)
        
        if len(hash_value) == 128:  # SHA-512 produces 128 hex chars
            logger.info(f"✓ SHA-512 hash generated (128 chars)")
        else:
            logger.error("Hash length mismatch")
            return False
        
        # Test integrity verification
        is_valid = security.verify_integrity(data, hash_value)
        if is_valid:
            logger.info("✓ Integrity verification: PASSED")
        else:
            logger.error("Integrity check failed")
            return False
        
        # Test Data Protection Manager
        mgr = DataProtectionManager()
        encrypted_id = mgr.protect_user_id("USER_ABC")
        logger.info("✓ Data Protection Manager initialized")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Security module test failed: {str(e)}")
        return False


def test_analytics_module():
    """Test visualization and analytics"""
    logger.info("\n[TEST 5] Analytics & Visualization Module")
    logger.info("-" * 50)
    
    try:
        from analytics import InsuranceAnalyticsDashboard
        import numpy as np
        
        # Create dummy dataframe
        df = pd.DataFrame({
            'age': np.random.uniform(18, 65, 100),
            'bmi': np.random.uniform(15, 55, 100),
            'charges': np.random.uniform(5000, 50000, 100),
            'smoker_yes': np.random.randint(0, 2, 100),
            'region': np.random.choice(['northeast', 'northwest', 'southeast', 'southwest'], 100),
            'children': np.random.randint(0, 5, 100)
        })
        
        predictions = np.random.uniform(5000, 50000, 100)
        
        # Initialize dashboard
        dashboard = InsuranceAnalyticsDashboard(df, predictions)
        logger.info("✓ Dashboard initialized")
        
        # Generate visualizations
        dashboard.plot_risk_distribution()
        logger.info("✓ Risk distribution plot generated")
        
        dashboard.plot_age_bmi_correlation()
        logger.info("✓ Age-BMI correlation plot generated")
        
        dashboard.plot_demographic_breakdown()
        logger.info("✓ Demographic breakdown plot generated")
        
        dashboard.plot_region_analysis()
        logger.info("✓ Regional analysis plot generated")
        
        dashboard.plot_prediction_performance(df['charges'].values, predictions)
        logger.info("✓ Performance plot generated")
        
        # Generate summary
        summary = dashboard.generate_summary_report()
        logger.info(f"✓ Analytics summary: {len(summary)} metrics")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Analytics module test failed: {str(e)}")
        return False


def test_dependencies():
    """Test all required dependencies"""
    logger.info("\n[TEST 0] Dependency Check")
    logger.info("-" * 50)
    
    dependencies = {
        'pandas': 'Data manipulation',
        'numpy': 'Numerical computing',
        'sklearn': 'Machine learning utilities',
        'tensorflow': 'Deep learning framework',
        'cryptography': 'Encryption library',
        'matplotlib': 'Plotting library',
        'seaborn': 'Statistical visualization'
    }
    
    missing = []
    
    for lib, desc in dependencies.items():
        try:
            __import__(lib if lib != 'sklearn' else 'sklearn')
            logger.info(f"✓ {lib:15} - {desc}")
        except ImportError:
            logger.warning(f"✗ {lib:15} - MISSING")
            missing.append(lib)
    
    if missing:
        logger.warning(f"\nMissing libraries: {', '.join(missing)}")
        logger.warning("Install with: pip install -r requirements.txt")
        return False
    
    return True


def main():
    """Run all tests"""
    logger.info("=" * 50)
    logger.info("InsurGuard AI - Validation Test Suite")
    logger.info("=" * 50)
    
    tests = [
        ("Dependencies", test_dependencies),
        ("Data Loading", test_data_loading),
        ("Deep Learning Model", test_deep_learning_model),
        ("Reinforcement Learning", test_reinforcement_learning),
        ("Security Module", test_security_module),
        ("Analytics Module", test_analytics_module),
    ]
    
    results = {}
    
    for name, test_func in tests:
        try:
            result = test_func()
            results[name] = "PASS" if result else "FAIL"
        except Exception as e:
            logger.error(f"✗ {name} test crashed: {str(e)}")
            results[name] = "ERROR"
    
    # Summary
    logger.info("\n" + "=" * 50)
    logger.info("TEST SUMMARY")
    logger.info("=" * 50)
    
    for test_name, status in results.items():
        symbol = "✓" if status == "PASS" else "✗"
        logger.info(f"{symbol} {test_name:30} {status}")
    
    passed = sum(1 for s in results.values() if s == "PASS")
    total = len(results)
    
    logger.info("\n" + "=" * 50)
    logger.info(f"Results: {passed}/{total} tests passed")
    logger.info("=" * 50)
    
    if passed == total:
        logger.info("\n✓ All systems operational! Ready to run: python main.py")
        return 0
    else:
        logger.warning("\n✗ Some tests failed. Check requirements and paths.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
