import sys

from PySide6.QtWidgets import QWidget, QApplication, QMessageBox, QLineEdit


from vistas.ui_geninformes import Ui_Form





class MiApp(QWidget, Ui_Form):
   
    def __init__(self):
        super().__init__()
        self.setupUi(self)
     
        
    
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mi_app = MiApp()
    mi_app.show()
    
    sys.exit(app.exec())