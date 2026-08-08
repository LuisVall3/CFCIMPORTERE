"""
backup.py

Realiza una copia de seguridad del Excel Maestro.
"""

from pathlib import Path
from shutil import copy2


class BackupManager:

    def __init__(self, origen: Path, carpeta_backup: Path):

        self.origen = origen
        self.carpeta_backup = carpeta_backup

    def crear_backup(self):

        if not self.origen.exists():
            raise FileNotFoundError(
                f"No existe el archivo {self.origen}"
            )

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