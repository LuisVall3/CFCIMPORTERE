"""
gui.py

Interfaz gráfica de Carbon Free Importer.
"""

import customtkinter as ctk
from tkinter import messagebox


class MainWindow(ctk.CTk):

    def __init__(self, app):

        super().__init__()

        self.app = app

        # ==========================
        # CONFIGURACIÓN DE VENTANA
        # ==========================

        self.title("Carbon Free Importer")
        self.geometry("850x600")
        self.minsize(750, 550)

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        # ==========================
        # ENCABEZADO
        # ==========================

        self.header = ctk.CTkFrame(
            self,
            corner_radius=0
        )

        self.header.pack(
            fill="x",
            padx=20,
            pady=(20, 10)
        )

        self.titulo = ctk.CTkLabel(
            self.header,
            text="CARBON FREE IMPORTER",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )

        self.titulo.pack(
            pady=(20, 5)
        )

        self.subtitulo = ctk.CTkLabel(
            self.header,
            text="Daily Operator Log",
            font=ctk.CTkFont(
                size=16
            )
        )

        self.subtitulo.pack(
            pady=(0, 20)
        )

        # ==========================
        # ESTADO
        # ==========================

        self.estado_frame = ctk.CTkFrame(
            self
        )

        self.estado_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        self.estado = ctk.CTkLabel(
            self.estado_frame,
            text="●  LISTO",
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        )

        self.estado.pack(
            padx=20,
            pady=15
        )

        # ==========================
        # BOTÓN
        # ==========================

        self.boton_importar = ctk.CTkButton(
            self,
            text="IMPORTAR REPORTE",
            height=50,
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            ),
            command=self.ejecutar
        )

        self.boton_importar.pack(
            padx=20,
            pady=15
        )

        # ==========================
        # REGISTRO
        # ==========================

        self.label_log = ctk.CTkLabel(
            self,
            text="Registro del proceso",
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            ),
            anchor="w"
        )

        self.label_log.pack(
            fill="x",
            padx=25,
            pady=(10, 5)
        )

        self.log = ctk.CTkTextbox(
            self,
            height=250,
            font=ctk.CTkFont(
                size=13
            )
        )

        self.log.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

        self.escribir(
            "✓ Carbon Free Importer iniciado."
        )

        self.escribir(
            "✓ Sistema listo para importar."
        )

    # ==========================
    # ESCRIBIR EN LOG
    # ==========================

    def escribir(self, texto):

        self.log.insert(
            "end",
            texto + "\n"
        )

        self.log.see("end")

        self.update_idletasks()

    # ==========================
    # EJECUTAR IMPORTACIÓN
    # ==========================

    def ejecutar(self):

        self.boton_importar.configure(
            state="disabled"
        )

        self.estado.configure(
            text="●  PROCESANDO..."
        )

        self.log.delete(
            "1.0",
            "end"
        )

        self.escribir(
            "Iniciando proceso..."
        )

        try:

            self.app.run(
                self.escribir
            )

            self.estado.configure(
                text="●  PROCESO FINALIZADO"
            )

            self.escribir(
                "✓ Proceso terminado correctamente."
            )

            messagebox.showinfo(
                "Carbon Free Importer",
                "El proceso terminó correctamente."
            )

        except Exception as e:

            self.estado.configure(
                text="●  ERROR"
            )

            self.escribir(
                f"❌ Error: {e}"
            )

            messagebox.showerror(
                "Carbon Free Importer",
                str(e)
            )

        finally:

            self.boton_importar.configure(
                state="normal"
            )