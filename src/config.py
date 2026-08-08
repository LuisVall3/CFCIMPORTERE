# """
# config.py

# Carga y valida la configuración del programa.
# """

# from pathlib import Path
# import json


# class ConfigManager:
#     """Gestiona la configuración de Carbon Free Importer."""

#     def __init__(self):

#         # Carpeta raíz del proyecto
#         self.root = Path(__file__).resolve().parent.parent

#         # Archivo de configuración
#         self.config_file = self.root / "config.json"

#         if not self.config_file.exists():
#             raise FileNotFoundError(
#                 f"No existe el archivo {self.config_file}"
#             )

#         with open(self.config_file, "r", encoding="utf-8") as file:
#             self.config = json.load(file)

#         self._create_directories()

#     def _create_directories(self):
#         """Crea automáticamente las carpetas necesarias."""

#         rutas = self.config["rutas"]

#         carpetas = [
#             self.root / rutas["descargas"],
#             self.root / rutas["logs"],
#             self.root / rutas["backups"],
#             self.root / "data",
#             self.root / "data" / "Maestro",
#         ]

#         for carpeta in carpetas:
#             carpeta.mkdir(parents=True, exist_ok=True)

#     @property
#     def asunto(self):
#         return self.config["correo"]["asunto"]

#     @property
#     def remitente(self):
#         return self.config["correo"]["remitente"]

#     @property
#     def ruta_descargas(self):
#         return Path.home() / "Downloads"

#     @property
#     def ruta_logs(self):
#         return self.root / self.config["rutas"]["logs"]

#     @property
#     def ruta_maestro(self):
#         return self.root / self.config["rutas"]["maestro"]

#     @property
#     def ruta_historial(self):
#         return self.root / self.config["rutas"]["historial"]

#     @property
#     def ruta_backups(self):
#         return self.root / self.config["rutas"]["backups"]

#     @property
#     def carpeta_maestro(self):
#         return self.root / "data" / "Maestro"

"""
config.py

Carga, valida y gestiona la configuración de Carbon Free Importer.
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

        self.cargar_config()

    def cargar_config(self):
        """Lee el archivo JSON de configuración."""
        with open(self.config_file, "r", encoding="utf-8") as file:
            self.config = json.load(file)
        
        self._create_directories()

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

        # Resolvemos las carpetas principales
        descargas = self._resolver_ruta(rutas.get("descargas", "data/Descargas"))
        logs = self._resolver_ruta(rutas.get("logs"))
        backups = self._resolver_ruta(rutas.get("backups", "data/Backups"))

        carpetas = [descargas, logs, backups, self.root / "data", self.root / "data" / "Maestro"]

        for carpeta in carpetas:
            if carpeta:
                # Si se configuró la ruta del maestro como archivo, tomamos solo su carpeta padre
                target = carpeta.parent if carpeta.suffix else carpeta
                target.mkdir(parents=True, exist_ok=True)

    def guardar_rutas(self, ruta_maestro: str, ruta_logs: str):
        """Guarda las nuevas rutas seleccionadas por el usuario en el config.json."""
        self.config["rutas"]["maestro"] = ruta_maestro
        self.config["rutas"]["logs"] = ruta_logs

        with open(self.config_file, "w", encoding="utf-8") as file:
            json.dump(self.config, file, indent=4, ensure_ascii=False)

        # Recargamos en memoria y aseguramos que las carpetas existan
        self.cargar_config()

    @property
    def necesita_configuracion(self) -> bool:
        """Devuelve True si no se han definido las rutas de Maestro o Logs."""
        rutas = self.config.get("rutas", {})
        maestro_valido = bool(rutas.get("maestro"))
        logs_valido = bool(rutas.get("logs"))
        return not (maestro_valido and logs_valido)

    # ==========================
    # PROPIEDADES DE ACCESO
    # ==========================

    @property
    def asunto(self):
        return self.config["correo"]["asunto"]

    @property
    def remitente(self):
        return self.config["correo"]["remitente"]

    @property
    def ruta_descargas(self):
        return Path.home() / "Downloads"

    @property
    def ruta_logs(self):
        return self._resolver_ruta(self.config["rutas"]["logs"])

    @property
    def ruta_maestro(self):
        return self._resolver_ruta(self.config["rutas"]["maestro"])

    @property
    def ruta_historial(self):
        return self._resolver_ruta(self.config["rutas"]["historial"])

    @property
    def ruta_backups(self):
        return self._resolver_ruta(self.config["rutas"]["backups"])