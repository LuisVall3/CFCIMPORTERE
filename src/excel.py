"""
excel.py - NovaSource Power Services
Módulo de procesamiento y manipulación del Excel Maestro para Carbon Free Importer.
"""

import os
from pathlib import Path
import pandas as pd


class ExcelManager:

    def __init__(self, ruta_maestro: str | Path):
        self.ruta_maestro = Path(ruta_maestro)

    def existe(self) -> bool:
        """Verifica la existencia del archivo Excel Maestro (requerido por app.py)."""
        return self.ruta_maestro.exists()

    def _cargar_maestro(self) -> pd.DataFrame:
        """Carga el contenido actual de la última hoja del Excel Maestro."""
        if not self.existe():
            return pd.DataFrame()

        try:
            excel_file = pd.ExcelFile(self.ruta_maestro)
            if not excel_file.sheet_names:
                return pd.DataFrame()
            
            ultima_hoja = excel_file.sheet_names[-1]
            return pd.read_excel(excel_file, sheet_name=ultima_hoja)
        except Exception as e:
            raise RuntimeError(f"Error al leer el archivo Maestro: {str(e)}")

    def agregar_registros(self, ruta_nuevo_archivo: str | Path) -> int:
        """
        Lee el nuevo reporte diario, lo compara con el Maestro para evitar duplicados
        y anexa únicamente los nuevos registros sin romper por inconsistencias de tipos.
        """
        ruta_nuevo = Path(ruta_nuevo_archivo)

        if not ruta_nuevo.exists():
            raise FileNotFoundError(f"No se encontró el archivo de origen: {ruta_nuevo}")

        # 1. Lectura de datasets
        df_nuevo = pd.read_excel(ruta_nuevo)
        df_maestro = self._cargar_maestro()

        if df_nuevo.empty:
            return 0

        # Si el maestro no existe aún, guardamos el primer bloque de datos
        if df_maestro.empty:
            self._guardar_en_maestro(df_nuevo)
            return len(df_nuevo)

        # 2. HOMOGENEIZACIÓN DE TIPOS (Evita errores float64 vs str en el merge)
        df_nuevo_str = df_nuevo.astype(str).apply(lambda x: x.str.strip())
        df_maestro_str = df_maestro.astype(str).apply(lambda x: x.str.strip())

        # 3. Comparación vía merge para detectar registros nuevos
        df_comparacion = df_nuevo_str.merge(
            df_maestro_str.drop_duplicates(),
            how="left",
            indicator=True
        )

        # 4. Inserción de registros únicos respetando los tipos originales de df_nuevo
        mask_nuevos = df_comparacion["_merge"] == "left_only"
        registros_nuevos = df_nuevo[mask_nuevos].copy()

        total_nuevos = len(registros_nuevos)

        if total_nuevos > 0:
            df_final = pd.concat([df_maestro, registros_nuevos], ignore_index=True)
            self._guardar_en_maestro(df_final)

        return total_nuevos

    def _guardar_en_maestro(self, df: pd.DataFrame):
        """Escribe los datos actualizados en la hoja principal del Excel Maestro."""
        with pd.ExcelWriter(self.ruta_maestro, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name="Master", index=False)