# """
# outlook.py

# Busca el último correo de Carbon Free y descarga el Excel.
# """

# import win32com.client


# class OutlookManager:

#     def __init__(self, config, logger, history):

#         self.config = config
#         self.logger = logger
#         self.history = history

#     def obtener_excel(self):

#         outlook = win32com.client.Dispatch(
#             "Outlook.Application"
#         ).GetNamespace("MAPI")

#         inbox = outlook.GetDefaultFolder(6)

#         mensajes = inbox.Items
#         mensajes.Sort("[ReceivedTime]", True)

#         asunto = self.config.asunto.lower()
#         remitente = self.config.remitente.lower()

#         for correo in mensajes:

#             try:

#                 if asunto not in correo.Subject.lower():
#                     continue

#                 if remitente not in correo.SenderEmailAddress.lower():
#                     continue

#                 entry_id = correo.EntryID

#                 if self.history.existe(entry_id):

#                     self.logger.info(
#                         "Este correo ya fue procesado."
#                     )

#                     return None

#                 self.logger.info(
#                     f"Correo encontrado: {correo.Subject}"
#                 )

#                 for adjunto in correo.Attachments:

#                     nombre = adjunto.FileName.lower()

#                     if not nombre.endswith(".xlsx"):
#                         continue

#                     destino = (
#                         self.config.ruta_descargas /
#                         adjunto.FileName
#                     )

#                     adjunto.SaveAsFile(str(destino))

#                     self.history.guardar(entry_id)

#                     self.logger.info(
#                         f"Archivo descargado: {adjunto.FileName}"
#                     )

#                     return destino

#             except Exception as e:

#                 self.logger.error(str(e))

#         return None

"""
outlook.py

En macOS toma el último Excel de data/Descargas.
En Windows descarga el Excel desde Outlook.
"""

import platform


class OutlookManager:

    def __init__(self, config, logger, history):

        self.config = config
        self.logger = logger
        self.history = history

    def obtener_excel(self):

        # ============================
        # MODO DESARROLLO (Mac)
        # ============================
        if platform.system() != "Windows":

            archivos = sorted(
                self.config.ruta_descargas.glob("*.xlsx"),
                key=lambda x: x.stat().st_mtime,
                reverse=True
            )

            if not archivos:

                self.logger.warning(
                    "No existen archivos en data/Descargas."
                )

                return None

            self.logger.info(
                f"Archivo encontrado: {archivos[0].name}"
            )

            return archivos[0]

        # ============================
        # WINDOWS
        # ============================

        import win32com.client

        outlook = win32com.client.Dispatch(
            "Outlook.Application"
        ).GetNamespace("MAPI")

        inbox = outlook.GetDefaultFolder(6)

        mensajes = inbox.Items
        mensajes.Sort("[ReceivedTime]", True)

        asunto = self.config.asunto.lower()
        remitente = self.config.remitente.lower()

        for correo in mensajes:

            try:

                if asunto not in correo.Subject.lower():
                    continue

                if remitente not in correo.SenderEmailAddress.lower():
                    continue

                entry_id = correo.EntryID

                if self.history.existe(entry_id):

                    self.logger.info(
                        "Correo ya procesado."
                    )

                    return None

                for adjunto in correo.Attachments:

                    if not adjunto.FileName.lower().endswith(".xlsx"):
                        continue

                    destino = (
                        self.config.ruta_descargas /
                        adjunto.FileName
                    )

                    adjunto.SaveAsFile(str(destino))

                    self.history.guardar(entry_id)

                    self.logger.info(
                        f"Archivo descargado: {adjunto.FileName}"
                    )

                    return destino

            except Exception as e:

                self.logger.error(str(e))

        return None