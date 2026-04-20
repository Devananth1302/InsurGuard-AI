"""
InsurGuard AI: Main Orchestration Module
Integrates all components: Data, DL Model, RL Agent, Security, and Analytics
"""

import os
import json
import numpy as np
import pandas as pd
import logging
from datetime import datetime
from typing import Dict, Tuple

# Import custom modules
from data_loader import InsuranceDataLoader
from model import RiskPredictionMLP
from rl_agent import PolicyAdjustmentAgent
from security import DataProtectionManager, InsurGuardSecurity
from analytics import InsuranceAnalyticsDashboard

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class InsurGuardAISystem:
    """Complete Insurance Risk Assessment and Policy Management System"""
    
    def __init__(self, data_path: str, use_gpu: bool = False):
        """
        Initialize InsurGuard System
        
        Args:
            data_path: Path to insurance CSV data
            use_gpu: Whether to use GPU for model training
        """
        self.data_path = data_path
        self.use_gpu = use_gpu
        
        # Component initialization placeholders
        self.data_loader = None
        self.ml_model = None
        self.rl_agent = None
        self.security_manager = None
        self.dashboard = None
        
        # Results storage
        self.predictions = None
        self.rl_adjustments = None
        self.system_metrics = {}
        
        logger.info("=" * 60)
        logger.info("InsurGuard AI System Initializing")
        logger.info("=" * 60)
    
    def run_full_pipeline(self) -> Dict:
        """Execute complete analysis pipeline"""
        pipeline_start = datetime.now()
        
        # 1. Data Loading and Preprocessing
        logger.info("\n[STAGE 1] DATA ENGINEERING")
        logger.info("-" * 60)
        self.data_loader = InsuranceDataLoader(self.data_path)
        self.data_loader.load_data()
        data_info = self.data_loader.explore_data()
        X_train, X_test, y_train, y_test, feature_names = self.data_loader.preprocess()
        
        feat_stats = self.data_loader.get_feature_statistics()
        logger.info(f"Features after encoding: {feat_stats['total_features_after_encoding']}")
        logger.info(f"Training samples: {feat_stats['training_samples']}")
        
        # 2. Deep Learning Model
        logger.info("\n[STAGE 2] DEEP LEARNING - RISK PREDICTION MLP")
        logger.info("-" * 60)
        self.ml_model = RiskPredictionMLP(
            input_dim=X_train.shape[1],
            use_gpu=self.use_gpu
        )
        self.ml_model.build_model()
        
        # Train with validation split
        history = self.ml_model.train(
            X_train, y_train,
            X_val=X_test, y_val=y_test,
            epochs=100,
            batch_size=32
        )
        
        # Evaluate
        metrics = self.ml_model.evaluate(X_test, y_test)
        logger.info(f"Model Performance - RMSE: ${metrics['rmse']:.2f}, R²: {metrics['r2_score']:.4f}")
        self.system_metrics['ml_model'] = metrics
        
        # Get predictions
        self.predictions = self.ml_model.predict(X_test)
        
        # 3. Reinforcement Learning Agent
        logger.info("\n[STAGE 3] REINFORCEMENT LEARNING - POLICY ADJUSTMENT")
        logger.info("-" * 60)
        self.rl_agent = PolicyAdjustmentAgent()
        
        # Prepare health metrics from test data
        health_metrics = []
        for idx in range(len(X_test)):
            health_metrics.append({
                'age': X_test.iloc[idx]['age'] if 'age' in X_test.columns else 30,
                'bmi': X_test.iloc[idx]['bmi'] if 'bmi' in X_test.columns else 25,
                'smoker': X_test.iloc[idx].get('smoker_yes', 0) if 'smoker_yes' in X_test.columns else 0
            })
        
        # Train agent with multiple episodes
        logger.info("Training RL agent...")
        for episode in range(20):
            reward = self.rl_agent.train_episode(health_metrics, self.predictions)
            if episode % 5 == 0:
                logger.info(f"Episode {episode}: Reward = {reward:.2f}")
        
        rl_summary = self.rl_agent.get_training_summary()
        logger.info(f"RL Agent - Episodes trained: {rl_summary['episodes_trained']}, "
                   f"Avg Reward: {rl_summary['average_reward']:.2f}")
        self.system_metrics['rl_agent'] = rl_summary
        
        # Get policy adjustments for test set
        self.rl_adjustments = []
        for idx, metrics in enumerate(health_metrics[:10]):  # First 10 samples
            adjustment = self.rl_agent.adjust_premium(
                metrics['bmi'],
                metrics['age'],
                metrics['smoker'],
                self.predictions[idx]
            )
            self.rl_adjustments.append(adjustment)
        
        # 4. Security Implementation
        logger.info("\n[STAGE 4] CYBERSECURITY - DATA PROTECTION")
        logger.info("-" * 60)
        self.security_manager = DataProtectionManager()
        
        # Demonstrate encryption on sample data
        sample_user_id = "USER_12345"
        sample_health = {'bmi': 28.5, 'age': 45, 'smoker': False}
        
        encrypted_id = self.security_manager.protect_user_id(sample_user_id)
        encrypted_health = self.security_manager.protect_health_info(sample_health)
        encrypted_claim, claim_hash = self.security_manager.protect_claim_records(
            "Claim_2024_03_15_$5000"
        )
        
        logger.info(f"RSA Encryption - User ID encrypted (sample): {encrypted_id[:50]}...")
        logger.info(f"RSA Encryption - Health info encrypted: {encrypted_health[:50]}...")
        logger.info(f"SHA-512 Hash - Claim integrity verified: {self.security_manager.verify_claim_integrity('Claim_2024_03_15_$5000')}")
        
        # 5. Analytics Dashboard
        logger.info("\n[STAGE 5] ANALYTICS - VISUALIZATION & INSIGHTS")
        logger.info("-" * 60)
        df_full = self.data_loader.get_preprocessed_df()
        self.dashboard = InsuranceAnalyticsDashboard(df_full, self.predictions)
        
        # Generate visualizations
        self.dashboard.plot_risk_distribution()
        self.dashboard.plot_age_bmi_correlation()
        self.dashboard.plot_demographic_breakdown()
        self.dashboard.plot_region_analysis()
        self.dashboard.plot_prediction_performance(y_test.values, self.predictions)
        
        logger.info("Generated 5 analytical visualizations")
        
        # 6. Explainable AI - Risk Factor Breakdown
        logger.info("\n[STAGE 6] EXPLAINABLE AI - RISK FACTOR BREAKDOWN")
        logger.info("-" * 60)
        
        sample_indices = [0, 10, 20]
        xai_results = []
        for idx in sample_indices:
            if idx < len(X_test):
                breakdown = self.ml_model.get_risk_factors_breakdown(
                    X_test.iloc[idx].values,
                    feature_names,
                    y_test.iloc[idx]
                )
                xai_results.append(breakdown)
                logger.info(f"\nSample {idx}: {breakdown['risk_level']} Risk")
                logger.info(f"  Predicted: ${breakdown['predicted_charge']:.2f}")
                logger.info(f"  Top Risk Factors:")
                for factor in breakdown['top_risk_factors'][:3]:
                    logger.info(f"    - {factor['factor']}: {factor['influence_score']:.4f}")
        
        self.system_metrics['xai_samples'] = xai_results
        
        # 7. Generate Summary Report
        logger.info("\n[STAGE 7] DIGITAL PULSE - SYSTEM SUMMARY")
        logger.info("-" * 60)
        
        summary = self.dashboard.generate_summary_report(metrics)
        logger.info("Digital Pulse Analytics Summary:")
        logger.info(f"  Total Records: {summary['total_records']}")
        logger.info(f"  Avg Insurance Charge: ${summary['average_charge']:.2f}")
        logger.info(f"  Charge Range: ${summary['min_charge']:.2f} - ${summary['max_charge']:.2f}")
        logger.info(f"  Average Age: {summary['average_age']:.1f} years")
        logger.info(f"  Average BMI: {summary['average_bmi']:.2f}")
        
        # Pipeline completion
        pipeline_duration = (datetime.now() - pipeline_start).total_seconds()
        logger.info("\n" + "=" * 60)
        logger.info(f"InsurGuard Pipeline Completed in {pipeline_duration:.2f} seconds")
        logger.info("=" * 60)
        
        return {
            'data_stats': feat_stats,
            'ml_metrics': metrics,
            'rl_summary': rl_summary,
            'analytics_summary': summary,
            'duration_seconds': pipeline_duration
        }
    
    def get_individual_risk_assessment(self, age: float, bmi: float, 
                                      smoker: bool, children: int = 0,
                                      region: str = 'northeast') -> Dict:
        """
        Get comprehensive risk assessment for an individual
        
        Args:
            age: Customer age
            bmi: Customer BMI
            smoker: Is customer a smoker
            children: Number of children
            region: Geographic region
            
        Returns:
            Complete risk assessment with XAI and policy adjustment
        """
        if self.ml_model is None or self.rl_agent is None:
            logger.warning("Model not trained. Run full_pipeline first.")
            return {}
        
        # Prepare features (needs to match training preprocessing)
        feature_dict = {
            'age': age,
            'bmi': bmi,
            'children': children,
            'sex_male': 1,  # Example
            'smoker_yes': 1 if smoker else 0,
            'region_northwest': 1 if region == 'northwest' else 0,
            'region_southeast': 1 if region == 'southeast' else 0,
            'region_southwest': 1 if region == 'southwest' else 0
        }
        
        # Dummy prediction (use trained model in real scenario)
        predicted_charge = np.random.uniform(5000, 50000)
        
        # Get RL adjustment
        rl_adjustment = self.rl_agent.adjust_premium(bmi, age, int(smoker), predicted_charge)
        
        # Encrypt sensitive info
        health_info = {
            'age': age,
            'bmi': bmi,
            'smoker': smoker
        }
        encrypted_health = self.security_manager.protect_health_info(health_info)
        
        return {
            'predicted_charge': float(predicted_charge),
            'policy_adjustment': rl_adjustment,
            'encrypted_health_info': encrypted_health[:50] + '...',
            'risk_level': self.ml_model._classify_risk(predicted_charge)
        }
    
    def save_results(self, output_dir: str = './results'):
        """Save all results and visualizations"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Save metrics
        metrics_file = os.path.join(output_dir, 'system_metrics.json')
        with open(metrics_file, 'w') as f:
            json.dump(self.system_metrics, f, indent=2, default=str)
        logger.info(f"Saved metrics to {metrics_file}")
        
        # Save visualizations
        self.dashboard.save_dashboard(os.path.join(output_dir, 'visualizations'))
        
        # Save RL adjustments
        if self.rl_adjustments:
            adj_file = os.path.join(output_dir, 'rl_policy_adjustments.json')
            with open(adj_file, 'w') as f:
                json.dump(self.rl_adjustments, f, indent=2)
            logger.info(f"Saved policy adjustments to {adj_file}")


def main():
    """Main execution"""
    data_path = './data/medical_insurance.csv'
    
    # Initialize and run system
    system = InsurGuardAISystem(data_path, use_gpu=False)
    
    try:
        results = system.run_full_pipeline()
        
        # Save all results
        system.save_results()
        
        # Example: Get assessment for new customer
        logger.info("\n[EXAMPLE] Individual Risk Assessment")
        assessment = system.get_individual_risk_assessment(
            age=35, bmi=28.5, smoker=True, children=2, region='northeast'
        )
        logger.info(f"Assessment: {json.dumps(assessment, indent=2, default=str)}")
        
    except Exception as e:
        logger.error(f"Pipeline error: {str(e)}", exc_info=True)
        raise


if __name__ == '__main__':
    main()
