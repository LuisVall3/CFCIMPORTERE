from src.app import CarbonFreeApp
from src.gui import MainWindow, SetupDialog


def main():
    app = CarbonFreeApp()

    # 1. Instanciamos MainWindow primero para darle a Tkinter su ventana raíz (Root)
    ventana = MainWindow(app)

    # 2. Si faltan rutas, usamos la ventana principal (oculta) como padre
    if app.config.necesita_configuracion:
        ventana.withdraw()  # Oculta la ventana principal mientras configuras

        setup = SetupDialog(config_manager=app.config, parent_window=ventana)
        ventana.wait_window(setup)  # Espera a que se guarde y cierre SetupDialog

        # Carga los loggers y manejadores con las rutas ya guardadas
        app.inicializar_servicios()

        ventana.deiconify()  # Muestra la ventana principal ya lista

    # 3. Muestra e inicia la interfaz gráfica si la configuración está completa
    if not app.config.necesita_configuracion:
        ventana.mainloop()


if __name__ == "__main__":
    main()