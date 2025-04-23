import sys

from PySide6.QtWidgets import QWidget, QApplication, QMessageBox, QLineEdit

from vistas.ui_geninformes import Ui_Form

class MiApp(QWidget, Ui_Form):
    """
    Clase principal de la aplicación, que hereda de QWidget y Ui_Form.

    Esta clase inicializa la interfaz de usuario definida en 'ui_geninformes' y establece
    los elementos gráficos necesarios para la aplicación.

    Args:
        None

    Returns:
        None
    """

    def __init__(self):
        """
        Inicializa la clase MiApp y configura la interfaz de usuario.

        Configura la interfaz utilizando el método 'setupUi' de la clase Ui_Form y muestra
        el formulario principal.

        Args:
            None

        Returns:
            None
        """
        super().__init__()
        self.setupUi(self)


if __name__ == "__main__":
    """
    Punto de entrada principal para ejecutar la aplicación.

    Crea una instancia de la clase MiApp, la muestra en pantalla y ejecuta el ciclo
    de eventos de la aplicación.

    Args:
        None

    Returns:
        int: El código de salida de la aplicación.
    """
    app = QApplication(sys.argv)

    mi_app = MiApp()
    mi_app.show()

    sys.exit(app.exec())
