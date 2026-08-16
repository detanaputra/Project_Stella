import os
import webbrowser
from typing import Dict, Optional
from app.models.topic_result import TopicResult

class TopicVisualizer:
    """Generate interactive visualizations for export to browser."""

    def __init__(self, output_dir: Optional[str] = None):
        self.output_dir = output_dir or "exports/viz"
        os.makedirs(self.output_dir, exist_ok=True)

    def visualize(self, result: TopicResult, algorithm_name: str) -> Dict[str, str]:
        """
        Generate visualizations for the given algorithm result.
        """
        # BERTopic provides high-level visualization methods if the model is in metadata
        if algorithm_name == "BERTopic" and 'model' in result.metadata:
            model = result.metadata['model']

            # In a real implementation, we would call:
            # fig = model.visualize_topics()
            # fig.write_html(path)

            # For now, we simulate the file creation to maintain the interface
            viz_files = {
                'topics': os.path.join(self.output_dir, 'topics.html'),
                'documents': os.path.join(self.output_dir, 'documents.html'),
                'heatmap': os.path.join(self.output_dir, 'heatmap.html')
            }

            for path in viz_files.values():
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(f"<html><body><h1>{algorithm_name} Visualization</h1><p>Interactive plot placeholder.</p></body></html>")

            return viz_files

        return {}

    def open_visualization(self, file_path: str) -> None:
        """Open a visualization file in the default browser."""
        webbrowser.open(f"file://{os.path.abspath(file_path)}")
