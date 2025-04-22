# -*- coding: utf-8 -*-

import os
import sys
from PySide6.QtCore import QCoreApplication, QRect
from PySide6.QtWidgets import (
    QApplication, QComboBox, QLineEdit, QPushButton,
    QWidget, QMessageBox, QInputDialog, QFileDialog
)
from controladores import crearinforme


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(400, 300)

        self.btnGenInforme = QPushButton(Form)
        self.btnGenInforme.setObjectName(u"btnGenInforme")
        self.btnGenInforme.setGeometry(QRect(270, 100, 111, 23))

        self.comboBoxFicheros = QComboBox(Form)
        self.comboBoxFicheros.setObjectName(u"comboBoxFicheros")
        self.comboBoxFicheros.setGeometry(QRect(20, 100, 231, 23))

        self.cdrTxtRutaSalida = QLineEdit(Form)
        self.cdrTxtRutaSalida.setObjectName(u"cdrTxtRuta")
        self.cdrTxtRutaSalida.setGeometry(QRect(40, 180, 281, 23))

        self.cdrTxtRutaEntrada = QLineEdit(Form)
        self.cdrTxtRutaEntrada.setObjectName(u"cdrTxtRuta_2")
        self.cdrTxtRutaEntrada.setGeometry(QRect(20, 40, 281, 23))

        ruta_base = os.getcwd()
        self.cdrTxtRutaEntrada.setText(ruta_base)
        self.cdrTxtRutaSalida.setText(ruta_base)

        self.retranslateUi(Form)

        self.cdrTxtRutaEntrada.returnPressed.connect(self.cambiar_ruta)
        self.btnGenInforme.clicked.connect(self.generar_informe)

        self.cdrTxtRutaEntrada.mousePressEvent = self.abrir_explorador_ruta_entrada
        self.cdrTxtRutaSalida.mousePressEvent = self.abrir_explorador_ruta_salida

        try:
            self.comboBoxFicheros.addItems(os.listdir(self.cdrTxtRutaEntrada.text()))
        except FileNotFoundError:
            self.aviso("Aviso ruta de entrada", "Indica la ruta de los ficheros jrxml")

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Generar Informes Fábrica", None))
        self.btnGenInforme.setText(QCoreApplication.translate("Form", u"Generar Informe", None))
        self.cdrTxtRutaSalida.setPlaceholderText(QCoreApplication.translate("Form", u"Ruta ficheros generados", None))
        self.cdrTxtRutaEntrada.setPlaceholderText(QCoreApplication.translate("Form", u"Ruta ficheros jrxml", None))
        self.cdrTxtRutaEntrada.setToolTip(QCoreApplication.translate("Form", u"Pulsar enter para actualizar la lista de ficheros", None))

    def abrir_explorador_ruta_entrada(self, event):
        ruta = QFileDialog.getExistingDirectory(None, "Selecciona la carpeta de los ficheros jrxml", os.getcwd())
        if ruta:
            self.cdrTxtRutaEntrada.setText(ruta)
            self.cambiar_ruta()

    def abrir_explorador_ruta_salida(self, event):
        ruta = QFileDialog.getExistingDirectory(None, "Selecciona la carpeta de destino para los PDF", os.getcwd())
        if ruta:
            self.cdrTxtRutaSalida.setText(ruta)

    def aviso(self, titulo, texto):
        dialogo = QMessageBox(self)
        dialogo.setWindowTitle(titulo)
        dialogo.setText(texto)
        dialogo.exec()

    def pedir_parametros(self, pLista):
        pTitulo = "Parámetros"
        pTexto = "Parámetros"
        sel, conf = QInputDialog.getItem(self, pTitulo, pTexto, pLista)
        if conf:
            return sel

    def error(self, pLista):
        return ""

    def generar_informe(self):
        mens_error = ("", self.error, "")
        sel_param = {
            'Informe_4_1_1_1_parametro_texto': ('Comentario', self.pedir_parametros, ""),
            'Informe_4_1_1_filtrado_datos': ('Ciudad', self.pedir_parametros,
                                             ['Almendralejo', 'Cáceres', 'Madrid', 'Salamanca', 'Santander', 'Sevilla']),
            'Informe_4_1_1_ordenar_datos': ('Orden', self.pedir_parametros,
                                           ['Ciudad', 'Direccion', 'Nombre']),
            'Informe_4_7_1_Graficos': ('Titulo', self.pedir_parametros, ""),
            'Informe_4_5_1_InformePrincipal': ('Titulo', self.pedir_parametros, ""),
            'clientes':('param_cliente', self.pedir_parametros, ""),
        }

        ficheroEntrada = self.cdrTxtRutaEntrada.text() + "/" + self.comboBoxFicheros.currentText()
        ficheroSalida = self.cdrTxtRutaSalida.text() + "/" + self.comboBoxFicheros.currentText()[:-6]

        if not os.path.exists(self.cdrTxtRutaSalida.text()):
            ficheroSalida = ficheroEntrada[:-6]
            self.aviso("Atención", "El directorio de salida " + self.cdrTxtRutaSalida.text() +
                       " no existe\nInformes en directorio de entrada")

        fichero_sel = self.comboBoxFicheros.currentText()[:-6]
        parametros = {
            sel_param.get(fichero_sel, mens_error)[0]:
                sel_param.get(fichero_sel, mens_error)[1]
                (sel_param.get(fichero_sel, mens_error)[2])
        }

        crearinforme.advanced_example_using_database(ficheroEntrada, ficheroSalida, parametros)

    def cambiar_ruta(self):
        try:
            self.comboBoxFicheros.clear()
            items = os.listdir(self.cdrTxtRutaEntrada.text())
            items.sort()
            self.comboBoxFicheros.addItems(items)
        except FileNotFoundError:
            self.aviso("Al cambiar ruta", "No existe el directorio " + self.cdrTxtRutaEntrada.text())


class MiApp(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mi_app = MiApp()
    mi_app.show()
    sys.exit(app.exec())

