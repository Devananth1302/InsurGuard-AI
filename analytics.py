"""
InsurGuard Analytics Dashboard
Visualization of healthcare risk distributions and claim patterns
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set style
sns.set_style("whitegrid")
sns.set_palette("husl")


class InsuranceAnalyticsDashboard:
    """Create comprehensive analytics visualizations"""
    
    def __init__(self, df: pd.DataFrame, predictions: np.ndarray = None):
        """
        Initialize dashboard
        
        Args:
            df: Preprocessed dataframe
            predictions: Model predictions (optional)
        """
        self.df = df
        self.predictions = predictions
        self.figures = {}
        logger.info("Analytics Dashboard initialized")
    
    def plot_risk_distribution(self, figsize: Tuple = (12, 6)) -> plt.Figure:
        """Plot healthcare risk distribution by demographic"""
        fig, axes = plt.subplots(1, 2, figsize=figsize)
        
        # Risk by smoking status
        if 'smoker_yes' in self.df.columns:
            smoker_col = 'smoker_yes'
        else:
            smoker_col = 'smoker'
        
        smoker_charges = self.df[self.df[smoker_col] == 1]['charges'] if smoker_col in self.df.columns else []
        non_smoker_charges = self.df[self.df[smoker_col] == 0]['charges'] if smoker_col in self.df.columns else self.df['charges']
        
        # Box plot
        data_box = [non_smoker_charges, smoker_charges] if len(smoker_charges) > 0 else [self.df['charges']]
        axes[0].boxplot(data_box, labels=['Non-Smoker', 'Smoker'] if len(smoker_charges) > 0 else ['All'])
        axes[0].set_ylabel('Insurance Charges ($)', fontsize=11)
        axes[0].set_title('Risk Distribution by Smoking Status', fontsize=12, fontweight='bold')
        axes[0].grid(True, alpha=0.3)
        
        # Distribution histogram
        axes[1].hist(self.df['charges'], bins=30, color='skyblue', edgecolor='black', alpha=0.7)
        if self.predictions is not None:
            axes[1].hist(self.predictions, bins=30, color='coral', edgecolor='black', alpha=0.5, label='Predicted')
            axes[1].legend()
        axes[1].set_xlabel('Charges ($)', fontsize=11)
        axes[1].set_ylabel('Frequency', fontsize=11)
        axes[1].set_title('Overall Risk Distribution', fontsize=12, fontweight='bold')
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        self.figures['risk_distribution'] = fig
        return fig
    
    def plot_age_bmi_correlation(self, figsize: Tuple = (10, 8)) -> plt.Figure:
        """Plot age and BMI correlation with charges"""
        fig = plt.figure(figsize=figsize)
        
        # Prepare data
        plot_df = self.df.copy()
        
        # Create scatter plot with color coding
        if 'smoker_yes' in plot_df.columns:
            colors = plot_df['smoker_yes'].map({1: 'red', 0: 'blue'})
            labels = {1: 'Smoker', 0: 'Non-Smoker'}
        else:
            colors = 'steelblue'
            labels = None
        
        scatter = plt.scatter(plot_df['age'], plot_df['bmi'], c=colors, s=50, 
                             alpha=0.6, edgecolors='black', linewidth=0.5)
        
        # Color bar for charges
        scatter2 = plt.scatter(plot_df['age'], plot_df['bmi'], c=plot_df['charges'], 
                              cmap='YlOrRd', s=50, alpha=0.6, edgecolors='black', linewidth=0.5)
        
        cbar = plt.colorbar(scatter2)
        cbar.set_label('Insurance Charges ($)', fontsize=11)
        
        plt.xlabel('Age (years)', fontsize=12, fontweight='bold')
        plt.ylabel('BMI (Body Mass Index)', fontsize=12, fontweight='bold')
        plt.title('Age-BMI Correlation with Risk Score', fontsize=13, fontweight='bold')
        plt.grid(True, alpha=0.3)
        
        self.figures['age_bmi'] = fig
        return fig
    
    def plot_demographic_breakdown(self, figsize: Tuple = (14, 5)) -> plt.Figure:
        """Plot claims and demographics breakdown"""
        fig, axes = plt.subplots(1, 3, figsize=figsize)
        
        # Age distribution
        axes[0].hist(self.df['age'], bins=15, color='skyblue', edgecolor='black', alpha=0.7)
        axes[0].set_xlabel('Age', fontsize=11)
        axes[0].set_ylabel('Count', fontsize=11)
        axes[0].set_title('Age Distribution', fontsize=12, fontweight='bold')
        axes[0].grid(True, alpha=0.3)
        
        # BMI distribution
        axes[1].hist(self.df['bmi'], bins=20, color='lightgreen', edgecolor='black', alpha=0.7)
        axes[1].set_xlabel('BMI', fontsize=11)
        axes[1].set_ylabel('Count', fontsize=11)
        axes[1].set_title('BMI Distribution', fontsize=12, fontweight='bold')
        axes[1].grid(True, alpha=0.3)
        
        # Children count
        if 'children' in self.df.columns:
            children_counts = self.df['children'].value_counts().sort_index()
            axes[2].bar(children_counts.index, children_counts.values, color='coral', edgecolor='black', alpha=0.7)
            axes[2].set_xlabel('Number of Children', fontsize=11)
            axes[2].set_ylabel('Count', fontsize=11)
            axes[2].set_title('Children Distribution', fontsize=12, fontweight='bold')
            axes[2].grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        self.figures['demographics'] = fig
        return fig
    
    def plot_region_analysis(self, figsize: Tuple = (12, 5)) -> plt.Figure:
        """Plot claims by region"""
        fig, axes = plt.subplots(1, 2, figsize=figsize)
        
        if 'region' in self.df.columns:
            # Region vs charges boxplot
            region_data = [self.df[self.df['region'] == reg]['charges'].values 
                          for reg in self.df['region'].unique()]
            axes[0].boxplot(region_data, labels=sorted(self.df['region'].unique()))
            axes[0].set_ylabel('Insurance Charges ($)', fontsize=11)
            axes[0].set_title('Risk Distribution by Region', fontsize=12, fontweight='bold')
            axes[0].grid(True, alpha=0.3, axis='y')
            axes[0].tick_params(axis='x', rotation=45)
            
            # Region counts
            region_counts = self.df['region'].value_counts()
            axes[1].bar(region_counts.index, region_counts.values, color='steelblue', 
                       edgecolor='black', alpha=0.7)
            axes[1].set_ylabel('Count', fontsize=11)
            axes[1].set_title('Sample Distribution by Region', fontsize=12, fontweight='bold')
            axes[1].grid(True, alpha=0.3, axis='y')
            axes[1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        self.figures['region'] = fig
        return fig
    
    def plot_prediction_performance(self, y_true: np.ndarray, y_pred: np.ndarray,
                                   figsize: Tuple = (12, 5)) -> plt.Figure:
        """Plot actual vs predicted charges"""
        fig, axes = plt.subplots(1, 2, figsize=figsize)
        
        # Actual vs Predicted scatter
        axes[0].scatter(y_true, y_pred, alpha=0.6, s=30, edgecolors='black', linewidth=0.5)
        axes[0].plot([y_true.min(), y_true.max()], [y_true.min(), y_true.max()], 
                    'r--', lw=2, label='Perfect Prediction')
        axes[0].set_xlabel('Actual Charges ($)', fontsize=11)
        axes[0].set_ylabel('Predicted Charges ($)', fontsize=11)
        axes[0].set_title('Actual vs Predicted Charges', fontsize=12, fontweight='bold')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # Residuals
        residuals = y_true - y_pred
        axes[1].scatter(y_pred, residuals, alpha=0.6, s=30, edgecolors='black', linewidth=0.5)
        axes[1].axhline(y=0, color='r', linestyle='--', lw=2)
        axes[1].set_xlabel('Predicted Charges ($)', fontsize=11)
        axes[1].set_ylabel('Residuals ($)', fontsize=11)
        axes[1].set_title('Prediction Residuals', fontsize=12, fontweight='bold')
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        self.figures['performance'] = fig
        return fig
    
    def save_dashboard(self, output_dir: str = './visualizations'):
        """Save all plots"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        for name, fig in self.figures.items():
            path = os.path.join(output_dir, f'{name}.png')
            fig.savefig(path, dpi=300, bbox_inches='tight')
            logger.info(f"Saved {name} to {path}")
    
    def generate_summary_report(self, metrics: Dict = None) -> Dict:
        """Generate analytics summary"""
        report = {
            'total_records': len(self.df),
            'average_charge': float(self.df['charges'].mean()),
            'median_charge': float(self.df['charges'].median()),
            'std_charge': float(self.df['charges'].std()),
            'min_charge': float(self.df['charges'].min()),
            'max_charge': float(self.df['charges'].max()),
            'average_age': float(self.df['age'].mean()),
            'average_bmi': float(self.df['bmi'].mean())
        }
        
        if 'region' in self.df.columns:
            report['regions'] = self.df['region'].nunique()
        
        if metrics:
            report.update(metrics)
        
        return report
