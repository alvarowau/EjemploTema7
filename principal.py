import sys

from PySide6.QtWidgets import QWidget, QApplication, QMessageBox, QLineEdit
# Asegúrate de que el archivo vistas/style.py contiene la variable style_sheet


from vistas.ui_geninformes import Ui_Form

# Asegúrate de que tus controladores existen y son correctos
# from controladores import crearinforme # Si usas esto en MiApp, impórtalo aquí


class MiApp(QWidget, Ui_Form):

    def __init__(self):
        super().__init__()
        # setupUi se encarga de configurar la interfaz definida en ui_geninformes.py
        self.setupUi(self)




    # Si los métodos como generar_informe, cambiar_ruta, aviso, etc. están definidos en tu clase MiApp
    # deben estar aquí dentro.


if __name__ == "__main__":
    app = QApplication(sys.argv)



    mi_app = MiApp()
    mi_app.show()

    sys.exit(app.exec())