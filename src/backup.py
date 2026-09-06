"""
backup.py

Realiza una copia de seguridad del Excel Maestro en la ruta donde reside el ejecutable/script.
"""

import sys
from pathlib import Path
from shutil import copy2


def get_app_dir() -> Path:
    """Devuelve la ruta raíz del directorio donde se ejecuta el .exe o el script principal."""
    if getattr(sys, 'frozen', False):
        # Si la app corre como .exe generado por PyInstaller
        return Path(sys.executable).parent
    else:
        # Si se ejecuta directamente desde Python (.py)
        return Path(__file__).resolve().parent.parent


class BackupManager:

    def __init__(self, origen: Path, carpeta_backup: Path = None):
        self.origen = origen
        
        # Si no se especifica ruta, asigna la carpeta 'backups' al lado del .exe
        if carpeta_backup is None:
            self.carpeta_backup = get_app_dir() / "backups"
        else:
            self.carpeta_backup = carpeta_backup

    def crear_backup(self) -> Path:
        if not self.origen.exists():
            raise FileNotFoundError(
                f"No existe el archivo de origen: {self.origen}"
            )

        # Crea la carpeta de respaldos si aún no existe
        self.carpeta_backup.mkdir(parents=True, exist_ok=True)

        # Nombre fijo del backup
        destino = (
            self.carpeta_backup /
            "CarbonFree_Master_BACKUP.xlsx"
        )

        # Sobrescribe el backup anterior
        copy2(
            self.origen,
            destino
        )

        return destino