"""
excel.py

Manejo del Excel Maestro.
"""

from pathlib import Path

import pandas as pd
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

        # Leer archivo nuevo
        df_nuevo = pd.read_excel(archivo_nuevo)

        # Si el Maestro no existe, lo crea completo
        if not self.existe():

            self.crear_maestro(df_nuevo)

            return len(df_nuevo)

        # Leer Maestro existente
        df_maestro = pd.read_excel(
            self.archivo_maestro
        )

        # Eliminar registros que ya existen
        df_comparacion = df_nuevo.merge(
            df_maestro.drop_duplicates(),
            how="left",
            indicator=True
        )

        df_nuevos = df_comparacion[
            df_comparacion["_merge"] == "left_only"
        ].drop(columns=["_merge"])

        # Si no hay registros nuevos
        if df_nuevos.empty:

            return 0

        # Abrir Excel Maestro
        wb = load_workbook(self.archivo_maestro)

        ws = wb[wb.sheetnames[0]]

        # Agregar solamente registros nuevos
        for fila in df_nuevos.itertuples(index=False):

            ws.append(list(fila))

        wb.save(self.archivo_maestro)

        return len(df_nuevos)