from src.app import CarbonFreeApp
from src.gui import MainWindow, SetupDialog


def main():
    app = CarbonFreeApp()

    # 1. Crear ventana principal
    ventana = MainWindow(app)

    # 2. Si requiere configuración previa, abre el diálogo en primer plano
    if app.config.necesita_configuracion:
        setup = SetupDialog(config_manager=app.config, parent_window=ventana)
        ventana.wait_window(setup)

        # Re-inicializar servicios con las rutas elegidas
        if hasattr(app, "inicializar_servicios"):
            app.inicializar_servicios()

    # 3. Inicia el bucle principal de la interfaz
    if not app.config.necesita_configuracion:
        ventana.mainloop()


if __name__ == "__main__":
    main()