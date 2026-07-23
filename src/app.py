"""
Clase principal de Carbon Free Importer
"""

from src.config import ConfigManager
from src.backup import BackupManager
from src.logger import LoggerManager
from src.excel import ExcelManager
from src.outlook import OutlookManager


class CarbonFreeApp:

    def __init__(self):

        self.config = ConfigManager()

        self.logger = LoggerManager(
            self.config.ruta_logs
        )

        self.outlook = OutlookManager(
            self.config,
            self.logger
        )

        self.excel = ExcelManager(
            self.config.ruta_maestro
        )

        self.backup = BackupManager(
            self.config.ruta_maestro,
            self.config.ruta_backups
        )

    def run(self):

        self.logger.info("=" * 50)
        self.logger.info("Carbon Free Importer iniciado")
        self.logger.info("=" * 50)

        print("\nCarbon Free Importer\n")

        # Verificar Outlook
        if not self.outlook.conectar():

            self.logger.warning(
                "No fue posible conectar con Outlook."
            )

            return

        # Crear Backup
        self.crear_backup()

        self.logger.info("Proceso finalizado correctamente.")

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