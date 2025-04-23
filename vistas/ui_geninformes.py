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
        # Conectar la señal de Enter para actualizar la lista
        self.cdrTxtRutaEntrada.returnPressed.connect(self.cambiar_ruta)
        self.btnGenInforme.clicked.connect(self.generar_informe)

        # Conectar clics del ratón para abrir explorador
        self.cdrTxtRutaEntrada.mousePressEvent = self.abrir_explorador_ruta_entrada
        self.cdrTxtRutaSalida.mousePressEvent = self.abrir_explorador_ruta_salida

        # Cargar la lista inicial al iniciar la interfaz
        try:
            # self.comboBoxFicheros.addItems(os.listdir(self.cdrTxtRutaEntrada.text())) # Línea original
             self.cambiar_ruta() # Llamamos a cambiar_ruta para cargar y filtrar
        except FileNotFoundError:
            self.aviso("Aviso ruta de entrada", "Indica la ruta de los ficheros jrxml")


    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Generar Informes Fábrica", None))
        self.btnGenInforme.setText(QCoreApplication.translate("Form", u"Generar Informe", None))
        self.cdrTxtRutaSalida.setPlaceholderText(QCoreApplication.translate("Form", u"Ruta ficheros generados", None))
        self.cdrTxtRutaEntrada.setPlaceholderText(QCoreApplication.translate("Form", u"Ruta ficheros jrxml", None))
        self.cdrTxtRutaEntrada.setToolTip(QCoreApplication.translate("Form", u"Pulsar enter para actualizar la lista de ficheros", None))


    def abrir_explorador_ruta_entrada(self, event):
        ruta = QFileDialog.getExistingDirectory(None, "Selecciona la carpeta de los ficheros jrxml", self.cdrTxtRutaEntrada.text() if os.path.exists(self.cdrTxtRutaEntrada.text()) else os.getcwd())
        if ruta:
            self.cdrTxtRutaEntrada.setText(ruta)
            self.cambiar_ruta() # Actualizar lista después de seleccionar la ruta

    def abrir_explorador_ruta_salida(self, event):
        ruta = QFileDialog.getExistingDirectory(None, "Selecciona la carpeta de destino para los PDF", self.cdrTxtRutaSalida.text() if os.path.exists(self.cdrTxtRutaSalida.text()) else os.getcwd())
        if ruta:
            self.cdrTxtRutaSalida.setText(ruta)


    def aviso(self, titulo, texto):
        dialogo = QMessageBox(self)
        dialogo.setWindowTitle(titulo)
        dialogo.setText(texto)
        dialogo.exec()

    def pedir_parametros(self, pLista):
        # Asegúrate de que pLista no esté vacío antes de usar QInputDialog
        if not pLista:
            self.aviso("Error de Parámetros", "No hay parámetros definidos para este informe.")
            return None # O manejar el caso de lista vacía según necesites

        pTitulo = "Parámetros"
        pTexto = "Selecciona el parámetro:" # Texto más claro para el usuario
        sel, conf = QInputDialog.getItem(self, pTitulo, pTexto, pLista, 0, False) # Añadido índice inicial y no editable
        if conf:
            return sel
        return None # Retornar None si el usuario cancela

    def error(self, pLista): # Esta función parece incompleta o un placeholder
        print("Función de error llamada con:", pLista)
        return "" # Retorna un valor por defecto, revisa si esto es lo esperado


    def generar_informe(self):
        # Diccionario de configuración de parámetros por nombre de fichero (sin extensión)
        # Para 'clientes' se espera el parámetro 'param_cliente' y se usa pedir_parametros sin lista inicial (se debería pasar la lista real de clientes)
        # Para otros ficheros, si no están en este diccionario, no se pedirán parámetros y se usará un diccionario vacío {}
        configuracion_parametros = {
            'InformeAlbaranesSinSubinformeSQL': {'param_cliente': (self.pedir_parametros, ["Cliente1", "Cliente2", "Cliente3"])}, # Ejemplo: pasar lista real de clientes
            # Añade aquí otros informes que requieran parámetros y sus configuraciones
            # 'OtroInformeConParametro': {'nombre_parametro': (self.pedir_parametros, ["ValorA", "ValorB"])}
        }


        ficheroEntrada = os.path.join(self.cdrTxtRutaEntrada.text(), self.comboBoxFicheros.currentText())
        # Asegurarse de que la ruta de salida existe o usar la de entrada
        rutaSalida = self.cdrTxtRutaSalida.text()
        if not os.path.exists(rutaSalida):
             self.aviso("Atención", f"El directorio de salida '{rutaSalida}' no existe.\nLos informes se generarán en el directorio de entrada.")
             rutaSalida = self.cdrTxtRutaEntrada.text()

        # Generar el nombre del fichero de salida (sin extensión jrxml, con extensión pdf)
        nombre_fichero_salida_base, _ = os.path.splitext(self.comboBoxFicheros.currentText())
        ficheroSalida = os.path.join(rutaSalida, nombre_fichero_salida_base + ".pdf")


        fichero_sel_base = os.path.splitext(self.comboBoxFicheros.currentText())[0] # Nombre del fichero sin extensión

        # Obtener la configuración de parámetros para el fichero seleccionado
        params_info = configuracion_parametros.get(fichero_sel_base, {}) # Usa diccionario vacío si no hay config

        parametros_a_enviar = {}
        for param_nombre, (metodo_pedir, lista_valores) in params_info.items():
             valor_param = metodo_pedir(lista_valores) # Llama al método para pedir el valor
             if valor_param is not None: # Solo añade el parámetro si el usuario no canceló
                 parametros_a_enviar[param_nombre] = valor_param
             else:
                 # Si un parámetro requerido es cancelado, podrías querer abortar la generación
                 self.aviso("Generación Cancelada", f"El valor para el parámetro '{param_nombre}' no fue proporcionado.")
                 return # Aborta la función generar_informe


        # Asegúrate de que crearinforme.advanced_example_using_database pueda manejar un diccionario vacío de parámetros
        try:
            crearinforme.advanced_example_using_database(ficheroEntrada, ficheroSalida, parametros_a_enviar)
            self.aviso("Informe Generado", f"El informe '{os.path.basename(ficheroSalida)}' ha sido generado con éxito.")
        except Exception as e:
            self.aviso("Error al Generar Informe", f"Ocurrió un error: {e}")


    def cambiar_ruta(self):
        try:
            self.comboBoxFicheros.clear()
            ruta_entrada = self.cdrTxtRutaEntrada.text()
            if os.path.exists(ruta_entrada) and os.path.isdir(ruta_entrada):
                items = os.listdir(ruta_entrada)
                # Filtrar solo archivos con extensión .jrxml
                ficheros_jrxml = [item for item in items if item.lower().endswith('.jrxml') and os.path.isfile(os.path.join(ruta_entrada, item))]
                ficheros_jrxml.sort() # Ordenar alfabéticamente
                self.comboBoxFicheros.addItems(ficheros_jrxml)
            else:
                 # Manejar caso de ruta no válida o no es un directorio
                 self.aviso("Ruta no válida", f"La ruta especificada '{ruta_entrada}' no es un directorio válido.")
                 self.comboBoxFicheros.clear() # Asegurarse de que la lista está vacía si la ruta es inválida

        except Exception as e:
            # Captura cualquier otra excepción (permisos, etc.)
            self.aviso("Error al cambiar ruta", f"Ocurrió un error al listar ficheros: {e}")
            self.comboBoxFicheros.clear()

