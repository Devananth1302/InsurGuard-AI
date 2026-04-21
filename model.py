import os
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import logging
import joblib
from typing import List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RiskPredictionMLP:

    def __init__(self, input_dim: int):
        self.input_dim = input_dim
        self.model = None

    def build_model(self):
        model = keras.Sequential([
            layers.Input(shape=(self.input_dim,)),
            layers.Dense(128, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.3),

            layers.Dense(64, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.3),

            layers.Dense(32, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.2),

            layers.Dense(1, activation='linear')
        ])

        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='mse',
            metrics=['mae']
        )

        self.model = model
        return model

    def train(self, X, y, epochs=50):
        X = np.array(X, dtype='float32')
        y = np.array(y, dtype='float32')

        self.model.fit(
            X, y,
            epochs=epochs,
            batch_size=32,
            verbose=1,
            callbacks=[
                keras.callbacks.EarlyStopping(
                    patience=10,
                    restore_best_weights=True
                )
            ]
        )

    def predict(self, X):
        X = np.array(X, dtype='float32')
        return self.model.predict(X).flatten()

    def save_model(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.model.save(path)
        logger.info(f"Model saved at {path}")

    def load_model(self, path):
        self.model = keras.models.load_model(path)
        logger.info(f"Model loaded from {path}")


# ================= TRAINING =================

def train_and_save():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    data_path = os.path.join(BASE_DIR, "data", "medical_insurance.csv")
    save_dir = os.path.join(BASE_DIR, "saved_models")
    model_path = os.path.join(save_dir, "mlp_model.keras")
    columns_path = os.path.join(save_dir, "columns.pkl")

    logger.info("🚀 Training model...")

    df = pd.read_csv(data_path)

    # One-hot encoding
    df = pd.get_dummies(df, columns=['sex', 'smoker', 'region'], drop_first=False)

    # Save feature columns
    feature_columns = df.drop(columns=['charges']).columns.tolist()
    os.makedirs(save_dir, exist_ok=True)
    joblib.dump(feature_columns, columns_path)

    logger.info(f"✅ Saved feature columns ({len(feature_columns)})")

    X = df.drop(columns=['charges']).values
    y = df['charges'].values

    model = RiskPredictionMLP(input_dim=X.shape[1])
    model.build_model()
    model.train(X, y)

    model.save_model(model_path)

    logger.info("✅ Training complete!")


if __name__ == "__main__":
    train_and_save()