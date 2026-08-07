"""
excel.py

Manejo del Excel Maestro.
"""

from pathlib import Path

import pandas as pd
from openpyxl import Workbook
from openpyxl import load_workbook


class ExcelManager:

    def __init__(self, archivo_maestro: Path):

        self.archivo_maestro = archivo_maestro

    def existe(self):

        return self.archivo_maestro.exists()

    def crear_maestro(self, dataframe: pd.DataFrame):

        dataframe.to_excel(
            self.archivo_maestro,
            index=False
        )

    def agregar_registros(self, archivo_nuevo: Path):

        # Leer archivo recibido
        df = pd.read_excel(archivo_nuevo)

        # Si no existe el maestro, lo crea
        if not self.existe():

            self.crear_maestro(df)

            return len(df)

        # Abrir el Excel maestro
        wb = load_workbook(self.archivo_maestro)

        # Trabajar siempre sobre la primera hoja
        ws = wb[wb.sheetnames[0]]

        # Agregar filas al final
        for fila in df.itertuples(index=False):

            ws.append(list(fila))

        wb.save(self.archivo_maestro)

        return len(df)