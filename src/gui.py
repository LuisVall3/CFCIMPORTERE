import customtkinter as ctk
from tkinter import messagebox


class MainWindow(ctk.CTk):

    def __init__(self, app):

        super().__init__()

        self.app = app

        self.title("Carbon Free Importer")
        self.geometry("700x500")

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.label = ctk.CTkLabel(
            self,
            text="Carbon Free Importer",
            font=("Arial", 24, "bold")
        )

        self.label.pack(pady=20)

        self.btn = ctk.CTkButton(
            self,
            text="Importar reporte",
            command=self.ejecutar
        )

        self.btn.pack(pady=10)

        self.log = ctk.CTkTextbox(
            self,
            width=650,
            height=300
        )

        self.log.pack(padx=20, pady=20)

    def escribir(self, texto):

        self.log.insert("end", texto + "\n")

        self.log.see("end")

    def ejecutar(self):

        self.btn.configure(state="disabled")

        try:

            self.escribir("Iniciando proceso...")

            self.app.run(self.escribir)

            self.escribir("Proceso finalizado.")

            messagebox.showinfo(
                "Carbon Free",
                "Proceso terminado correctamente."
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

        self.btn.configure(state="normal")