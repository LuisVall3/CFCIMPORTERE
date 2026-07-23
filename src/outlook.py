"""
outlook.py

Gestión de Outlook.
"""

from pathlib import Path
import platform


class OutlookManager:

    def __init__(self, config, logger):

        self.config = config
        self.logger = logger

    def conectar(self):

        if platform.system() != "Windows":

            self.logger.warning(
                "Outlook solamente está disponible en Windows."
            )

            return False

        try:

            import win32com.client

            self.outlook = (
                win32com.client.Dispatch(
                    "Outlook.Application"
                )
                .GetNamespace("MAPI")
            )

            self.logger.info(
                "Conexión con Outlook establecida."
            )

            return True

        except Exception as e:

            self.logger.error(str(e))

            return False