"""
app.py

Clase principal de Carbon Free Importer.
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
            self.logger,

        )

        self.excel = ExcelManager(
            self.config.ruta_maestro
        )

        self.backup = BackupManager(
            self.config.ruta_maestro,
            self.config.ruta_backups
        )

    def run(self, escribir=None):

        def log(mensaje):

            self.logger.info(mensaje)

            if escribir:
                escribir(mensaje)

            print(mensaje)

        log("===================================")
        log("Carbon Free Importer iniciado")
        log("===================================")

        # Buscar reporte
        log("Buscando reporte diario...")

        archivo = self.outlook.obtener_excel()

        if not archivo:

            log("No se encontró un reporte nuevo.")

            return

        log(f"Reporte encontrado: {archivo.name}")

        # Backup
        if self.excel.existe():

            log("Creando backup del Excel Maestro...")

            backup = self.backup.crear_backup()

            log(f"Backup creado: {backup.name}")

        else:

            log("El Excel Maestro todavía no existe.")

        # Actualizar maestro
        log("Actualizando Excel Maestro...")

        try:

            registros = self.excel.agregar_registros(
                archivo
            )

            log(
                f"Registros nuevos agregados: {registros}"
            )

            # Eliminar archivo SOLO si la importación fue exitosa
            archivo.unlink()

            log(
                f"Archivo procesado eliminado: {archivo.name}"
            )

        except Exception as e:

            self.logger.error(
                f"Error durante la importación: {e}"
            )

            log(
                f"❌ Error durante la importación: {e}"
            )

            log(
                "El archivo NO fue eliminado para poder revisarlo."
            )

        log("===================================")
        log("Proceso terminado correctamente.")
        log("===================================")