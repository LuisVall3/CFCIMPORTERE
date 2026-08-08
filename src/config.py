"""
config.py

Carga, valida y gestiona la configuración persistente de Carbon Free Importer.
"""

from pathlib import Path
import json
import os
import sys


class ConfigManager:
    """Gestiona la configuración de Carbon Free Importer."""

    def __init__(self):
        # Carpeta raíz del proyecto
        self.root = Path(__file__).resolve().parent.parent

        # 1. Definir ruta persistente fuera del directorio temporal del .exe
        if sys.platform == "win32":
            self.app_dir = Path(os.environ.get("APPDATA", Path.home())) / "NovaSource"
        else:
            self.app_dir = Path.home() / "Library" / "Application Support" / "NovaSource"

        self.app_dir.mkdir(parents=True, exist_ok=True)
        self.config_file = self.app_dir / "config.json"

        # 2. Cargar o crear configuración
        self.cargar_config()

    def _obtener_config_por_defecto(self) -> dict:
        """Devuelve la estructura básica si config.json no existe aún."""
        return {
            "correo": {
                "asunto": "CARBON FREE CHILE Daily Operator Log",
                "remitente": "fleet_performance@novasourcepower.com"
            },
            "rutas": {
                "descargas": "data/Descargas",
                "maestro": "",
                "historial": "data/historial.txt",
                "logs": "",
                "backups": "data/Backups"
            }
        }

    def cargar_config(self):
        """Lee el archivo JSON persistente o lo crea con valores por defecto."""
        if self.config_file.exists():
            try:
                with open(self.config_file, "r", encoding="utf-8") as file:
                    self.config = json.load(file)
            except Exception:
                self.config = self._obtener_config_por_defecto()
        else:
            self.config = self._obtener_config_por_defecto()
            self._guardar_json()

        self._create_directories()

    def _guardar_json(self):
        """Escribe directamente los datos de self.config en el archivo de usuario."""
        with open(self.config_file, "w", encoding="utf-8") as file:
            json.dump(self.config, file, indent=4, ensure_ascii=False)

    def _resolver_ruta(self, ruta_str: str) -> Path:
        """
        Convierte una cadena de texto en Path.
        Si la ruta es relativa, la resuelve desde la raíz del proyecto (self.root).
        Si es una ruta absoluta (ej. C:/... o /Users/...), la respeta.
        """
        if not ruta_str:
            return None
        
        path = Path(ruta_str)
        if path.is_absolute():
            return path
        return self.root / path

    def _create_directories(self):
        """Crea automáticamente las carpetas locales o configuradas si no existen."""
        rutas = self.config.get("rutas", {})

        descargas = self._resolver_ruta(rutas.get("descargas", "data/Descargas"))
        logs = self._resolver_ruta(rutas.get("logs"))
        backups = self._resolver_ruta(rutas.get("backups", "data/Backups"))

        carpetas = [descargas, logs, backups, self.root / "data", self.root / "data" / "Maestro"]

        for carpeta in carpetas:
            if carpeta:
                target = carpeta.parent if carpeta.suffix else carpeta
                target.mkdir(parents=True, exist_ok=True)

    def guardar_rutas(self, ruta_maestro: str, ruta_logs: str):
        """Guarda las nuevas rutas seleccionadas por el usuario en el config.json persistente."""
        if "rutas" not in self.config:
            self.config["rutas"] = {}

        self.config["rutas"]["maestro"] = ruta_maestro
        self.config["rutas"]["logs"] = ruta_logs

        self._guardar_json()
        self.cargar_config()

    @property
    def necesita_configuracion(self) -> bool:
        """Devuelve True si no se han definido las rutas de Maestro o Logs, o si no existen físicamente."""
        rutas = self.config.get("rutas", {})
        maestro = rutas.get("maestro", "")
        logs = rutas.get("logs", "")

        maestro_valido = bool(maestro) and Path(maestro).exists()
        logs_valido = bool(logs) and Path(logs).exists()

        return not (maestro_valido and logs_valido)

    # ==========================
    # PROPIEDADES DE ACCESO
    # ==========================

    @property
    def asunto(self):
        return self.config.get("correo", {}).get("asunto", "CARBON FREE CHILE Daily Operator Log")

    @property
    def remitente(self):
        return self.config.get("correo", {}).get("remitente", "fleet_performance@novasourcepower.com")

    @property
    def ruta_descargas(self):
        return Path.home() / "Downloads"

    @property
    def ruta_logs(self):
        return self._resolver_ruta(self.config["rutas"].get("logs", ""))

    @property
    def ruta_maestro(self):
        return self._resolver_ruta(self.config["rutas"].get("maestro", ""))

    @property
    def ruta_historial(self):
        return self._resolver_ruta(self.config["rutas"].get("historial", "data/historial.txt"))

    @property
    def ruta_backups(self):
        return self._resolver_ruta(self.config["rutas"].get("backups", "data/Backups"))