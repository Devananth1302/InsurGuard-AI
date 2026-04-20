"""
InsurGuard Deep Learning Model
Multi-Layer Perceptron for risk prediction with XAI support
"""

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import logging
from typing import Dict, Tuple, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RiskPredictionMLP:
    """Multi-Layer Perceptron for insurance risk assessment"""
    
    def __init__(self, input_dim: int, use_gpu: bool = False):
        """
        Initialize MLP model
        
        Args:
            input_dim: Number of input features
            use_gpu: Whether to use GPU acceleration
        """
        self.input_dim = input_dim
        self.use_gpu = use_gpu
        self.model = None
        self.history = None
        self.feature_names = None
        self.feature_importance = None
        
        # Set device
        if use_gpu:
            self.device = '/GPU:0'
            logger.info("GPU acceleration enabled")
        else:
            self.device = '/CPU:0'
            logger.info("Using CPU")
    
    def build_model(self, layers_config: List[int] = None) -> keras.Model:
        """
        Build MLP architecture
        
        Args:
            layers_config: List of neuron counts per hidden layer
                          Default: [128, 64, 32]
        """
        if layers_config is None:
            layers_config = [128, 64, 32]
        
        logger.info(f"Building MLP with architecture: {layers_config}")
        
        with tf.device(self.device):
            model = keras.Sequential([
                layers.Input(shape=(self.input_dim,)),
                layers.Dense(layers_config[0], activation='relu'),
                layers.BatchNormalization(),
                layers.Dropout(0.3),
                
                layers.Dense(layers_config[1], activation='relu'),
                layers.BatchNormalization(),
                layers.Dropout(0.3),
                
                layers.Dense(layers_config[2], activation='relu'),
                layers.BatchNormalization(),
                layers.Dropout(0.2),
                
                layers.Dense(1, activation='linear')
            ])
            
            model.compile(
                optimizer=keras.optimizers.Adam(learning_rate=0.001),
                loss='mse',
                metrics=['mae', 'mse']
            )
        
        self.model = model
        logger.info(model.summary())
        return model
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray,
              X_val: np.ndarray = None, y_val: np.ndarray = None,
              epochs: int = 100, batch_size: int = 32) -> Dict:
        """
        Train the MLP model
        
        Args:
            X_train: Training features
            y_train: Training targets (charges)
            X_val: Validation features
            y_val: Validation targets
            epochs: Number of training epochs
            batch_size: Batch size for training
            
        Returns:
            Training history dictionary
        """
        logger.info(f"Starting training for {epochs} epochs on {self.device}")
        
        # Ensure data types are correct
        X_train = np.array(X_train, dtype='float32')
        y_train = np.array(y_train, dtype='float32')
        
        with tf.device(self.device):
            val_data = None
            if X_val is not None and y_val is not None:
                X_val = np.array(X_val, dtype='float32')
                y_val = np.array(y_val, dtype='float32')
                val_data = (X_val, y_val)
            
            self.history = self.model.fit(
                X_train, y_train,
                validation_data=val_data,
                epochs=epochs,
                batch_size=batch_size,
                verbose=1,
                callbacks=[
                    keras.callbacks.EarlyStopping(
                        monitor='val_loss' if val_data else 'loss',
                        patience=15,
                        restore_best_weights=True
                    )
                ]
            )
        
        logger.info("Training completed")
        return self.history.history
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict insurance charges/risk scores"""
        # Ensure X is a numpy array with float32 dtype
        if isinstance(X, np.ndarray):
            X = X.astype('float32')
        else:
            X = np.array(X, dtype='float32')
        
        with tf.device(self.device):
            predictions = self.model.predict(X, verbose=0)
        return predictions.flatten()
    
    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> Dict:
        """Evaluate model on test set"""
        # Ensure X_test is float32
        X_test = np.array(X_test, dtype='float32')
        y_test = np.array(y_test, dtype='float32')
        
        with tf.device(self.device):
            loss, mae, mse = self.model.evaluate(X_test, y_test, verbose=0)
        
        predictions = self.predict(X_test)
        rmse = np.sqrt(np.mean((predictions - y_test) ** 2))
        r2 = 1 - (np.sum((y_test - predictions) ** 2) / 
                  np.sum((y_test - np.mean(y_test)) ** 2))
        
        metrics = {
            'loss': float(loss),
            'mae': float(mae),
            'mse': float(mse),
            'rmse': float(rmse),
            'r2_score': float(r2)
        }
        
        logger.info(f"Test Metrics - RMSE: {rmse:.2f}, R²: {r2:.4f}")
        return metrics
    
    def get_risk_factors_breakdown(self, X_sample: np.ndarray, 
                                   feature_names: List[str],
                                   y_actual: float = None) -> Dict:
        """
        Generate explainable AI risk factor breakdown
        
        Args:
            X_sample: Single sample or batch
            feature_names: Names of features
            y_actual: Actual charge value (optional)
            
        Returns:
            Dictionary with risk breakdown
        """
        if X_sample.ndim == 1:
            X_sample = X_sample.reshape(1, -1)
        
        prediction = self.predict(X_sample)[0]
        
        # Calculate feature influence using permutation importance
        # For each feature, calculate how much removing it changes prediction
        baseline_pred = prediction
        feature_importance = {}
        
        for i, feat_name in enumerate(feature_names):
            X_permuted = X_sample.copy()
            X_permuted[0, i] = np.random.normal(0, 1)
            permuted_pred = self.predict(X_permuted)[0]
            importance = abs(baseline_pred - permuted_pred)
            feature_importance[feat_name] = float(importance)
        
        # Sort by importance
        sorted_features = sorted(
            feature_importance.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]  # Top 5 features
        
        breakdown = {
            'predicted_charge': float(prediction),
            'risk_level': self._classify_risk(prediction),
            'top_risk_factors': [
                {
                    'factor': feat,
                    'influence_score': score
                }
                for feat, score in sorted_features
            ],
            'actual_charge': float(y_actual) if y_actual is not None else None
        }
        
        return breakdown
    
    @staticmethod
    def _classify_risk(charge: float) -> str:
        """Classify risk level based on predicted charge"""
        if charge < 10000:
            return "LOW"
        elif charge < 20000:
            return "MEDIUM"
        elif charge < 35000:
            return "HIGH"
        else:
            return "CRITICAL"
    
    def save_model(self, path: str):
        """Save trained model"""
        self.model.save(path)
        logger.info(f"Model saved to {path}")
    
    def load_model(self, path: str):
        """Load trained model"""
        self.model = keras.models.load_model(path)
        logger.info(f"Model loaded from {path}")
