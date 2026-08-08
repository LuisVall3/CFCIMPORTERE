"""
excel.py

Manejo del Excel Maestro.
"""

from pathlib import Path
import pandas as pd


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
        df_maestro = pd.read_excel(self.archivo_maestro)

        # Eliminar registros del nuevo archivo que ya existen en el Maestro
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

        # Concatenar el maestro existente con las filas nuevas
        # ignore_index=True reindexa todo para asegurar continuidad limpia sin huecos
        df_actualizado = pd.concat([df_maestro, df_nuevos], ignore_index=True)

        # Sobrescribir la planilla Maestro ordenada y sin espacios vacíos
        df_actualizado.to_excel(
            self.archivo_maestro,
            index=False
        )

        return len(df_nuevos)