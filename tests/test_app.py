"""
test_app.py

Pruebas unitarias para verificar los módulos de Configuración, 
Backups y la presencia del archivo .spec.
"""

from pathlib import Path
import pytest
from src.config import ConfigManager
from src.backup import BackupManager


def test_config_initialization():
    """Verifica que ConfigManager inicialice sus rutas por defecto sin arrojar excepciones."""
    config = ConfigManager()
    assert config.app_dir is not None
    assert isinstance(config.app_dir, Path)
    assert config.config_file.name == "config.json"


def test_backup_manager_creation(tmp_path):
    """Verifica que BackupManager cree la copia del Maestro en el directorio indicado."""
    # Crear un archivo Excel simulado en un directorio temporal
    origen_mock = tmp_path / "Master_Simulado.xlsx"
    origen_mock.write_text("contenido simulado del archivo maestro")

    carpeta_backup_mock = tmp_path / "backups"

    # Instanciar el manager pasándole las rutas temporales
    backup_mgr = BackupManager(origen=origen_mock, carpeta_backup=carpeta_backup_mock)
    destino = backup_mgr.crear_backup()

    # Validaciones
    assert destino.exists()
    assert destino.name == "CarbonFree_Master_BACKUP.xlsx"
    assert destino.parent == carpeta_backup_mock


def test_spec_file_exists():
    """Asegura que el archivo app.spec exista en la raíz del proyecto para evitar fallos en CI/CD."""
    root_dir = Path(__file__).resolve().parent.parent
    spec_path = root_dir / "app.spec"
    assert spec_path.exists(), "El archivo app.spec no fue encontrado en la raíz del repositorio."