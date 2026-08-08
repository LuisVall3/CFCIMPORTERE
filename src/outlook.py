"""
outlook.py

Busca el Excel más reciente en la carpeta Descargas.
No utiliza Outlook.
"""

from pathlib import Path


class OutlookManager:

    def __init__(self, config, logger, history=None):

        self.config = config
        self.logger = logger
        self.history = history

    def obtener_excel(self):

        archivos = sorted(
            self.config.ruta_descargas.glob("*.xlsx"),
            key=lambda archivo: archivo.stat().st_mtime,
            reverse=True
        )

        if not archivos:

            self.logger.warning(
                "No existen archivos Excel en la carpeta Descargas."
            )

            return None

        archivo = archivos[0]

        self.logger.info(
            f"Excel encontrado: {archivo.name}"
        )

        return archivo