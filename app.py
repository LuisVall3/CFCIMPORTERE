from src.app import CarbonFreeApp
from src.gui import MainWindow, SetupDialog


def main():

    app = CarbonFreeApp()

    # Si faltan las rutas en config.json, abre el diálogo de selección
    if app.config.necesita_configuracion:
        # AQUÍ ESTÁ EL CAMBIO: asignamos el parámetro de forma explícita
        setup = SetupDialog(config_manager=app.config)
        setup.mainloop()

        # Carga los loggers y manejadores de archivos con las rutas elegidas
        app.inicializar_servicios()

    # Inicia la ventana principal solo si la configuración está completa
    if not app.config.necesita_configuracion:
        ventana = MainWindow(app)
        ventana.mainloop()


if __name__ == "__main__":
    main()