import os
import pandas as pd
from typing import List, Tuple, Optional, Dict
from dataclasses import dataclass, field

@dataclass
class ValidationResult:
    """Result of file validation with research guidance."""
    is_valid: bool
    warnings: List[str] = field(default_factory=list)
    error: Optional[str] = None

class DataLoader:
    """Load and validate input data for topic modelling."""

    def validate_file(self, file_path: str) -> 'ValidationResult':
        """
        Validate file exists, is readable, and provide research guidance.
        """
        if not os.path.exists(file_path):
            return ValidationResult(is_valid=False, error="File not found.")

        if not file_path.lower().endswith(('.csv', '.txt')):
            return ValidationResult(is_valid=False, error="Unsupported file format. Please use .csv or .txt.")

        try:
            # Load a small sample to check content
            texts = self.load_texts(file_path)

            warnings = []
            num_docs = len(texts)

            # Research Guidance: Sample Size
            if num_docs < 50:
                warnings.append(f"Small sample size detected ({num_docs} docs). Topic modelling results may be unstable.")
            elif num_docs < 200:
                warnings.append(f"Moderate sample size ({num_docs} docs). Results may vary based on hyperparameters.")

            # Research Guidance: Content Check
            if num_docs > 0:
                avg_len = sum(len(t.split()) for t in texts) / num_docs
                if avg_len < 10:
                    warnings.append("Documents are very short on average. Consider combining rows or using a different data source.")

            return ValidationResult(is_valid=True, warnings=warnings)

        except Exception as e:
            return ValidationResult(is_valid=False, error=f"Error reading file: {str(e)}")

    def load_preview(self, file_path: str, n_lines: int = 10) -> List[str]:
        """Load first N lines for preview."""
        try:
            if file_path.lower().endswith('.csv'):
                df = pd.read_csv(file_path, nrows=n_lines)
                # Use the first text column found
                text_col = df.select_dtypes(include=['object']).columns[0]
                return df[text_col].astype(str).tolist()
            else:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return [f.readline().strip() for _ in range(n_lines)]
        except Exception as e:
            raise ValueError(f"Failed to load preview: {str(e)}")

    def load_texts(self, file_path: str) -> List[str]:
        """Load all documents from the file."""
        try:
            if file_path.lower().endswith('.csv'):
                df = pd.read_csv(file_path)
                text_col = df.select_dtypes(include=['object']).columns[0]
                return df[text_col].astype(str).tolist()
            else:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return [line.strip() for line in f if line.strip()]
        except Exception as e:
            raise ValueError(f"Failed to load texts: {str(e)}")
