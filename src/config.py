"""
config.py

Carga y valida la configuración del programa.
"""

from pathlib import Path
import json


class ConfigManager:
    """Gestiona la configuración de Carbon Free Importer."""

    def __init__(self):

        # Carpeta raíz del proyecto
        self.root = Path(__file__).resolve().parent.parent

        # Archivo de configuración
        self.config_file = self.root / "config.json"

        if not self.config_file.exists():
            raise FileNotFoundError(
                f"No existe el archivo {self.config_file}"
            )

        with open(self.config_file, "r", encoding="utf-8") as file:
            self.config = json.load(file)

        self._create_directories()

    def _create_directories(self):
        """Crea automáticamente las carpetas necesarias."""

        rutas = self.config["rutas"]

        carpetas = [
            self.root / rutas["descargas"],
            self.root / rutas["logs"],
            self.root / rutas["backups"],
            self.root / "data",
            self.root / "data" / "Maestro",
        ]

        for carpeta in carpetas:
            carpeta.mkdir(parents=True, exist_ok=True)

    @property
    def asunto(self):
        return self.config["correo"]["asunto"]

    @property
    def remitente(self):
        return self.config["correo"]["remitente"]

    @property
    def ruta_descargas(self):
        return self.root / self.config["rutas"]["descargas"]

    @property
    def ruta_logs(self):
        return self.root / self.config["rutas"]["logs"]

    @property
    def ruta_maestro(self):
        return self.root / self.config["rutas"]["maestro"]

    @property
    def ruta_historial(self):
        return self.root / self.config["rutas"]["historial"]

    @property
    def ruta_backups(self):
        return self.root / self.config["rutas"]["backups"]

    @property
    def carpeta_maestro(self):
        return self.root / "data" / "Maestro"