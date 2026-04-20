"""
InsurGuard Data Processing Module
Handles data loading and advanced preprocessing
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InsuranceDataLoader:
    """Load and preprocess insurance data"""
    
    def __init__(self, data_path: str):
        """Initialize data loader with file path"""
        self.data_path = data_path
        self.df = None
        self.scaler = StandardScaler()
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.feature_names = None
        self.categorical_features = []
        self.numerical_features = []
    
    def load_data(self) -> pd.DataFrame:
        """Load CSV data"""
        logger.info(f"Loading data from {self.data_path}")
        self.df = pd.read_csv(self.data_path)
        logger.info(f"Loaded {len(self.df)} records with {len(self.df.columns)} columns")
        return self.df
    
    def explore_data(self) -> dict:
        """Provide data exploration summary"""
        info = {
            'shape': self.df.shape,
            'columns': self.df.columns.tolist(),
            'dtypes': self.df.dtypes.to_dict(),
            'missing': self.df.isnull().sum().to_dict(),
            'stats': self.df.describe().to_dict()
        }
        logger.info(f"Data shape: {info['shape']}")
        return info
    
    def preprocess(self, test_size: float = 0.2) -> tuple:
        """
        Advanced preprocessing with feature scaling and encoding
        
        Returns:
            Tuple of (X_train, X_test, y_train, y_test, feature_names)
        """
        logger.info("Starting preprocessing pipeline...")
        
        # Separate features and target
        X = self.df.drop('charges', axis=1)
        y = self.df['charges']
        
        # Identify feature types
        self.categorical_features = X.select_dtypes(include='object').columns.tolist()
        self.numerical_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
        
        logger.info(f"Numerical features: {self.numerical_features}")
        logger.info(f"Categorical features: {self.categorical_features}")
        
        # One-hot encoding for categorical features (lifestyle factors)
        X_encoded = pd.get_dummies(X, columns=self.categorical_features, drop_first=True)
        
        # Convert all columns to float64 to ensure numeric dtype
        X_encoded = X_encoded.astype('float64')
        
        # Feature scaling for BMI and Age
        scaling_features = ['age', 'bmi']
        X_encoded[scaling_features] = self.scaler.fit_transform(X_encoded[scaling_features])
        
        logger.info(f"After preprocessing: {X_encoded.shape[1]} features")
        
        # Train-test split
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X_encoded, y, test_size=test_size, random_state=42
        )
        
        self.feature_names = X_encoded.columns.tolist()
        
        logger.info(f"Training set: {self.X_train.shape}")
        logger.info(f"Test set: {self.X_test.shape}")
        
        return self.X_train, self.X_test, self.y_train, self.y_test, self.feature_names
    
    def get_feature_statistics(self) -> dict:
        """Get statistics on processed features"""
        return {
            'numerical_features': self.numerical_features,
            'categorical_features': self.categorical_features,
            'total_features_after_encoding': len(self.feature_names),
            'training_samples': len(self.X_train),
            'testing_samples': len(self.X_test),
            'target_mean': float(self.y_train.mean()),
            'target_std': float(self.y_train.std())
        }
    
    def get_preprocessed_df(self) -> pd.DataFrame:
        """Get the full preprocessed dataset"""
        X_full = self.df.drop('charges', axis=1)
        X_full = pd.get_dummies(X_full, columns=self.categorical_features, drop_first=True)
        X_full = X_full.astype('float64')
        X_full[['age', 'bmi']] = self.scaler.transform(X_full[['age', 'bmi']])
        X_full['charges'] = self.df['charges'].values
        return X_full
