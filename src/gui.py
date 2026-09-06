"""
gui.py - NovaSource Power Services
Interfaz Gráfica Profesional tipo Dashboard Enterprise para Carbon Free Importer.
Soporte completo para modo Claro / Oscuro, gestión de configuración de rutas (Maestro/Logs),
rediseño visual de tarjetas y registro en logs.
"""

import os
import sys
import threading
import traceback
from datetime import datetime
from pathlib import Path
import pandas as pd
import customtkinter as ctk
from tkinter import messagebox, filedialog, ttk
from PIL import Image, ImageTk

# Configuración de apariencia global por defecto
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# =========================================================
# PALETA DE COLORES ENTERPRISE (Soporte Dual Light/Dark)
# =========================================================
PALETTE = {
    "Dark": {
        "BG": "#0F172A",           # Slate 900
        "CARD_BG": "#1E293B",      # Slate 800
        "CARD_BORDER": "#334155",  # Slate 700
        "TERMINAL_BG": "#090D16",  # Deep Dark Blue
        "TERM_HEADER": "#1E293B",  # Terminal bar
        "TEXT_MAIN": "#F8FAFC",    # Slate 50
        "TEXT_MUTED": "#94A3B8",   # Slate 400
        "LOG_TEXT": "#A7F3D0",     # Emerald light
        "TREE_BG": "#0F172A",
        "TREE_FG": "#F8FAFC",
        "TREE_HEAD": "#1E293B",
    },
    "Light": {
        "BG": "#F8FAFC",           # Slate 50
        "CARD_BG": "#FFFFFF",      # Pure White
        "CARD_BORDER": "#CBD5E1",  # Slate 300
        "TERMINAL_BG": "#1E293B",  # Slate 800 para contraste de terminal incluso en light
        "TERM_HEADER": "#334155",  # Slate 700
        "TEXT_MAIN": "#0F172A",    # Slate 900
        "TEXT_MUTED": "#64748B",   # Slate 500
        "LOG_TEXT": "#38BDF8",     # Sky light
        "TREE_BG": "#FFFFFF",
        "TREE_FG": "#0F172A",
        "TREE_HEAD": "#E2E8F0",
    }
}

ACCENT_GREEN = "#10B981"    # Emerald 500
ACCENT_BLUE = "#0284C7"     # Sky 600
COLOR_ERROR = "#EF4444"      # Red 500
COLOR_WARNING = "#F59E0B"    # Amber 500


def obtener_ruta_recurso(ruta_relativa: str) -> Path:
    if hasattr(sys, '_MEIPASS'):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).resolve().parent.parent
    return base_path / ruta_relativa


def aplicar_icono_ventana(window):
    ruta_ico = obtener_ruta_recurso("assets/favicon.ico")
    ruta_png = obtener_ruta_recurso("assets/novasource_logo.png")

    if sys.platform.startswith("win") and ruta_ico.exists():
        try:
            window.iconbitmap(str(ruta_ico))
        except Exception:
            pass

    if ruta_png.exists():
        try:
            img_pil = Image.open(ruta_png)
            photo = ImageTk.PhotoImage(img_pil)
            window.tk.call('wm', 'iconphoto', window._w, photo)
            window._icon_photo = photo
        except Exception as e:
            print(f"Error cargando icono PNG: {e}")


