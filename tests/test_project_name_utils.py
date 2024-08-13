"""
tests/test_project_name_utils.py
Test module for ProjectNameRetriever class.
"""

import tempfile
import unittest
from pathlib import Path
from src.install.project_name_utils import ProjectNameRetriever

class TestProjectNameRetriever(unittest.TestCase):
    """Clase de prueba para la clase ProjectNameRetriever."""

    def test_get_project_name(self):
        """Prueba el método get_project_name."""
        retriever = ProjectNameRetriever(Path("/some/path/to/project"))
        self.assertEqual(retriever.get_project_name(), "project")

    def test_get_project_name_from_file(self):
        """Prueba el método get_project_name_from_file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)
            temp_file = temp_dir_path / "project_name.txt"
            temp_file.write_text("expected_project_name")

            retriever = ProjectNameRetriever(temp_dir_path)
            self.assertEqual(
                retriever.get_project_name_from_file("project_name.txt"),
                "expected_project_name"
            )

if __name__ == "__main__":
    unittest.main()
