"""
history.py

Evita procesar dos veces el mismo correo.
"""

from pathlib import Path


class HistoryManager:

    def __init__(self, archivo: Path):

        self.archivo = archivo

        self.archivo.parent.mkdir(parents=True, exist_ok=True)
        self.archivo.touch(exist_ok=True)

    def existe(self, entry_id: str):

        with open(self.archivo, "r", encoding="utf-8") as f:
            return entry_id in {line.strip() for line in f}

    def guardar(self, entry_id: str):

        with open(self.archivo, "a", encoding="utf-8") as f:
            f.write(entry_id + "\n")