class MainWindow(ctk.CTk):

    def __init__(self, app):
        super().__init__()

        self.app = app
        self.modo_actual = "Dark"

        # Configuración principal
        self.title("NovaSource Power | Carbon Free Importer")
        self.geometry("1000x720")
        self.minsize(920, 650)

        aplicar_icono_ventana(self)
        self._crear_interfaz()
        self._aplicar_colores_tema()

    def _crear_interfaz(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)  # La consola se expande

        # ==========================
        # 1. NAVBAR / HEADER DE MARCA
        # ==========================
        self.header_frame = ctk.CTkFrame(self, corner_radius=16, border_width=1)
        self.header_frame.grid(row=0, column=0, padx=20, pady=(15, 10), sticky="ew")
        self.header_frame.grid_columnconfigure(0, weight=1)

        # Contenedor del Logo
        self.brand_container = ctk.CTkFrame(self.header_frame, fg_color="transparent", corner_radius=16)
        self.brand_container.grid(row=0, column=0, padx=16, pady=12, sticky="w")

        self.logo_box = ctk.CTkFrame(self.brand_container, width=50, height=50, fg_color="transparent")
        self.logo_box.pack(side="left", padx=(0, 15))
        self.logo_box.pack_propagate(False)

        ruta_logo = obtener_ruta_recurso("assets/novasource_logo.png")
        if ruta_logo.exists():
            img_logo_pil = Image.open(ruta_logo)
            logo_ctk = ctk.CTkImage(light_image=img_logo_pil, dark_image=img_logo_pil, size=(38, 38))
            self.lbl_logo_img = ctk.CTkLabel(self.logo_box, image=logo_ctk, text="")
            self.lbl_logo_img.place(relx=0.5, rely=0.5, anchor="center")

        self.title_box = ctk.CTkFrame(self.brand_container, fg_color="transparent")
        self.title_box.pack(side="left")

        self.brand_label = ctk.CTkLabel(
            self.title_box,
            text="NOVASOURCE POWER SERVICES",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=ACCENT_GREEN
        )
        self.brand_label.pack(anchor="w")

        self.titulo = ctk.CTkLabel(
            self.title_box,
            text="Carbon Free Importer",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.titulo.pack(anchor="w")

        # Acciones Superiores
        self.header_actions = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.header_actions.grid(row=0, column=1, padx=20, pady=12, sticky="e")

        self.btn_ver_maestro = ctk.CTkButton(
            self.header_actions,
            text="🔍 Ver Maestro",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#334155",
            hover_color="#475569",
            height=36,
            corner_radius=10,
            command=self._ver_previsualizacion_maestro
        )
        self.btn_ver_maestro.pack(side="left", padx=(0, 10))

        self.btn_config = ctk.CTkButton(
            self.header_actions,
            text="⚙️",
            width=38,
            height=36,
            font=ctk.CTkFont(size=16),
            fg_color="#334155",
            hover_color="#475569",
            corner_radius=10,
            command=self._abrir_configuracion
        )
        self.btn_config.pack(side="left", padx=(0, 15))

        self.switch_tema = ctk.CTkSwitch(
            self.header_actions,
            text="🌙 Oscuro",
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self._alternar_tema,
            onvalue="Dark",
            offvalue="Light"
        )
        self.switch_tema.select()
        self.switch_tema.pack(side="right")

        # ==========================
        # 2. PANEL DE CONTROL & KPIS
        # ==========================
        self.dashboard_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.dashboard_frame.grid(row=1, column=0, padx=20, pady=5, sticky="ew")
        self.dashboard_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # Card 1: Estado del Sistema
        self.card_status_frame, self.lbl_status_val, self.lbl_status_sub = self._crear_kpi_card(
            self.dashboard_frame,
            col=0,
            titulo="ESTADO DEL SISTEMA",
            valor="● SISTEMA LISTO",
            sub="Esperando archivo",
            color_valor=ACCENT_GREEN
        )

        # Card 2: Última Importación
        self.card_last_frame, self.lbl_last_val, self.lbl_last_sub = self._crear_kpi_card(
            self.dashboard_frame,
            col=1,
            titulo="ÚLTIMA EJECUCIÓN",
            valor="Sin registros hoy",
            sub="--:--:--",
            color_valor=ACCENT_BLUE
        )

        # Card 3: Botón Principal de Importación
        self.card_action = ctk.CTkFrame(self.dashboard_frame, corner_radius=12, border_width=1)
        self.card_action.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")

        self.boton_importar = ctk.CTkButton(
            self.card_action,
            text="⚡ SELECCIONAR Y PROCESAR",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=ACCENT_GREEN,
            hover_color="#059669",
            text_color="#022C22",
            height=42,
            corner_radius=10,
            command=self.iniciar_importacion_thread
        )
        self.boton_importar.pack(expand=True, fill="both", padx=15, pady=15)

        # ==========================
        # 3. TERMINAL DE CONSOLA
        # ==========================
        self.terminal_container = ctk.CTkFrame(self, corner_radius=14, border_width=1)
        self.terminal_container.grid(row=2, column=0, padx=20, pady=(10, 15), sticky="nsew")
        self.terminal_container.grid_rowconfigure(1, weight=1)
        self.terminal_container.grid_columnconfigure(0, weight=1)

        self.term_header = ctk.CTkFrame(self.terminal_container, height=34, corner_radius=0)
        self.term_header.grid(row=0, column=0, sticky="ew")

        dots_frame = ctk.CTkFrame(self.term_header, fg_color="transparent")
        dots_frame.pack(side="left", padx=12)

        for color in ["#EF4444", "#F59E0B", "#10B981"]:
            dot = ctk.CTkFrame(dots_frame, width=10, height=10, corner_radius=5, fg_color=color)
            dot.pack(side="left", padx=2)

        self.lbl_term_title = ctk.CTkLabel(
            self.term_header,
            text="Console Output - Live Log Stream",
            font=ctk.CTkFont(family="Consolas", size=11, weight="bold")
        )
        self.lbl_term_title.pack(side="left", padx=10)

        self.btn_clear_log = ctk.CTkButton(
            self.term_header,
            text="Limpiar",
            width=60,
            height=22,
            font=ctk.CTkFont(size=10, weight="bold"),
            fg_color="#334155",
            hover_color="#475569",
            corner_radius=6,
            command=self._limpiar_consola
        )
        self.btn_clear_log.pack(side="right", padx=10)

        self.log = ctk.CTkTextbox(
            self.terminal_container,
            font=ctk.CTkFont(family="Consolas", size=12),
            fg_color="transparent",
            corner_radius=0,
            state="disabled"
        )
        self.log.grid(row=1, column=0, padx=12, pady=8, sticky="nsew")

        # ==========================
        # 4. BARRA DE ESTADO (FOOTER)
        # ==========================
        self.statusbar = ctk.CTkFrame(self, height=25, fg_color="transparent")
        self.statusbar.grid(row=3, column=0, padx=20, pady=(0, 8), sticky="ew")

        self.lbl_footer_status = ctk.CTkLabel(
            self.statusbar,
            text="Ready | NovaSource Engine v1.2",
            font=ctk.CTkFont(size=10)
        )
        self.lbl_footer_status.pack(side="left")

        self.escribir("[SYSTEM] Inicializando entorno NovaSource Carbon Free Importer...")
        self.escribir("[SYSTEM] Listo para procesar registros diarios.")

    def _crear_kpi_card(self, parent, col, titulo, valor, sub, color_valor):
        card = ctk.CTkFrame(parent, corner_radius=12, border_width=1)
        card.grid(row=0, column=col, padx=5, pady=5, sticky="nsew")

        lbl_title = ctk.CTkLabel(card, text=titulo, font=ctk.CTkFont(size=10, weight="bold"))
        lbl_title.pack(anchor="w", padx=12, pady=(10, 0))

        lbl_val = ctk.CTkLabel(card, text=valor, font=ctk.CTkFont(size=14, weight="bold"), text_color=color_valor)
        lbl_val.pack(anchor="w", padx=12, pady=(2, 0))

        lbl_sub = ctk.CTkLabel(card, text=sub, font=ctk.CTkFont(size=10))
        lbl_sub.pack(anchor="w", padx=12, pady=(0, 8))

        return card, lbl_val, lbl_sub

    def _aplicar_colores_tema(self):
        colors = PALETTE[self.modo_actual]
        self.configure(fg_color=colors["BG"])

        self.header_frame.configure(fg_color=colors["CARD_BG"], border_color=colors["CARD_BORDER"])
        self.titulo.configure(text_color=colors["TEXT_MAIN"])

        for card in [self.card_status_frame, self.card_last_frame, self.card_action]:
            card.configure(fg_color=colors["CARD_BG"], border_color=colors["CARD_BORDER"])

        self.terminal_container.configure(fg_color=colors["TERMINAL_BG"], border_color=colors["CARD_BORDER"])
        self.term_header.configure(fg_color=colors["TERM_HEADER"])
        self.lbl_term_title.configure(text_color=colors["TEXT_MUTED"])
        self.log.configure(text_color=colors["LOG_TEXT"])

        self.lbl_footer_status.configure(text_color=colors["TEXT_MUTED"])

        if self.modo_actual == "Dark":
            self.switch_tema.configure(text="🌙 Oscuro", text_color=colors["TEXT_MAIN"])
        else:
            self.switch_tema.configure(text="☀️ Claro", text_color=colors["TEXT_MAIN"])

    def _alternar_tema(self):
        self.modo_actual = self.switch_tema.get()
        ctk.set_appearance_mode(self.modo_actual)
        self._aplicar_colores_tema()

    def _limpiar_consola(self):
        self.log.configure(state="normal")
        self.log.delete("1.0", "end")
        self.log.configure(state="disabled")

    def escribir(self, texto: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log.configure(state="normal")
        self.log.insert("end", f"[{timestamp}] {texto}\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    def _abrir_configuracion(self):
        config_mgr = getattr(self.app, "config_manager", None) or getattr(self.app, "config", None)
        ruta_maestro_previa = self._obtener_ruta_maestro()

        dialog = SetupDialog(config_mgr, parent_window=self)
        self.wait_window(dialog)

        ruta_maestro_nueva = self._obtener_ruta_maestro()
        if ruta_maestro_nueva and ruta_maestro_nueva != ruta_maestro_previa:
            self.escribir(f"[CONFIG] Archivo Maestro actualizado: {ruta_maestro_nueva}")
            messagebox.showinfo("Configuración", f"Ruta del Excel Maestro actualizada con éxito:\n\n{ruta_maestro_nueva}", parent=self)

    def _obtener_ruta_maestro(self):
        if hasattr(self.app, "config"):
            cfg = self.app.config
            if hasattr(cfg, "ruta_maestro"):
                return cfg.ruta_maestro
            elif isinstance(cfg, dict):
                return cfg.get("rutas", {}).get("maestro") or cfg.get("ruta_maestro")
        if hasattr(self.app, "config_manager"):
            cm = self.app.config_manager
            if hasattr(cm, "ruta_maestro"):
                return cm.ruta_maestro
            elif hasattr(cm, "config") and isinstance(cm.config, dict):
                return cm.config.get("rutas", {}).get("maestro")
        return None

    def _ver_previsualizacion_maestro(self):
        ruta_maestro = self._obtener_ruta_maestro()

        if not ruta_maestro or not os.path.exists(str(ruta_maestro)):
            messagebox.showwarning("Atención", "No se encontró la ruta del Excel Maestro o el archivo no existe. Utiliza el botón ⚙️ para configurarlo.", parent=self)
            return

        try:
            with pd.ExcelFile(ruta_maestro) as excel_file:
                hojas = excel_file.sheet_names

                if not hojas:
                    messagebox.showinfo("Información", "El archivo Excel Maestro está vacío.", parent=self)
                    return

                nombre_hoja = "Master" if "Master" in hojas else hojas[-1]
                df_raw = pd.read_excel(excel_file, sheet_name=nombre_hoja, header=None, nrows=35)

            df = df_raw.copy()
            df.columns = [f"Columna {i+1}" if "Unnamed:" in str(c) or str(c).strip() == "" else str(c) for i, c in enumerate(df.columns)]

            top = ctk.CTkToplevel(self)
            top.title(f"Vista Previa Maestro - [{nombre_hoja}]")
            top.geometry("920x520")
            top.transient(self)
            top.grab_set()

            aplicar_icono_ventana(top)

            colors = PALETTE[self.modo_actual]

            info_frame = ctk.CTkFrame(top, corner_radius=12, fg_color=colors["CARD_BG"])
            info_frame.pack(fill="x", padx=20, pady=(15, 12))

            lbl_hoja = ctk.CTkLabel(info_frame, text=f"📊 HOJA MAESTRA: {nombre_hoja}", font=ctk.CTkFont(size=13, weight="bold"), text_color=ACCENT_GREEN)
            lbl_hoja.pack(side="left", padx=16, pady=10)

            lbl_archivo = ctk.CTkLabel(info_frame, text=f"📁 {os.path.basename(str(ruta_maestro))}", font=ctk.CTkFont(size=11), text_color=colors["TEXT_MUTED"])
            lbl_archivo.pack(side="right", padx=16, pady=10)

            frame_tabla = ctk.CTkFrame(top, corner_radius=12, fg_color=colors["CARD_BG"])
            frame_tabla.pack(fill="both", expand=True, padx=20, pady=(0, 20))

            style = ttk.Style()
            style.theme_use("clam")
            font_family = 'Consolas' if sys.platform.startswith('win') else 'Calibri'

            style.configure("Custom.Treeview", background=colors["TREE_BG"], fieldbackground=colors["TREE_BG"], foreground=colors["TREE_FG"], rowheight=26, borderwidth=0, font=(font_family, 10))
            style.configure("Custom.Treeview.Heading", background=colors["TREE_HEAD"], foreground=ACCENT_GREEN, relief="flat", font=(font_family, 10, 'bold'))

            cols = list(df.columns)
            tree = ttk.Treeview(frame_tabla, style="Custom.Treeview", columns=cols, show='headings', selectmode='browse')

            scroll_y = ttk.Scrollbar(frame_tabla, orient="vertical", command=tree.yview)
            scroll_x = ttk.Scrollbar(frame_tabla, orient="horizontal", command=tree.xview)
            tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

            scroll_y.pack(side="right", fill="y")
            scroll_x.pack(side="bottom", fill="x")
            tree.pack(fill="both", expand=True, padx=4, pady=4)

            for c in cols:
                tree.heading(c, text=str(c))
                tree.column(c, width=140, anchor="center")

            for idx, row in df.iterrows():
                valores = [str(val) if (pd.notna(val) and str(val) != "nan") else "" for val in row]
                tree.insert("", "end", values=valores)

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la vista previa:\n\n{str(e)}", parent=self)

    def iniciar_importacion_thread(self):
        initial_dir = getattr(self.app.config, "ruta_descargas", None) if hasattr(self.app, "config") else None

        archivo_seleccionado = filedialog.askopenfilename(
            parent=self,
            title="Seleccionar reporte diario para procesar",
            initialdir=str(initial_dir) if initial_dir else None,
            filetypes=[("Archivos Excel", "*.xlsx"), ("Todos los archivos", "*.*")]
        )

        if not archivo_seleccionado:
            self.escribir("[CANCELADO] No se seleccionó ningún archivo.")
            return

        self.boton_importar.configure(state="disabled", fg_color="#334155")
        self.lbl_status_val.configure(text="● PROCESANDO...", text_color=COLOR_WARNING)
        self.lbl_status_sub.configure(text=os.path.basename(archivo_seleccionado))

        self.escribir(f"[RUN] Archivo seleccionado: {archivo_seleccionado}")

        thread = threading.Thread(
            target=self._ejecutar_proceso,
            args=(archivo_seleccionado,),
            daemon=True
        )
        thread.start()

    def _ejecutar_proceso(self, ruta_archivo):
        try:
            def log_seguro(mensaje):
                self.after(0, lambda: self.escribir(mensaje))

            self.app.run(log_seguro, ruta_archivo=ruta_archivo)
            self.after(0, lambda: self._al_finalizar_exito(ruta_archivo))

        except Exception as e:
            error_detallado = traceback.format_exc()
            self.after(0, lambda err=error_detallado: self._al_finalizar_error(err))

    def _al_finalizar_exito(self, ruta_archivo):
        hora_actual = datetime.now().strftime("%H:%M:%S")

        self.lbl_status_val.configure(text="● COMPLETADO", text_color=ACCENT_GREEN)
        self.lbl_status_sub.configure(text="Listo para nueva tarea")

        self.lbl_last_val.configure(text="Éxito")
        self.lbl_last_sub.configure(text=f"Procesado a las {hora_actual}")

        self.escribir("[SUCCESS] Operación finalizada e integrada en Excel Maestro.")
        self.boton_importar.configure(state="normal", fg_color=ACCENT_GREEN)

        messagebox.showinfo("NovaSource Power", "El reporte ha sido importado y procesado exitosamente.", parent=self)

    def _al_finalizar_error(self, error_msg: str):
        self.lbl_status_val.configure(text="● ERROR DE EJECUCIÓN", text_color=COLOR_ERROR)
        self.lbl_status_sub.configure(text="Revisar logs de consola")

        self.escribir(f"[ERROR] Ocurrió una falla crítica:\n{error_msg}")
        self.boton_importar.configure(state="normal", fg_color=ACCENT_GREEN)

        messagebox.showerror("Error", f"Ocurrió un error en el procesamiento:\n\n{error_msg}", parent=self)


# ==========================================
# DIÁLOGO DE CONFIGURACIÓN INICIAL / RUTAS
# ==========================================
class SetupDialog(ctk.CTkToplevel):

    def __init__(self, config_manager, parent_window=None):
        # Evita la creación de la ventana Tk raíz transparente
        if parent_window is None:
            super().__init__()
        else:
            super().__init__(parent_window)

        self.config_manager = config_manager
        self.parent_window = parent_window

        self.title("NovaSource Power | Configuración de Rutas")
        self.geometry("580x420")
        self.resizable(False, False)

        # Configuración estricta de jerarquía visual y foco
        if parent_window:
            self.transient(parent_window)
            self.lift()
            self.grab_set()

        aplicar_icono_ventana(self)

        # Cargar rutas previas
        rutas = {}
        if hasattr(self.config_manager, "config"):
            cfg = self.config_manager.config
            if isinstance(cfg, dict):
                rutas = cfg.get("rutas", {})
        
        self.ruta_maestro = ctk.StringVar(
            value=getattr(self.config_manager, "ruta_maestro", rutas.get("maestro", "")) or ""
        )
        self.ruta_logs = ctk.StringVar(
            value=getattr(self.config_manager, "ruta_logs", rutas.get("logs", "")) or ""
        )

        self._crear_widgets()

    def _crear_widgets(self):
        # Header / Título del diálogo
        self.header_frame = ctk.CTkFrame(self, corner_radius=12, border_width=1)
        self.header_frame.pack(fill="x", padx=20, pady=(20, 15))

        lbl_titulo = ctk.CTkLabel(
            self.header_frame,
            text="⚙️ CONFIGURACIÓN DE RUTAS DEL SISTEMA",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=ACCENT_GREEN
        )
        lbl_titulo.pack(anchor="w", padx=15, pady=(12, 2))

        lbl_sub = ctk.CTkLabel(
            self.header_frame,
            text="Define las ubicaciones predeterminadas para los archivos y registros.",
            font=ctk.CTkFont(size=11)
        )
        lbl_sub.pack(anchor="w", padx=15, pady=(0, 12))

        # --- CAMPO: ARCHIVO MAESTRO ---
        lbl_m = ctk.CTkLabel(
            self,
            text="Archivo Excel Maestro (.xlsx):",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        lbl_m.pack(anchor="w", padx=25, pady=(5, 2))

        frame_m = ctk.CTkFrame(self, fg_color="transparent")
        frame_m.pack(fill="x", padx=25, pady=(0, 15))

        entry_m = ctk.CTkEntry(
            frame_m,
            textvariable=self.ruta_maestro,
            placeholder_text="Ruta del Excel Maestro...",
            height=36
        )
        entry_m.pack(side="left", fill="x", expand=True, padx=(0, 10))

        btn_m = ctk.CTkButton(
            frame_m,
            text="Explorar",
            width=90,
            height=36,
            fg_color="#334155",
            hover_color="#475569",
            corner_radius=8,
            command=self._seleccionar_maestro
        )
        btn_m.pack(side="right")

        # --- CAMPO: CARPETA LOGS ---
        lbl_l = ctk.CTkLabel(
            self,
            text="Carpeta de Registros (Logs):",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        lbl_l.pack(anchor="w", padx=25, pady=(5, 2))

        frame_l = ctk.CTkFrame(self, fg_color="transparent")
        frame_l.pack(fill="x", padx=25, pady=(0, 20))

        entry_l = ctk.CTkEntry(
            frame_l,
            textvariable=self.ruta_logs,
            placeholder_text="Carpeta donde guardar logs...",
            height=36
        )
        entry_l.pack(side="left", fill="x", expand=True, padx=(0, 10))

        btn_l = ctk.CTkButton(
            frame_l,
            text="Explorar",
            width=90,
            height=36,
            fg_color="#334155",
            hover_color="#475569",
            corner_radius=8,
            command=self._seleccionar_logs
        )
        btn_l.pack(side="right")

        # --- BOTÓN DE ACCIÓN FINAL ---
        btn_guardar = ctk.CTkButton(
            self,
            text="GUARDAR Y CONTINUAR ➔",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=ACCENT_GREEN,
            hover_color="#059669",
            text_color="#022C22",
            height=42,
            corner_radius=10,
            command=self._guardar
        )
        btn_guardar.pack(fill="x", padx=25, pady=10)

    def _seleccionar_maestro(self):
        file_path = filedialog.askopenfilename(
            parent=self,
            title="Seleccionar Excel Maestro",
            filetypes=[("Archivos Excel", "*.xlsx")]
        )
        if file_path:
            self.ruta_maestro.set(file_path)

    def _seleccionar_logs(self):
        dir_path = filedialog.askdirectory(
            parent=self,
            title="Seleccionar Carpeta de Logs"
        )
        if dir_path:
            self.ruta_logs.set(dir_path)

    def _guardar(self):
        maestro = self.ruta_maestro.get().strip()
        logs = self.ruta_logs.get().strip()

        if not maestro or not logs:
            messagebox.showwarning("Atención", "Por favor define ambas rutas antes de continuar.", parent=self)
            return

        # Guardar la configuración según la firma disponible
        if hasattr(self.config_manager, "guardar_rutas"):
            self.config_manager.guardar_rutas(maestro, logs)
        elif hasattr(self.config_manager, "guardar_config"):
            try:
                self.config_manager.guardar_config(maestro, logs)
            except TypeError:
                self.config_manager.guardar_config(maestro)

        # Actualizar atributos directos
        if hasattr(self.config_manager, "ruta_maestro"):
            self.config_manager.ruta_maestro = maestro
        if hasattr(self.config_manager, "ruta_logs"):
            self.config_manager.ruta_logs = logs

        # Romper de forma segura la asignación de ventana modal
        try:
            self.grab_release()
        except Exception:
            pass

        self.destroy()