import unittest
from unittest.mock import patch, MagicMock
from src.install.project_name_utils import ProjectNameRetriever
from pathlib import Path

class TestProjectNameRetriever(unittest.TestCase):
    """
    Clase para probar la obtención del nombre del proyecto.
    """

    @patch('src.install.project_name_utils.Path')
    def test_get_project_name(self, mock_path):
        mock_path.return_value.name = 'Presupuestador'
        retriever = ProjectNameRetriever(mock_path.return_value)
        project_name = retriever.get_project_name()
        self.assertEqual(project_name, 'Presupuestador')

@patch('src.install.project_name_utils.Path')
def test_get_project_name_from_file(self, mock_path):
    mock_file_path = MagicMock()
    mock_file_path.read_text.return_value = 'Presupuestador'
    mock_path.return_value.__truediv__.return_value = mock_file_path
    
    retriever = ProjectNameRetriever(Path('/dummy/path'))
    project_name = retriever.get_project_name_from_file('project_name.txt')
    self.assertEqual(project_name, 'Presupuestador')

if __name__ == '__main__':
    unittest.main()