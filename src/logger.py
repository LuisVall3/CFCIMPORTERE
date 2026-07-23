"""
logger.py

Sistema de registro de eventos de Carbon Free Importer.
"""

import logging
from pathlib import Path
from datetime import datetime


class LoggerManager:

    def __init__(self, carpeta_logs: Path):

        self.carpeta_logs = carpeta_logs

        self.carpeta_logs.mkdir(parents=True, exist_ok=True)

        nombre_log = datetime.now().strftime("%Y-%m-%d") + ".log"

        self.log_file = self.carpeta_logs / nombre_log

        self.logger = logging.getLogger("CarbonFreeImporter")

        self.logger.setLevel(logging.INFO)

        # Evita duplicar handlers si se instancia más de una vez
        if not self.logger.handlers:

            formatter = logging.Formatter(
                "%(asctime)s | %(levelname)s | %(message)s",
                "%d/%m/%Y %H:%M:%S"
            )

            file_handler = logging.FileHandler(
                self.log_file,
                encoding="utf-8"
            )

            file_handler.setFormatter(formatter)

            console_handler = logging.StreamHandler()

            console_handler.setFormatter(formatter)

            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

    def info(self, mensaje: str):
        self.logger.info(mensaje)

    def warning(self, mensaje: str):
        self.logger.warning(mensaje)

    def error(self, mensaje: str):
        self.logger.error(mensaje)