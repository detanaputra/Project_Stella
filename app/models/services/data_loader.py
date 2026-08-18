import os
import pandas as pd
from typing import List, Optional
from dataclasses import dataclass, field

@dataclass
class ValidationResult:
    """Result of file validation with research guidance."""
    is_valid: bool
    warnings: List[str] = field(default_factory=list)
    error: Optional[str] = None

class DataLoader:
    """Load and validate input data for topic modelling."""

    #: Encodings tried in order for text files and CSV (audit M6).
    _ENCODINGS = ('utf-8', 'latin-1')

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
                df = self._read_csv(file_path)
                text_col = self._pick_text_column(df)
                return df[text_col].dropna().astype(str).str.strip().head(n_lines).tolist()
            else:
                return self._read_text_file(file_path)[:n_lines]
        except Exception as e:
            raise ValueError(f"Failed to load preview: {str(e)}")

    def load_texts(self, file_path: str) -> List[str]:
        """Load all documents from the file."""
        try:
            if file_path.lower().endswith('.csv'):
                df = self._read_csv(file_path)
                text_col = self._pick_text_column(df)
                # Drop NaN cells, empty and whitespace-only rows so the model
                # never trains on the literal string "nan" (audit M6).
                series = df[text_col].dropna().astype(str).str.strip()
                return series[series.str.len() > 0].tolist()
            else:
                return self._read_text_file(file_path)
        except Exception as e:
            raise ValueError(f"Failed to load texts: {str(e)}")

    def _read_csv(self, file_path: str) -> pd.DataFrame:
        """Read a CSV, falling back to latin-1 when utf-8 fails (audit M6)."""
        try:
            return pd.read_csv(file_path)
        except UnicodeDecodeError:
            return pd.read_csv(file_path, encoding='latin-1')

    def _read_text_file(self, file_path: str) -> List[str]:
        """Read a .txt file, trying encodings in order (audit M6)."""
        for encoding in self._ENCODINGS:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    return [line.strip() for line in f if line.strip()]
            except UnicodeDecodeError:
                continue
        raise ValueError(f"Unable to decode file with encodings: {', '.join(self._ENCODINGS)}")

    def _pick_text_column(self, df: pd.DataFrame) -> str:
        """Choose the first text (object) column, raising a clear error if
        the CSV has no text column at all instead of an IndexError (audit M6)."""
        text_cols = df.select_dtypes(include=['object']).columns
        if len(text_cols) == 0:
            raise ValueError(
                "No text column found. Please ensure the CSV contains at least "
                "one column of text data."
            )
        return str(text_cols[0])
