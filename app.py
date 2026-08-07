from src.app import CarbonFreeApp
from src.gui import MainWindow


def main():

    app = CarbonFreeApp()

    ventana = MainWindow(app)

    ventana.mainloop()


if __name__ == "__main__":
    main()