"""
backup.py

Realiza copias de seguridad del Excel maestro.
"""

from pathlib import Path
from shutil import copy2
from datetime import datetime


class BackupManager:

    def __init__(self, origen: Path, carpeta_backup: Path):

        self.origen = origen
        self.carpeta_backup = carpeta_backup

    def crear_backup(self):

        if not self.origen.exists():
            raise FileNotFoundError(
                f"No existe el archivo {self.origen}"
            )

        fecha = datetime.now().strftime("%Y%m%d_%H%M%S")

        nombre = f"{self.origen.stem}_{fecha}{self.origen.suffix}"

        destino = self.carpeta_backup / nombre

        copy2(self.origen, destino)

        return destino