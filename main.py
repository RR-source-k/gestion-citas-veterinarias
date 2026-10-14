"""Punto de entrada de la aplicación de gestión de citas veterinarias."""
from presentacion.presentacion import Presentacion


class Main:
    """Clase que inicia la aplicación."""

    @staticmethod
    def main() -> None:
        presentacion = Presentacion()
        presentacion.iniciar_interfaz()


if __name__ == "__main__":
    Main.main()
