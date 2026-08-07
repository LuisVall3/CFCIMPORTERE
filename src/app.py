"""
Clase principal de Carbon Free Importer
"""

from src.config import ConfigManager
from src.backup import BackupManager
from src.logger import LoggerManager
from src.excel import ExcelManager
from src.outlook import OutlookManager
from src.history import HistoryManager


class CarbonFreeApp:

    def __init__(self):

        self.config = ConfigManager()

        self.logger = LoggerManager(
            self.config.ruta_logs
        )
        self.history = HistoryManager(
            self.config.ruta_historial
        )

        self.outlook = OutlookManager(
            self.config,
            self.logger,
            self.history
        )

        self.excel = ExcelManager(
            self.config.ruta_maestro
        )

        self.backup = BackupManager(
            self.config.ruta_maestro,
            self.config.ruta_backups
        )

    def run(self, callback=print):

        callback("Buscando correo...")

        archivo = self.outlook.obtener_excel()

        if archivo is None:

            callback("No existen correos nuevos.")

            return

        callback("Correo encontrado.")

        try:

            self.backup.crear_backup()

            callback("Backup creado.")

        except FileNotFoundError:

            callback("No existe Excel maestro.")

        filas = self.excel.agregar_registros(archivo)

        callback(f"{filas} filas agregadas.")

        callback("Proceso terminado.")
        
    def crear_backup(self):

        try:

            self.logger.info(
                "Creando Backup..."
            )

            archivo = self.backup.crear_backup()

            self.logger.info(
                f"Backup creado: {archivo.name}"
            )

            print("✅ Backup creado.")

        except FileNotFoundError:

            self.logger.warning(
                "Excel Maestro inexistente."
            )

            print(
                "⚠ Excel Maestro no encontrado."
            )