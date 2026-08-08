from pathlib import Path


class OutlookManager:

    def __init__(self, config, logger, history=None):
        self.config = config
        self.logger = logger
        self.history = history

    def obtener_excel(self, ruta_archivo=None):
        """
        Si se pasa `ruta_archivo`, usa ese archivo directamente.
        Si no, busca el Excel más reciente en Descargas.
        """
        if ruta_archivo:
            archivo = Path(ruta_archivo)
            if archivo.exists():
                self.logger.info(f"Excel seleccionado manualmente: {archivo.name}")
                return archivo
            else:
                self.logger.error(f"El archivo especificado no existe: {ruta_archivo}")
                return None

        # Comportamiento por defecto (si no se envía ruta)
        archivos = sorted(
            self.config.ruta_descargas.glob("*.xlsx"),
            key=lambda archivo: archivo.stat().st_mtime,
            reverse=True
        )

        if not archivos:
            self.logger.warning("No existen archivos Excel en la carpeta Descargas.")
            return None

        archivo = archivos[0]
        self.logger.info(f"Excel encontrado: {archivo.name}")
        return archivo